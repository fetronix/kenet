from django.urls import path
from .views import (
    list_consignments, 
    add_consignment, 
    list_receivings, 
    add_receiving, 
    list_assets, 
    add_asset, 
    ListDispatches,  # Use the new ListDispatches view
    AddDispatch,     # Use the new AddDispatch view
    RegisterAPIView, 
    LoginAPIView
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # Consignment URLs
    path('consignments/', list_consignments, name='list_consignments'),
    path('api/consignments/', add_consignment, name='add_consignment'),

    # Receiving URLs
    path('receivings/', list_receivings, name='list_receivings'),
    path('api/receivings/add/', add_receiving, name='add_receiving'),

    # Asset URLs
    path('assets/', list_assets, name='list_assets'),
    path('api/assets/add/', add_asset, name='add_asset'),

     # Dispatch URLs
    path('dispatches/', ListDispatches.as_view(), name='list_dispatches'),  # Updated to use ListDispatches
    path('api/dispatches/add/', AddDispatch.as_view(), name='add_dispatch'),  # Updated to use AddDispatch


    # Authentication URLs
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
