from django import forms
from .models import Asset, Receiving

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = '__all__'  # Include all fields in the form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter the receiving field to show only approved items
        self.fields['receiving'].queryset = Receiving.objects.filter(status='approved')
