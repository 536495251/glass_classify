"""
URL configuration for glass_classify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
import app.views

urlpatterns = [
    # path("admin/", admin.site.urls),
    path('', app.views.upload),
    path('upload/', app.views.upload, name='upload'),
    path('index/', app.views.index, name='index'),
    path('train_model/', app.views.train_model, name='train_model'),
    path('model_predict/', app.views.model_predict, name='model_predict'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
