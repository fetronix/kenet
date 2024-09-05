from django.contrib import admin
from .models import Consignment, Location, Category, Receiving, Asset, Dispatch
from .forms import *

@admin.register(Consignment)
class ConsignmentAdmin(admin.ModelAdmin):
    list_display = ('slk_id', 'supplier', 'quantity', 'location', 'datetime', 'invoice_number', 'get_received_by_full_name', 'project')
    search_fields = ('slk_id', 'supplier', 'invoice_number', 'project')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')

@admin.register(Receiving)
class ReceivingAdmin(admin.ModelAdmin):
    list_display = (
        'consignment', 'status', 'serial_number', 'description', 'name', 
        'model', 'category', 'supplier', 'get_received_by_full_name', 'invoice_number', 'location'
    )
    search_fields = ('serial_number', 'name', 'description', 'supplier', 'invoice_number')
    list_filter = ('status', 'category')
    # Removed 'status' from readonly_fields
    list_editable= ('status',)
    readonly_fields = ('supplier', 'get_received_by_full_name', 'invoice_number', 'location')


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    form = AssetForm  # Use the custom form
    list_display = (
        'receiving', 'tag_number', 'description', 'serial_number',
        'name','status', 'model', 'get_received_by_full_name', 'location', 'invoice_number', 'supplier'
    )
    search_fields = ('tag_number', 'description', 'serial_number', 'name', 'model')
    readonly_fields = ('description', 'serial_number', 'name', 'model', 'get_received_by_full_name', 'location', 'invoice_number', 'supplier')
    list_editable= ('status',)

@admin.register(Dispatch)
class DispatchAdmin(admin.ModelAdmin):
    list_display = ('asset', 'get_user_full_name', 'get_approver_full_name', 'status','location', 'datetime', 'destination')
    search_fields = ('asset__tag_number', 'user__username', 'approver__username')
    readonly_fields = ('get_user_full_name', 'get_approver_full_name')
    list_editable= ('status',)
    # Ensure 'status' is editable by not including it in readonly_fields



