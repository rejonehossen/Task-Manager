# Created by Rejone Hossen | Premium Task Manager | 2025

from django.contrib import admin
from .models import CustomUser, Category, Tag, Task, SharedList
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html


# ⭐ Premium Custom Admin for User
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_premium', 'theme', 'created_at', 'profile_picture_preview')
    list_filter = ('is_premium', 'theme', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = UserAdmin.fieldsets + (
        ("Extra Info", {
            "fields": ('profile_picture', 'bio', 'theme', 'is_premium', 'created_at', 'updated_at')
        }),
    )

    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="40" height="40" style="border-radius: 50%;" />', obj.profile_picture.url)
        return "-"
    profile_picture_preview.short_description = "Profile"


# 🎯 Premium Task Admin
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'priority_colored', 'completed', 'due_date', 'is_overdue', 'category', 'created_at')
    list_filter = ('priority', 'completed', 'category', 'tags')
    search_fields = ('title', 'description')
    list_editable = ('completed',)
    autocomplete_fields = ['category', 'tags']
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    def priority_colored(self, obj):
        colors = {'H': 'red', 'M': 'orange', 'L': 'green'}
        return format_html(
            '<strong style="color:{};">{}</strong>',
            colors.get(obj.priority, 'gray'),
            obj.get_priority_display()
        )
    priority_colored.short_description = '🔥 Priority'


# 📦 Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'color_display')
    search_fields = ('name',)
    list_filter = ('user',)

    def color_display(self, obj):
        return format_html(
            '<span style="background-color:{}; padding: 2px 8px; border-radius:5px;">{}</span>',
            obj.color,
            obj.color
        )
    color_display.short_description = "Color"


# 🏷️ Tag Admin
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name',)
    list_filter = ('user',)


# 🤝 Shared List Admin with Inline Tasks
class TaskInline(admin.TabularInline):
    model = SharedList.tasks.through
    extra = 1

@admin.register(SharedList)
class SharedListAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'collaborator_count', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('owner',)
    inlines = [TaskInline]
    filter_horizontal = ('collaborators', 'tasks')
    readonly_fields = ('created_at',)

    def collaborator_count(self, obj):
        return obj.collaborators.count()
    collaborator_count.short_description = "👥 Collaborators"



