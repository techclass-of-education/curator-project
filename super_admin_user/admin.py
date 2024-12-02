from django.contrib import admin

from .models import SuperAdmin, AdminUserList

admin.site.register(SuperAdmin)

admin.site.register(AdminUserList)