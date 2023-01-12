from django.contrib import admin
from user.models import User, RefreshTokens, VerificationOTP, Goal
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'phone', 'created_at', 'updated_at', 'deleted_at')
    list_display_links = ('id', 'email', 'first_name', 'last_name', 'created_at')
    search_fields = ('email', 'first_name', 'last_name',)

@admin.register(RefreshTokens)
class RefreshTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'refreshToken']
    readonly_fields = ['user', 'refreshToken', 'issued']


@admin.register(VerificationOTP)
class VerificationOTPAdmin(admin.ModelAdmin):
    list_display = ['user', 'otp']
    readonly_fields = ['user', 'otp', 'created_at']

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['user', 'goal']
    readonly_fields = ['user', 'goal']