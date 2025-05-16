from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status, generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .filters import EquipmentFilter, EquipmentTypeFilter
from .models import Equipment, EquipmentType
from .pagination import StandardResultsSetPagination
from .serializers import EquipmentSerializer, EquipmentTypeSerializer, \
    UserLoginSerializer, UserRegisterSerializer
from .services.equipment import create_equipment, soft_delete_equipment, \
    update_equipment
from .services.user import register_user, generate_tokens_for_user


class EquipmentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing equipment types.
    """
    queryset = (EquipmentType.objects
                             .with_equipment_count()
                             .order_by('id', 'name'))
    serializer_class = EquipmentTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = EquipmentTypeFilter
    search_fields = ['name', 'serial_number_mask']
    pagination_class = StandardResultsSetPagination


class EquipmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing equipment.
    """
    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = EquipmentFilter
    ordering_fields = ['id', 'created_at', 'updated_at', 'serial_number']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return (Equipment.objects
                .active()
                .order_by('id', 'created_at'))

    def create(self, request, *args, **kwargs):
        equipment_type_id = request.data.get('equipment_type')
        if 'serial_numbers' in request.data:
            serial_numbers = request.data.get('serial_numbers')
        else:
            serial_numbers = [request.data.get('serial_number', '')]
        notes = request.data.get('notes', '')

        try:
            equipment_list = create_equipment(
                equipment_type_id, serial_numbers, notes
            )
        except ValidationError as e:
            return Response(
                {
                    "serial_numbers_errors":
                        e.detail.get("serial_numbers_errors", [])
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        result_serializer = self.get_serializer(equipment_list, many=True)
        return Response(
            result_serializer.data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        equipment = self.get_object()
        new_serial_number = request.data.get('serial_number')
        new_equipment_type = request.data.get('equipment_type')
        notes = request.data.get('notes')

        try:
            equipment = update_equipment(
                equipment, new_equipment_type, new_serial_number, notes
            )
        except ValidationError as e:
            return Response(
                {
                    "serial_numbers_errors":
                        e.detail.get("serial_numbers_errors", [])
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        result_serializer = self.get_serializer(equipment)
        return Response(
            result_serializer.data,
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        """Safe delete"""
        equipment = self.get_object()
        soft_delete_equipment(equipment)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        Retrieve single equipment instance by ID.
        """
        equipment = Equipment.objects.get_active_or_404(pk=pk)
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

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        tokens = generate_tokens_for_user(user)

        return Response({
            'access_token': tokens['access_token'],
            'refresh_token': tokens['refresh_token'],
            'user_id': user.pk,
            'email': user.email,
            'username': user.username
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

        try:
            user = register_user(username, password, email)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        tokens = generate_tokens_for_user(user)

        return Response({
            'access_token': tokens['access_token'],
            'refresh_token': tokens['refresh_token'],
            'user_id': user.pk,
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_201_CREATED)
