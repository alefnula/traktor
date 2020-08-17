from django.urls import path

from traktor.views.api.v0 import api


urlpatterns = [
    # Project
    path("projects/", api.ProjectListCreate.as_view()),
    path("projects/<slug:project_id>/", api.ProjectGetUpdateDelete.as_view()),
    # Task
    path("projects/<slug:project_id>/tasks/", api.TaskListCreate.as_view()),
    path(
        "projects/<slug:project_id>/tasks/<slug:task_id>/",
        api.TaskGetUpdateDelete.as_view(),
    ),
    # Timer
    path("timer/start/<slug:project_id>/", api.timer_default_start),
    path("timer/start/<slug:project_id>/<slug:task_id>/", api.timer_start),
    path("timer/stop/", api.timer_stop),
    path("timer/status/", api.timer_status),
    path("timer/today/", api.timer_today),
    path("timer/report/", api.timer_report),
]
