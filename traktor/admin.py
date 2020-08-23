from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from traktor.models import User, Project, Task, Entry


class ColoredMixin:
    def colored_name(self, obj):
        return obj.html(obj.name)

    colored_name.short_description = "Name"


def name(s: str):
    def decorator(func):
        func.short_description = s
        return func

    return decorator


admin.register(User)(UserAdmin)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin, ColoredMixin):
    list_display = ("colored_name",)
    ordering = ["name"]
    search_fields = ["name"]
    readonly_fields = ("slug", "created_on", "updated_on")
    fieldsets = (
        (None, {"fields": ("name", "slug", "color")}),
        ("Timestamps", {"fields": ("created_on", "updated_on")}),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin, ColoredMixin):
    list_display = ("project_name", "colored_name", "default")
    ordering = ["project__name", "name"]
    search_fields = ["project__name", "name"]
    readonly_fields = ("slug", "created_on", "updated_on")
    fieldsets = (
        (None, {"fields": ("project", "name", "slug", "default", "color")}),
        ("Timestamps", {"fields": ("created_on", "updated_on")}),
    )

    @name("Project")
    def project_name(self, obj):
        return obj.project.html(obj.project.name)


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = (
        "project_name",
        "task_name",
        "running_time",
        "start_time",
        "end_time",
    )
    ordering = ["-start_time"]
    search_fields = ["project__name", "task__name"]
    readonly_fields = (
        "running_time",
        "created_on",
        "updated_on",
    )
    fieldsets = (
        (None, {"fields": ("project", "task", "description", "notes")}),
        ("Timer", {"fields": ("start_time", "end_time", "running_time")}),
        ("Timestamps", {"fields": ("created_on", "updated_on")}),
    )

    @name("Project")
    def project_name(self, obj):
        return obj.project.html(obj.project.name)

    @name("Task")
    def task_name(self, obj):
        return obj.task.html(obj.task.name)
