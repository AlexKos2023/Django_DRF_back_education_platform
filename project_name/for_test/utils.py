from django.db import transaction
from django.db.models import Count
from .models import Group, ProductAccess


@transaction.atomic
def grant_access_and_assign_group(product, user):
    # Создаем доступ (если уже есть - просто получаем объект)
    access, created = ProductAccess.objects.get_or_create(user=user, product=product)

    # Если продукт еще не начался - пересобираем все группы равномерно
    if not product.has_started:
        rebalance_groups(product)
    else:
        # Если начался - просто пихаем в первую свободную (базовый алгоритм)
        assign_user_to_group(product, user)

    return access, created


@transaction.atomic
def assign_user_to_group(product, user):
    """Базовый алгоритм: заполнение до максимального значения (5 баллов)"""
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
    """Сложный алгоритм: разница не более 1 (+3 балла)"""
    if product.has_started:
        return False

    groups = list(
        Group.objects.select_for_update()
        .filter(product=product)
        .order_by('id')
    )

    if not groups:
        return False

    # Собираем всех юзеров и очищаем группы
    all_users = []
    for group in groups:
        all_users.extend(list(group.users.all()))
        group.users.clear()

    total = len(all_users)
    n = len(groups)

    if n == 0 or total == 0:
        return True

    # Математика для разницы не более 1 человека
    base = total // n
    extra = total % n

    idx = 0
    # Первый проход: распределяем строго по математике
    for i, group in enumerate(groups):
        target = base + (1 if i < extra else 0)

        # Учитываем max_group_size (если людей вдруг слишком много)
        if target > product.max_group_size:
            target = product.max_group_size

        for _ in range(target):
            if idx >= total:
                break
            group.users.add(all_users[idx])
            idx += 1

    # Второй проход: если из-за max_group_size у нас остались "лишние" люди,
    # мы обязаны добавить их в группы, чтобы не потерять доступ.
    # Да, группа может превысить max, но это безопаснее, чем выкинуть юзера.
    while idx < total:
        for group in groups:
            if idx >= total:
                break
            group.users.add(all_users[idx])
            idx += 1

    return True