from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from traktor.models import User, Project, Task, Entry


def name(s: str):
    def decorator(func):
        func.short_description = s
        return func

    return decorator


class ColoredMixin:
    @name("Color")
    def colored_color(self, obj):
        return obj.html(obj.color)


admin.register(User)(UserAdmin)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin, ColoredMixin):
    list_display = ["name", "user", "colored_color"]
    list_filter = ["user__username"]
    ordering = ["user__username", "name"]
    search_fields = ["user__username", "name"]
    readonly_fields = ("user", "slug", "created_on", "updated_on")
    fieldsets = (
        (None, {"fields": ("user", "name", "slug", "color")}),
        ("Timestamps", {"fields": ("created_on", "updated_on")}),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin, ColoredMixin):
    list_display = ["name", "project_name", "user", "colored_color", "default"]
    list_filter = ["project__user__username"]
    ordering = ["project__user__username", "project__name", "name"]
    search_fields = ["project__user__username", "project__name", "name"]
    readonly_fields = ("user", "slug", "created_on", "updated_on")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "project",
                    "name",
                    "slug",
                    "default",
                    "color",
                )
            },
        ),
        ("Timestamps", {"fields": ("created_on", "updated_on")}),
    )

    @name("User")
    def user(self, obj):
        return obj.project.user

    @name("Project")
    def project_name(self, obj):
        return obj.project.name


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = (
        "task_name",
        "project_name",
        "user",
        "running_time",
        "start_time",
        "end_time",
    )
    list_filter = ["task__project__user__username"]
    ordering = ["-start_time", "task__project__user__username"]
    search_fields = [
        "task__project__user__username",
        "task__project__name",
        "task__name",
    ]
    readonly_fields = (
        "user",
        "project_name",
        "running_time",
        "created_on",
        "updated_on",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "project_name",
                    "task",
                    "description",
                    "notes",
                )
            },
        ),
        ("Timer", {"fields": ("start_time", "end_time", "running_time")}),
        ("Timestamps", {"fields": ("created_on", "updated_on")}),
    )

    @name("User")
    def user(self, obj):
        return obj.task.project.user

    @name("Project")
    def project_name(self, obj):
        return obj.task.project.name

    @name("Task")
    def task_name(self, obj):
        return obj.task.name
