from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', include('social_django.urls', namespace='social')),
    path('fitting/?id=', views.get_fitting, name='get_fitting'),
    path('fitting/', views.fitting, name='fitting'),
]

# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
