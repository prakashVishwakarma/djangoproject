from django.urls import path
from .views import TaskCreateView

urlpatterns = [
    path('tasks/', TaskCreateView.as_view(), name='task-create'),
    path('get-all-tasks/', TaskCreateView.as_view(), name='get-all-tasks'),
    path('get-by-id/<pk>', TaskCreateView.as_view(), name='get-by-id'),
    path('put-by-id/<pk>', TaskCreateView.as_view(), name='put-by-id'),
    path('patch-by-id/<pk>', TaskCreateView.as_view(), name='patch-by-id'),
]
