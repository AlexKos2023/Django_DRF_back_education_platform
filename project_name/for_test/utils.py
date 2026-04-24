from django.db import transaction
from django.db.models import Count
from .models import Group, ProductAccess


@transaction.atomic
def grant_access_and_assign_group(product, user):
    access, created = ProductAccess.objects.get_or_create(user=user, product=product)
    assign_user_to_group(product, user)
    return access, created


@transaction.atomic
def assign_user_to_group(product, user):
    groups = list(
        Group.objects.select_for_update()
        .filter(product=product)
        .annotate(users_count=Count('users'))
        .order_by('users_count', 'id')
    )

    if not groups:
        return None

    for group in groups:
        if group.users_count < product.max_group_size and not group.users.filter(id=user.id).exists():
            group.users.add(user)
            return group

    return None


@transaction.atomic
def rebalance_groups(product):
    if product.has_started:
        return False

    groups = list(
        Group.objects.select_for_update()
        .filter(product=product)
        .annotate(users_count=Count('users'))
        .order_by('id')
    )

    if not groups:
        return False

    all_users = []
    for group in groups:
        all_users.extend(list(group.users.all()))
        group.users.clear()

    total = len(all_users)
    n = len(groups)

    if n == 0:
        return False

    base = total // n
    extra = total % n

    idx = 0
    for i, group in enumerate(groups):
        target = base + (1 if i < extra else 0)
        target = max(target, product.min_group_size)
        target = min(target, product.max_group_size)

        for _ in range(target):
            if idx >= total:
                break
            group.users.add(all_users[idx])
            idx += 1

    for user in all_users[idx:]:
        for group in groups:
            if group.users.count() < product.max_group_size:
                group.users.add(user)
                break

    return True