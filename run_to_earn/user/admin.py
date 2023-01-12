from django.contrib import admin
from user.models import User
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'phone', 'created_at', 'updated_at', 'deleted_at')
    list_display_links = ('id', 'email', 'first_name', 'last_name', 'created_at')
    search_fields = ('email', 'first_name', 'last_name',)