from django.forms import ModelForm
from django import forms
from .models import Revenue
from .models import Expend
from .models import Labour

class RevenueForm(ModelForm):
    class Meta:
        model = Revenue
        fields = ['PriceAmount','PayerName', 'UnitNumber','Doc']

class ExpendForm(ModelForm):
    class Meta:
        model = Expend
        fields = ['PriceAmount','Supplier','Doc']

class LabourForm(ModelForm):
    class Meta:
        model = Labour
        fields = ['PriceAmount','LabourName']