from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'partners.views.index'),
    url(r'^search/', 'partners.views.search'),
    url(r'^load_products/', 'partners.views.load_products'),
    url(r'^login/', 'partners.views.login'),
    url(r'^user_info/', 'partners.views.user_info'),
    url(r'^logout/', 'partners.views.logout'),
    url(r'^register/', 'partners.views.register'),
    url(r'^profile', 'partners.views.profile'),
    url(r'^register_contact/', 'partners.views.register_contact'),
    url(r'^admin/', include(admin.site.urls)),
)
