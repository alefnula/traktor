from rest_framework import serializers

from traktor.engine import engine
from traktor.models import Project, Task, Entry
from traktor.serializers.validators import color_validator

# Colored


class ColoredCreateSerializer(serializers.Serializer):
    color = serializers.CharField(max_length=7, validators=[color_validator])


class ColoredUpdateSerializer(serializers.Serializer):
    color = serializers.CharField(
        max_length=7,
        validators=[color_validator],
        required=False,
        allow_null=True,
    )

    def update(self, instance, validated_data):
        color = validated_data.get("color", None)
        if color is not None:
            instance.color = color


# Project


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.slug

    class Meta:
        model = Project
        fields = ["id", "name", "color", "created_on", "updated_on"]


class ProjectCreateSerializer(ColoredCreateSerializer):
    name = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return engine.project_create(**validated_data)


class ProjectUpdateSerializer(ColoredUpdateSerializer):
    name = serializers.CharField(
        max_length=255, required=False, allow_null=True
    )


# Task


class TaskSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    def get_project(self, obj):
        return obj.project.slug

    def get_id(self, obj):
        return obj.slug

    class Meta:
        model = Task
        fields = [
            "project",
            "id",
            "name",
            "color",
            "default",
            "created_on",
            "updated_on",
        ]


class TaskCreateSerializer(ColoredCreateSerializer):
    name = serializers.CharField(max_length=255)
    default = serializers.BooleanField(default=False, required=False)


class TaskUpdateSerializer(ColoredUpdateSerializer):
    name = serializers.CharField(
        max_length=255, required=False, allow_null=True
    )
    default = serializers.BooleanField(
        default=False, required=False, allow_null=True
    )


# Entry


class EntrySerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()
    task = serializers.SerializerMethodField()
    running_time = serializers.SerializerMethodField()

    def get_project(self, obj) -> str:
        return obj.project.slug

    def get_task(self, obj) -> str:
        return obj.task.slug

    def get_running_time(self, obj) -> str:
        return obj.running_time

    class Meta:
        model = Entry
        fields = [
            "project",
            "task",
            "description",
            "notes",
            "start_time",
            "end_time",
            "duration",
            "running_time",
            "created_on",
            "updated_on",
        ]


# Report


class ReportSerializer(serializers.Serializer):
    project = serializers.CharField()
    task = serializers.CharField()
    duration = serializers.IntegerField()
    running_time = serializers.CharField()
