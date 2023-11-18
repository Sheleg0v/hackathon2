from django.contrib import admin

from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('rfid', 'first_name', 'last_name', 'middle_name', 'employee_id', 'role', 'phone')


admin.site.register(User, UserAdmin)