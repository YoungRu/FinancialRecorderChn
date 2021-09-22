from django.contrib import admin
from .models import Revenue, Expend, Labour
# Register your models here.
class DateAdmin(admin.ModelAdmin):
    readonly_fields = ['Date']

admin.site.register(Revenue, DateAdmin)
admin.site.register(Expend, DateAdmin)
admin.site.register(Labour, DateAdmin)