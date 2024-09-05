from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Dispatch
from .serializers import DispatchSerializer

from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import (
    ConsignmentSerializer, 
    ReceivingSerializer, 
    AssetSerializer, 
    RegisterSerializer, 
    LoginSerializer
)
from .models import Consignment, Receiving, Asset
from django.urls import reverse

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_consignment(request):
    serializer = ConsignmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def list_consignments(request):
    consignments = Consignment.objects.all()
    serializer = ConsignmentSerializer(consignments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Only authenticated users can view Receiving instances
def list_receivings(request):
    receivings = Receiving.objects.all()
    serializer = ReceivingSerializer(receivings, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Only authenticated users can add Receiving instances
def add_receiving(request):
    serializer = ReceivingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Only authenticated users can view Asset instances
def list_assets(request):
    assets = Asset.objects.all()
    serializer = AssetSerializer(assets, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Only authenticated users can add Asset instances
def add_asset(request):
    serializer = AssetSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)  # Create token
            login_url = request.build_absolute_uri(reverse('login'))
            return Response({
                "message": "User registered successfully!",
                "token": token.key,
                "redirect_url": login_url
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)  # Create token on login
                consignments_url = request.build_absolute_uri(reverse('list_consignments'))
                return Response({
                    "message": "Login successful!",
                    "token": token.key,
                    "redirect_url": consignments_url
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ListDispatches(generics.ListAPIView):
    queryset = Dispatch.objects.all()
    serializer_class = DispatchSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

class AddDispatch(generics.CreateAPIView):
    queryset = Dispatch.objects.all()
    serializer_class = DispatchSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def perform_create(self, serializer):
        # Automatically set the user and approver from the request
        serializer.save(user=self.request.user)
