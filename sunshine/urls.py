from django.conf.urls import patterns, include, url
from django.contrib import admin
from registration import urls as registration

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^', include('sunfront.urls')),
    url(r'^', include('spine.urls')),
    url(r'^', include('sajax.urls')),
    url(r'^library/', include('library.urls')),
    url(r'^admin/', include(admin.site.urls)),


    # Registration app URLs

    url(r'^login/$',
        registration.auth_views.login,
        {'template_name': 'registration/login.html'},
        name='auth_login'),

    url(r'^account/activate/(?P<activation_key>\w+)/$',
        registration.activate,
        name='registration_activate'),

    # - password reset

    url(r'^password/reset/$',
        registration.auth_views.password_reset,
        name='auth_password_reset'),

    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        registration.auth_views.password_reset_confirm,
        name='auth_password_reset_confirm'),

    url(r'^password/reset/complete/$',
        registration.auth_views.password_reset_complete,
        name='auth_password_reset_complete'),

    url(r'^password/reset/done/$',
        registration.auth_views.password_reset_done,
        name='auth_password_reset_done'),
)
