from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Inclusion of "authentication" application URLs
    path("", include('authentication.urls')),
    # URL to access the administration interface
    path("admin/", admin.site.urls),
    # Inclusion of "reviews" application URLs
    path("reviews/", include('reviews.urls')),
]

# Added static URLs for media files in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
