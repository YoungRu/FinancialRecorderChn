from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Revenue(models.Model):
    PriceAmount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    UnitNumber = models.CharField(max_length=10, null=True, blank=True)
    PayerName = models.CharField(max_length=100, null=True, blank=True)
    Doc = models.ImageField(null=True, upload_to='proof/',blank=True)
    Time = models.TimeField(auto_now_add=True)
    DateTime = models.DateTimeField(auto_now_add=True, null=True)
    Date = models.DateField(auto_now_add=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default='1')

    def __str__(self):
        return self.PayerName

class Expend(models.Model):
    PriceAmount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Supplier = models.CharField(max_length=50, blank=True)
    Doc = models.FileField(null=True, upload_to='proof/', blank=True)
    Time = models.TimeField(auto_now_add=True)
    DateTime = models.DateTimeField(auto_now_add=True, null=True)
    Date = models.DateField(auto_now_add=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default='1')

    def __str__(self):
        return str(self.Supplier)

class Labour(models.Model):
    PriceAmount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    LabourName = models.CharField(max_length=50, blank=True)
    Time = models.TimeField(auto_now_add=True)
    DateTime = models.DateTimeField(auto_now_add=True, null=True)
    Date = models.DateField(auto_now_add=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default='1')

    def __str__(self):
        return str(self.LabourName)