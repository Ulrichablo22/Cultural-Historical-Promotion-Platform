from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views
from rest_framework_simplejwt.views import TokenRefreshView


router = DefaultRouter()
router.register(r'lieux', views.LieuViewSet)
router.register(r'evenements', views.EvenementViewSet)
router.register(r'medias', views.MediaViewSet)
router.register(r'avis', views.AvisViewSet)
router.register(r'utilisateurs', views.UserViewSet)
router.register(r'users', views.UserProfileViewSet, basename='profile')
router.register(r'notifications', views.NotificationViewSet, basename='notifications')


urlpatterns = [
    path('', include(router.urls)),  # Ajouter les routes des ViewSets
    path('log_in/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('sign_up/', views.RegisterView.as_view(), name='auth_register'),
    path('test/', views.testEndPoint, name='test'),
    path('routes/', views.getRoutes, name='api_routes'),
    path('search/', views.search, name='search'),
]
