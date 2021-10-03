from django.forms import ModelForm
from django import forms
from .models import Revenue, Expend, Labour, History


class RevenueForm(ModelForm):
    class Meta:
        model = Revenue
        fields = ['PriceAmount','PayerName', 'UnitNumber','Doc']

        widgets = {
            'PriceAmount': forms.TextInput(attrs={'class': 'form-control', 'rows': 1, 'autocomplete':"off"}),
            'PayerName': forms.Textarea(attrs={'class': 'form-control', 'rows': 1,'autocomplete':"on"}),
            'UnitNumber': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
        }

class ExpendForm(ModelForm):
    class Meta:
        model = Expend
        fields = ['PriceAmount','Supplier','Doc']

        widgets = {
            'PriceAmount': forms.TextInput(attrs={'class': 'form-control', 'rows': 1 , 'autocomplete':"off"}),
            'Supplier': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),

       }


class LabourForm(ModelForm):
    class Meta:
        model = Labour
        fields = ['PriceAmount','LabourName']

        widgets = {
            'PriceAmount': forms.TextInput(attrs={'class': 'form-control', 'rows': 1, 'autocomplete':"off"}),
            'LabourName': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
        }

class HistoryForm(ModelForm):
    class Meta:
        model = History
        fields = ['From_Date', 'Until_Date']

        widgets = {
            'From_Date': forms.SelectDateWidget(),
            'Until_Date': forms.SelectDateWidget(),
        }