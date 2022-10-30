from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from blog import views

router = routers.DefaultRouter()
router.register('blog', views.BlogViewSet, basename="blog")

schema_view = get_schema_view(
   openapi.Info(
      title="Blogs API",
      default_version='v1-beta',
      description="Blog create description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="chopona09@gmail.com"),
      license=openapi.License(name="No License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/viewset/', include(router.urls)),
    path('api/generics/blog/', views.BlogListCreateView.as_view()),
    path('api/generics/blog/<int:pk>/', views.BlogRetrieveUpdateDeleteView.as_view()),
    path('api/views/blog/', views.BlogViewListCreate.as_view()),
    path('api/views/blog/<int:pk>/', views.BlogViewDetail.as_view()),
    path('api/function/blog/', views.blog_list_create),
    path('api/function/blog/<int:pk>/', views.blog_detail),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),
    path('json-doc/', schema_view.without_ui(cache_timeout=0), name='json-doc'),
]


# urlpatterns = [
#    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
#    ...
# ]