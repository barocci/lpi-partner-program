from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'partners.views.index'),
    url(r'^search/', 'partners.views.search'),
    url(r'^load_products/', 'partners.views.load_products'),
    url(r'^login/', 'partners.views.login'),
    url(r'^user_info/', 'partners.views.user_info'),
    url(r'^account_info/', 'partners.views.account_info'),
    url(r'^logout/', 'partners.views.logout'),
    url(r'^subscribe/', 'partners.views.subscribe'),
    url(r'^profile/', 'partners.views.profile'),
    url(r'^edit_profile/', 'partners.views.edit_profile'),
    url(r'^register/', 'partners.views.register'),
    url(r'^details/', 'partners.views.details'),
    url(r'^hook/', 'partners.views.hook'),
    url(r'^avatar_upload/', 'partners.views.avatar_upload'),
    url(r'^change_password/', 'partners.views.change_password'),
    url(r'^template/', 'partners.views.template'),
    url(r'^register_contact/', 'partners.views.register_contact'),
    url(r'^attach_contact/', 'partners.views.attach_contact'),
    url(r'^contratto/', 'partners.views.contract'),
    url(r'^admin/', include(admin.site.urls)),
)
