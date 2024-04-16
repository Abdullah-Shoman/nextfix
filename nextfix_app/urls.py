from django.urls import path
from . import views


urlpatterns = [
    path('',views.index),
    path('registration',views.registration_form),
    path('login',views.login_form),
    path('logout',views.logout),
    path('shows',views.shows_page),
    path('shows/new',views.add_show),
    path('add',views.create_new_show),
    path('delete/<int:show_id>',views.delete_show),
    path('shows/edit/<int:show_id>',views.edit_show),
    path('edit/<int:show_id>',views.post_edit_show),
    path('shows/<int:show_id>',views.show_details),
    path('post_comment',views.add_show_comment),
    path('delete_show_comment/<int:show_id>/<int:comment_id>',views.delete_show_comment)
]