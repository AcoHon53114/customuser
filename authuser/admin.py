# authuser/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.hashers import make_password

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        exclude = ('id', 'user_permissions', 'name', 'is_superuser', 'is_staff', 'groups', 'last_login', 'date_joined')  # 排除不需要的字段
        import_id_fields = ('username',)  # 使用 username 作為導入的唯一標識

    def before_import_row(self, row, **kwargs):
        # 在導入之前處理密碼加密
        password = row.get('password')
        if password:
            row['password'] = make_password(password)
        # 確保用戶標記為 is_staff 和 is_active
        row['is_staff'] = True
        row['is_active'] = True

class UserAdmin(BaseUserAdmin, ImportExportModelAdmin):
    resource_class = UserResource  # 指定使用 UserResource

    list_display = ('id', 'username', 'email', 'name', 'resident_id', 'resident_name', 'resident_description',
                    'resident_contact_person', 'resident_contact_phone', 'resident_contact_email', 'resident_contact_relation')
    list_display_links = ('id', 'username', 'email', 'name', 'resident_id', 'resident_name', 'resident_description',
                          'resident_contact_person', 'resident_contact_phone', 'resident_contact_email', 'resident_contact_relation')
    list_filter = ('username', 'email', 'name')
    search_fields = ('username', 'email', 'name', 'resident_id', 'resident_name', 'resident_description',
                     'resident_contact_person', 'resident_contact_phone', 'resident_contact_email', 'resident_contact_relation')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'name', 'resident_id', 'resident_name', 'resident_description',
                                      'resident_contact_person', 'resident_contact_phone', 'resident_contact_email',
                                      'resident_contact_relation')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'resident_id', 'resident_name', 'resident_description',
                       'resident_contact_person', 'resident_contact_phone', 'resident_contact_email', 'resident_contact_relation'),
        }),
    )

    def save_model(self, request, obj, form, change):
        # 在保存用戶時對密碼進行加密處理
        if not change:  # 如果是新增用戶
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        # 在保存表單集時對密碼進行加密處理
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, User) and not change:
                instance.set_password(instance.password)
            instance.save()
        formset.save_m2m()

    def save_related(self, request, form, formsets, change):
        # 在保存相關對象時對密碼進行加密處理
        super().save_related(request, form, formsets, change)
        if not change:  # 如果是新增用戶
            user = form.instance
            user.set_password(user.password)
            user.save()

    def save_form(self, request, form, change):
        # 在保存表單時對密碼進行加密處理
        if not change:  # 如果是新增用戶
            user = form.instance
            user.set_password(user.password)
        return super().save_form(request, form, change)

admin.site.register(User, UserAdmin)  # 确保注册 UserAdmin