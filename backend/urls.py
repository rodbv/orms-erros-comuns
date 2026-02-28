from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
]


# Add Silk URLs if enabled
if "silk" in settings.INSTALLED_APPS:
    urlpatterns.append(path("silk/", include("silk.urls", namespace="silk")))

# Add Django Debug Toolbar URLs if enabled
if "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
