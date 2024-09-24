from django.urls import path,include
from .views import *
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import LocationViewSet, CategoryViewSet,LocationCreate


router = DefaultRouter()
router.register(r'locations', LocationViewSet)
router.register(r'categories', CategoryViewSet) 


urlpatterns = [
    # Consignment URLs
    path('consignments/', list_consignments, name='list_consignments'),
    path('api/consignments/add/', AddConsignmentAPIView.as_view(), name='add_consignment'),
    # path('api/consignments/', add_consignment, name='add_consignment'),

    # Receiving URLs
    path('receivings/', list_receivings, name='list_receivings'),
     path('api/receivings/add/', AddReceivingAPIView.as_view(), name='add_receiving'),
    # path('api/receivings/add/', add_receiving, name='add_receiving'),

    # Asset URLs
    path('assets/', list_assets, name='list_assets'),
    path('assets/create/', AssetCreateView.as_view(), name='asset-create'),
    # path('api/assets/add/', add_asset, name='add_asset'),

     # Dispatch URLs
    path('dispatches/', ListDispatches.as_view(), name='list_dispatches'),  # Updated to use ListDispatches
    path('api/dispatches/add/', AddDispatch.as_view(), name='add_dispatch'),  # Updated to use AddDispatch


    # Authentication URLs
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    
    
    
    path('api/', include(router.urls)), 
    path('api/locations/add', LocationCreate.as_view(), name='location-create'),
    path('api/category/add', CategoryCreate.as_view(), name='category-create'),
]
