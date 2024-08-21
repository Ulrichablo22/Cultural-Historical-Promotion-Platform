from django.contrib import admin
from api.models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role']


class ProfileAdmin(admin.ModelAdmin):
    list_editable = ['verified']
    list_display = ['user', 'full_name' ,'verified']

admin.site.register(User, UserAdmin)
admin.site.register( Profile,ProfileAdmin)
admin.site.register(Lieu)
admin.site.register(Evenement)
admin.site.register(Avis)
admin.site.register(Media)

