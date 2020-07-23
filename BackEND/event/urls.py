from django.urls import path
from . import views

urlpatterns =[
    path('details/<slug>/', views.detail),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('create/', views.create, name="create"),
    path('edit/<slug>', views.edit),
    path('delete/<slug>', views.delete),

    # --------------------api path-------------------

    path('get_schedule/<slug>', views.get_schedule),
    path('put_schedule/<slug>', views.put_schedule),
    path('del_schedule/<slug>', views.del_schedule),
    path('post_schedule/', views.post_schedule),
    path('get_all_event/', views.get_all_event),
]

