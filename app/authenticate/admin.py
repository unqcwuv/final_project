from django.contrib import admin

from .models import User, Company


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'is_company_owner',
        'company',
        'is_active',
        'is_superuser')

    list_display_links = ('id', 'email')

    search_fields = ('username', 'email', 'first_name', 'last_name')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'inn',
        'owner',
        'phone',
        'email'
    )

    list_display_links = ('id', 'title')

    search_fields = ('title', 'inn')