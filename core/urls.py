from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView
from core.views import MyTokenObtainPairView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('account/', include('account.api.urls')),
    path('community/', include('community.api.urls')),
]
