from django.conf.urls import url
from account import views

urlpatterns = [
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^reset$', views.reset),
    url(r'^change$', views.change),
    url(r'^user_edit$', views.user_edit),
    url(r'^user_delete$', views.user_delete),
    url(r'^user_list$', views.user_list),
    # url(r'^register_supper$', views.register_supper),
]