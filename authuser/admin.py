from django.contrib import admin
from .models import User
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class UserResource(resources.ModelResource):
    class Meta:
        model = User

class UserAdmin(ImportExportModelAdmin):
    list_display = ('id', 'email', 'name')  # 使用 User 模型中实际存在的字段
    list_display_links = ('id', 'email', 'name')  # 使用 User 模型中实际存在的字段
    list_filter = ('email', 'name')  # 使用 User 模型中实际存在的字段
    search_fields = ('email', 'name')  # 使用 User 模型中实际存在的字段
    list_per_page = 25
    resource_classes = [UserResource]

admin.site.register(User, UserAdmin)  # 确保注册 UserAdmin