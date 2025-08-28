from django.urls import path
from . import views as views

app_name = 'tasks'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('task-list/', views.TaskListView.as_view(), name='task_list'),
    path('completed-task-list/', views.CompletedTaskListView.as_view(), name='task_list_complete'),
    path('create-task/', views.CreateTaskView.as_view(), name='task_create'),
    path('update-task/<int:pk>/', views.UpdateTaskView.as_view(), name='task_update'),
    path('complete-task/<int:pk>', views.CompleteTask.as_view(), name='task_complete'),
    path('restore-task/<int:pk>', views.RestoreTask.as_view(), name='task_restore'),
    path('delete-task/<int:pk>/', views.DeleteTaskView.as_view(), name='task_delete'),
]