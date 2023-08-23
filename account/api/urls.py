from django.urls import path
from account.api.views import SignupView, UserProfileView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='SignupView'),
    path('update-account/', SignupView.as_view(), name='updateSignupView'),
    path('close-account/<int:pk>/', SignupView.as_view(), name='closeSignupView'),
    path('update-profile/', UserProfileView.as_view(), name='UserProfileView'),
]
