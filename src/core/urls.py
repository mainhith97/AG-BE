from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
  url(r'^admin/', admin.site.urls),
  url(r'^', include(('api.router', 'api'), namespace='v1')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
