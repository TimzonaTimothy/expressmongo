from django.contrib import admin
from .models import *


class CourierAdmin(admin.ModelAdmin):
	list_display = ('tracking_id', 'service_type','content',)
	# change_list_template = 'admin/change_list.html'
	actions = None

class TransactionAdmin(admin.ModelAdmin):
	list_display = ( 'parcel', 'details', 'activity','date')
	list_per_page = 20
	

admin.site.site_header = 'EXPRESS-MONGO-ADMIN'
admin.site.site_title = 'EXPRESS-MONGO-ADMINISTRATION'
admin.site.register(Courier, CourierAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Contact)

