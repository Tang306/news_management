from django.conf.urls import url, include

urlpatterns = [
    url(r'^account/api/', include('account.urls')),
    url(r'^news/api/', include('news.urls')),
    # url(r'^logger/api/', include('logger.urls')),

]
