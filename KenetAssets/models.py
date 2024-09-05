from django.core.exceptions import ValidationError
from django.db import models, IntegrityError
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Max

# Set timezone to Kenyan time (EAT)
import pytz
KENYA_TIME_ZONE = pytz.timezone('Africa/Nairobi')

class Location(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Consignment(models.Model):
    id = models.AutoField(primary_key=True)
    slk_id = models.CharField(max_length=20, unique=True, blank=True, editable=False)  # Make slk_id uneditable
    supplier = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now)
    invoice_number = models.CharField(max_length=100, blank=True, null=True)
    invoice = models.FileField(upload_to='invoices/', blank=True, null=True)
    received_by = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.TextField(blank=True, null=True)
    project = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slk_id:
            last_slk = Consignment.objects.aggregate(Max('id'))['id__max']
            new_id = 1 if last_slk is None else last_slk + 1
            self.slk_id = f'SLK{new_id:03}'
        super().save(*args, **kwargs)

    def get_received_by_full_name(self):
        if self.received_by:
            return f"{self.received_by.first_name} {self.received_by.last_name}"
        return "N/A"

    def __str__(self):
        return self.slk_id

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Receiving(models.Model):
    STATUS_CHOICES = [
        ('testing', 'Testing'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    ]
    
    consignment = models.ForeignKey(Consignment, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    serial_number = models.CharField(max_length=255)
    description = models.TextField()
    name = models.CharField(max_length=255, blank=True, null=True)  # Auto-populated
    model = models.CharField(max_length=255, blank=True, null=True)  # Auto-populated
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # Auto-populated
    supplier = models.CharField(max_length=255, blank=True, null=True)  # New field
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # New field
    invoice_number = models.CharField(max_length=255, blank=True, null=True)  # New field
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)  # Auto-populated
    
    class Meta:
        unique_together = ('serial_number', 'consignment')

    def save(self, *args, **kwargs):
        # Check if the serial_number already exists in the database
        if Receiving.objects.filter(serial_number=self.serial_number).exclude(pk=self.pk).exists():
            raise ValidationError(f"An item with the serial number '{self.serial_number}' already exists.")
        
        if self.consignment:
            self.supplier = self.consignment.supplier
            self.received_by = self.consignment.received_by
            self.invoice_number = self.consignment.invoice_number
            self.location = self.consignment.location

        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            # Handle the unique constraint violation here
            raise ValidationError(f"An item with the serial number '{self.serial_number}' already exists for this consignment.")

    def get_received_by_full_name(self):
        if self.received_by:
            return f"{self.received_by.first_name} {self.received_by.last_name}"
        return "N/A"

    def __str__(self):
        return self.serial_number

class Asset(models.Model):
    STATUS_CHOICES = [
        ('in_use', 'In Use'),
        ('available', 'Available'),
        ('maintenance', 'Maintenance'),
        ('decommissioned', 'Decommissioned'),
    ]
    
    receiving = models.ForeignKey(Receiving, on_delete=models.CASCADE, related_name='assets')
    tag_number = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)  # Auto-populated
    serial_number = models.CharField(max_length=255, blank=True, null=True)  # Auto-populated
    name = models.CharField(max_length=255, blank=True, null=True)  # Auto-populated
    model = models.CharField(max_length=255, blank=True, null=True)  # Auto-populated
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')  # Editable status
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Auto-populated
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)  # Auto-populated
    invoice_number = models.CharField(max_length=255, blank=True, null=True)  # Auto-populated
    supplier = models.CharField(max_length=255, blank=True, null=True)  # Auto-populated

    class Meta:
        unique_together = ('serial_number', 'receiving')

    def save(self, *args, **kwargs):
        # Ensure validation is called before saving
        if self.receiving:
            self.description = self.receiving.description
            self.serial_number = self.receiving.serial_number
            self.name = self.receiving.name
            self.model = self.receiving.model
            self.received_by = self.receiving.received_by
            self.location = self.receiving.location
            self.invoice_number = self.receiving.invoice_number
            self.supplier = self.receiving.supplier

        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            # Handle the unique constraint violation here
            raise ValidationError(f"An asset with the serial number '{self.serial_number}' already exists for this receiving.")

    def get_received_by_full_name(self):
        if self.received_by:
            return f"{self.received_by.first_name} {self.received_by.last_name}"
        return "N/A"

    def __str__(self):
        return self.tag_number

class Dispatch(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('dispatched', 'Dispatched'),
        ('delivered', 'Delivered'),
    ]
    
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='dispatches')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dispatches')
    approver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approvals')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    datetime = models.DateTimeField(default=timezone.now)
    comments = models.TextField(blank=True, null=True)
    destination = models.CharField(max_length=255, blank=True, null=True)  # New field
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)  # Auto-populated

    def save(self, *args, **kwargs):
        # Auto-populate the location from the asset if it's not already set
        if self.asset and not self.location:
            self.location = self.asset.location

        super().save(*args, **kwargs)

    def get_user_full_name(self):
        if self.user:
            return f"{self.user.first_name} {self.user.last_name}"
        return "N/A"

    def get_approver_full_name(self):
        if self.approver:
            return f"{self.approver.first_name} {self.approver.last_name}"
        return "N/A"

    def __str__(self):
        return f"Dispatch {self.asset.tag_number} by {self.user.username}"
