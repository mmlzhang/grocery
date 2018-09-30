from django.contrib import admin

from user.models import Permission, Role, User, UserProfile


class PermisssionAdmin(admin.ModelAdmin):
    list_display = ('id', 'p_hans', 'p_en')
    ordering = ('id',)
    search_fields = ('p_hans',)  # 搜索


admin.site.register(Permission, PermisssionAdmin)


class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'name_en')
    ordering = ('id',)
    search_fields = ('name',)  # 搜索


admin.site.register(Role, RoleAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'ticket', 'delete', 'role')
    ordering = ('id',)
    search_fields = ('username',)  # 搜索


admin.site.register(User, UserAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'website', 'picture')
    ordering = ('id',)


admin.site.register(UserProfile, UserProfileAdmin)




