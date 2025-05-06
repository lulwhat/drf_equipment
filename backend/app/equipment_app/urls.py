from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, \
    TokenRefreshView, TokenVerifyView

from . import views

router = DefaultRouter()
router.register(r'equipment', views.EquipmentViewSet,
                basename='equipment')
router.register(r'equipment-type', views.EquipmentTypeViewSet,
                basename='equipment-type')

urlpatterns = [
    # ViewSet routes
    path('', include(router.urls)),
    
    # Authentication endpoints  
    path('token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(),
         name='token_verify'),
    path('user/login', views.UserLoginView.as_view(), name='user_login'),
    path('user/register', views.UserRegisterView.as_view(),
         name='user_register'),
]
