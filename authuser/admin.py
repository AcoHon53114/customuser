# authuser/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class UserResource(resources.ModelResource):
    class Meta:
        model = User

class UserAdmin(BaseUserAdmin, ImportExportModelAdmin):
    list_display = ('id', 'username', 'email', 'name')  # 使用 User 模型中实际存在的字段
    list_display_links = ('id', 'username', 'email', 'name')  # 使用 User 模型中实际存在的字段
    list_filter = ('username', 'email', 'name')  # 使用 User 模型中实际存在的字段
    search_fields = ('username', 'email', 'name')  # 使用 User 模型中实际存在的字段
    list_per_page = 25
    resource_classes = [UserResource]

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    def save_model(self, request, obj, form, change):
        # 确保密码被正确哈希处理
        if obj.pk:
            orig_obj = User.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(User, UserAdmin)  # 确保注册 UserAdmin