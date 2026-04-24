from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User, Group as AuthGroup
from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .models import Product, Lesson, ProductAccess
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    AssignRoleSerializer,
    ProductSerializer,
    ProductCreateSerializer,
    LessonSerializer,
    ProductAccessSerializer,
)
from .permissions import IsTeacherOrAdmin, IsAdminOnly, HasProductAccess
from .utils import grant_access_and_assign_group
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'user_id': user.id,
            'username': user.username,
            'token': token.key,
        }, status=status.HTTP_201_CREATED)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'user_id': user.id,
            'username': user.username,
            'token': token.key,
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if not user:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)
        auth_login(request, user)
        return Response({
            'user_id': user.id,
            'username': user.username,
            'token': token.key,
            'roles': list(user.groups.values_list('name', flat=True))
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        auth_logout(request)
        return Response({'detail': 'Logged out'}, status=status.HTTP_200_OK)


class AssignRoleView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOnly]

    def post(self, request):
        serializer = AssignRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(User, id=serializer.validated_data['user_id'])
        role = serializer.validated_data['role']

        for group_name in ['student', 'teacher', 'admin']:
            g, _ = AuthGroup.objects.get_or_create(name=group_name)
            user.groups.remove(g)

        if role == 'admin':
            user.is_staff = True
            user.is_superuser = True
            user.save(update_fields=['is_staff', 'is_superuser'])
        else:
            user.is_staff = False
            if user.is_superuser:
                user.is_superuser = False
                user.save(update_fields=['is_staff', 'is_superuser'])

        group, _ = AuthGroup.objects.get_or_create(name=role)
        user.groups.add(group)

        return Response({
            'detail': 'Role assigned',
            'user_id': user.id,
            'role': role
        })


class ProductCreateView(APIView):
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def post(self, request):
        serializer = ProductCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save(creator=request.user)
        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)


class AvailableProductsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.annotate(lessons_count=Count('lessons')).select_related('creator')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductLessonsView(APIView):
    permission_classes = [IsAuthenticated, HasProductAccess]

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        self.check_object_permissions(request, product)
        lessons = Lesson.objects.filter(product=product)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)


class GrantAccessView(APIView):
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def post(self, request):
        serializer = ProductAccessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = get_object_or_404(Product, id=serializer.validated_data['product'].id)
        user = get_object_or_404(User, id=serializer.validated_data['user'].id)

        access, created = grant_access_and_assign_group(product, user)
        return Response({
            'access_id': access.id,
            'created': created,
            'user': user.id,
            'product': product.id
        }, status=status.HTTP_201_CREATED)

def home_view(request):
    return render(request, 'for_test/home.html')

class ProductListView(ListView):
    model = Product
    template_name = 'for_test/product_list.html'
    context_object_name = 'products'

def about_view(request):
    return render(request, 'for_test/about.html')

def contacts_view(request):
    return render(request, 'for_test/contacts.html')

@login_required(login_url='login')
def buy_product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'for_test/buy.html', {'product': product})

def home_view(request):
    return render(request, 'for_test/home.html')

class ProductListView(ListView):
    model = Product
    template_name = 'for_test/product_list.html'
    context_object_name = 'products'

def about_view(request):
    return render(request, 'for_test/about.html')

def contacts_view(request):
    return render(request, 'for_test/contacts.html')

@login_required(login_url='login')
def buy_product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'for_test/buy.html', {'product': product})

@login_required(login_url='login')
def profile_view(request):
    return render(request, 'for_test/profile.html')