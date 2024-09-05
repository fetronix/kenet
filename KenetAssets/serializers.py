from rest_framework import serializers
from .models import *

class ConsignmentSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.name', read_only=True)
    received_by_name = serializers.CharField(source='received_by.username', read_only=True)
    class Meta:
        model = Consignment
        fields = [
            'id',
            'slk_id',
            'supplier',
            'quantity',
            'datetime',
            'invoice_number',
            'invoice',
            'comments',
            'project',
            'location_name',  # Use location_name instead of location
            'received_by_name',  # Use received_by_name instead of received_by
        ]

class ReceivingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receiving
        fields = '__all__'

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'


from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email')
        )
        return user



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)




class DispatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispatch
        fields = ['id', 'asset', 'user', 'approver', 'status', 'datetime', 'comments', 'destination', 'location']

    def validate(self, attrs):
        # Example validation to ensure that the asset is available for dispatch
        asset = attrs.get('asset')
        if asset.status != 'available':
            raise serializers.ValidationError("Asset must be available for dispatch.")
        return attrs
