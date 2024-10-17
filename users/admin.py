from django.contrib import admin
from django.contrib import admin
from .models import User, Profile
# Register your models here.


# Customizing User Admin
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'is_staff')  # Fields to display in the list view
    search_fields = ('email', 'username')  # Fields to search
    list_filter = ('is_staff', 'is_superuser')  # Filters available in the admin

# Customizing Profile Admin
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'user__username', 'address', 'country')  # Fields to display in the list view
    search_fields = ('user__email', 'address')  # Searching by related user fields

# Registering models with the custom admin classes
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)