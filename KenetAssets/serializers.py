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
        
class ConsignmentCreateSerializer(serializers.ModelSerializer):
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())  # Dropdown for location
    invoice = serializers.FileField()  # For file upload

    class Meta:
        model = Consignment
        fields = ['supplier', 'quantity', 'location', 'invoice_number', 'invoice', 'comments', 'project']

    def create(self, validated_data):
        request = self.context.get('request')  # Get request context to fetch the current user
        validated_data['received_by'] = request.user  # Set the received_by field as the current user
        return super().create(validated_data)

class ReceivingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receiving
        fields = '__all__'
        
        
from rest_framework import serializers
from .models import Receiving, Consignment, Category

class ReceivingCreateSerializer(serializers.ModelSerializer):
    consignment = serializers.PrimaryKeyRelatedField(queryset=Consignment.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True, required=False)
    
    # Dropdown for status field
    status = serializers.ChoiceField(choices=Receiving.STATUS_CHOICES)

    class Meta:
        model = Receiving
        fields = [
            'consignment', 
            'serial_number', 
            'description', 
            'name', 
            'model', 
            'category', 
            'status'
        ]

    def create(self, validated_data):
        consignment = validated_data['consignment']
        
        # Automatically populate fields based on the selected consignment
        validated_data['supplier'] = consignment.supplier
        validated_data['received_by'] = consignment.received_by
        validated_data['invoice_number'] = consignment.invoice_number
        validated_data['location'] = consignment.location
        
        return super().create(validated_data)


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

from rest_framework import serializers
from .models import Asset, Receiving, Location

class AssetCreateSerializer(serializers.ModelSerializer):
    receiving = serializers.PrimaryKeyRelatedField(queryset=Receiving.objects.all())
    
    class Meta:
        model = Asset
        fields = [
            'receiving',
            'tag_number',
            'status',  # Editable status
        ]
    
    def create(self, validated_data):
        receiving = validated_data['receiving']
        
        # Automatically populate fields from the selected receiving instance
        validated_data['description'] = receiving.description
        validated_data['serial_number'] = receiving.serial_number
        validated_data['name'] = receiving.name
        validated_data['model'] = receiving.model
        validated_data['received_by'] = receiving.received_by
        validated_data['location'] = receiving.location
        validated_data['invoice_number'] = receiving.invoice_number
        validated_data['supplier'] = receiving.supplier
        
        return super().create(validated_data)



class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'  # You can specify specific fields if needed
        
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'  # You can specify specific fields if needed