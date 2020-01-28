from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView


urlpatterns = [
    path('timing/', include('timing.urls')),
    path('admin/', admin.site.urls),
    path(r'', RedirectView.as_view(url='/timing/race/'))
]