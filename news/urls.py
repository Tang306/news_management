from django.conf.urls import url
from news import views

urlpatterns = [
    url(r'^news_list$', views.news_list),
    url(r'^get_news_info$', views.get_news_info),
    url(r'^add_news$', views.add_news),
    url(r'^post_news$', views.post_news),
    url(r'^del_news$', views.del_news),
    url(r'^submit_news$', views.submit_news),
    url(r'^examine_news$', views.examine_news),
    url(r'^web_list$', views.web_list),
]