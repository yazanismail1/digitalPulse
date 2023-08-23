from django.urls import include, path

from community.api.views import CertainCommunity, CommunitiesInRadius, CommunityCRUDView, CommunityView, JoinCommunityView, LeaveCommunityView, YourOwnComunities

urlpatterns = [
    path('get-all/', CommunityView.as_view(), name='CommunityView'),
    path('get-community/<int:pk>/', CertainCommunity.as_view(), name='CertainCommunity'),
    path('near-community/', CommunitiesInRadius.as_view(), name='CommunitiesInRadius'),
    path('create-community/', CommunityCRUDView.as_view(), name='CommunityCRUDView'),
    path('update-community/<int:pk>/', CommunityCRUDView.as_view(), name='CommunityCRUDViewUpdate'),
    path('leave-community/<int:pk>/', LeaveCommunityView.as_view(), name='LeaveCommunityViewLeave'),
    path('own-communities/', YourOwnComunities.as_view(), name='YourOwnComunities'),
    path('join-community/<int:pk>/', JoinCommunityView.as_view(), name='JoinCommunityView'),
]