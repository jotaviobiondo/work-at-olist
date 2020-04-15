from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from library.views import AuthorViewSet

router = routers.DefaultRouter()
router.register(r'api/authors', AuthorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
