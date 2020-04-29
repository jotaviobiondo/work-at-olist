from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers

from library.views import AuthorViewSet, BookViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Library API",
        default_version='v1',
        description="Authors and books REST API",
    ),
    public=True,
)

router = routers.DefaultRouter()
router.register(r'api/authors', AuthorViewSet)
router.register(r'api/books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui(cache_timeout=0)),
]
