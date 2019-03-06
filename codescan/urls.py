
from django.urls import path,include
from . import views
urlpatterns = [
    path('add/', views.addtask),
    path('index/',views.index),
    path('task/',views.task),
    path('result/',views.result),
    path('detail/',views.detail),
]
