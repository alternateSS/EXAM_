
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from account import views as acc_view
from news import views as news_view
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

acc_router = DefaultRouter()
acc_router.register('register', acc_view.AuthorRegisterAPIView)

news_router = DefaultRouter()
news_router.register('news', news_view.NewsViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="EXAM",
      default_version='v-0.1-Beta',
      description="NO discription",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="ram-kg@mail.ru"),
      license=openapi.License(name="No License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/register', include(acc_router.urls)),
    path('api/account/token', obtain_auth_token),

    path('api/news', include(news_router.urls)),
    # path('api/news/<int:pk>', ),
    path('api/news/<news_id>/comments', news_view.CommentListCreateAPIView.as_view()),
    # path('api/news/<int:news_id>/comments/<pk>', ),

    # path('api/statuses', ),
    # path('api/statuses/<pk>', ),
    # path('api/news/<news_id>/<slug>', ),
    # path('api/news/<news_id>/comments/<comment_id>/<slug>/', )


]
