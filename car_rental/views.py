from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST,HTTP_200_OK
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_available', 'price_per_day']
    search_fields = ['car_name', 'car_desc']
    ordering_fields = ['price_per_day', 'car_name']

    def get_permissions(self):
        if self.action in ['create', 'update']:
            return [permissions.DjangoModelPermissions()]
        return super().get_permissions()

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['customer', 'rental_date', 'days_for_rent']
    search_fields = ['loc_from', 'loc_to']
    ordering_fields = ['rental_date', 'total_price']

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.DjangoModelPermissions()]
        return super().get_permissions()

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['city', 'date_joined']
    search_fields = ['name', 'email', 'phone']
    ordering_fields = ['date_joined', 'name']

    def get_permissions(self):
        if self.action == 'update':
            return [permissions.DjangoModelPermissions()]
        return super().get_permissions()

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(username=email, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=HTTP_200_OK)


class CustomerRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful"}, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
