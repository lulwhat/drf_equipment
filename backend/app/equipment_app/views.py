from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Equipment, EquipmentType
from .pagination import StandardResultsSetPagination
from .serializers import EquipmentSerializer, EquipmentTypeSerializer, \
    BulkEquipmentCreateSerializer, UserLoginSerializer, UserRegisterSerializer


class EquipmentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing equipment types.
    """
    queryset = EquipmentType.objects.annotate(
        equipment_count=Count(
            'equipment',
            filter=Q(equipment__is_deleted=False)
        )
    ).order_by('id', 'name')
    serializer_class = EquipmentTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'serial_number_mask']
    pagination_class = StandardResultsSetPagination


class EquipmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing equipment.
    """
    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['serial_number', 'notes', 'equipment_type__name']
    filterset_fields = ['equipment_type']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return (Equipment.objects
                .filter(is_deleted=False)
                .order_by('id', 'created_at'))

    def create(self, request, *args, **kwargs):
        if 'serial_numbers' in request.data:
            serializer = BulkEquipmentCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            equipment_list = serializer.save()
            result_serializer = EquipmentSerializer(equipment_list, many=True)
            return Response(result_serializer.data,
                            status=status.HTTP_201_CREATED)
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Safe delete"""
        equipment = self.get_object()
        equipment.is_deleted = True
        equipment.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        Retrieve single equipment instance by ID.
        """
        equipment = get_object_or_404(Equipment, pk=pk, is_deleted=False)
        serializer = self.get_serializer(equipment)
        return Response(serializer.data)


class UserLoginView(generics.GenericAPIView):
    """
    User authentication (token issuance).
    """
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.check_password(password):
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response({
            "access_token": str(access_token),
            "refresh_token": str(refresh),
            "user_id": user.pk,
            "email": user.email,
            "username": user.username
        })


class UserRegisterView(generics.GenericAPIView):
    """
    Register a new user and return JWT tokens.
    """
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        email = serializer.validated_data.get('email', '')

        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response({
            'access_token': str(access_token),
            'refresh_token': str(refresh),
            'user_id': user.pk,
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_201_CREATED)
