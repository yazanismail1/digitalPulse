import re
from rest_framework import status
from django.db import transaction
from rest_framework.response import Response
from account.models import UserProfile
from community.api.serializers import CommunitySerializer, CommunityTwoSerializer, SignleCommunitySerializer
from community.models import Community, Membership
from custom.customClasses import CustomAPIView
from django.db.models import F, ExpressionWrapper, FloatField
from django.db.models.functions import Radians, Sin, Cos, Sqrt


# ---------- CustomUserView ---------- #
class CommunityView(CustomAPIView):
    serializer_class = CommunitySerializer
    model = Community.objects.prefetch_related("members")
    not_allowed_actions = []

class CertainCommunity(CustomAPIView):
    serializer_class = CommunitySerializer
    model = Community.objects.prefetch_related("members")
    not_allowed_actions = []

    def get(self, request, pk):
        try:
            communityId = pk
            community = Community.objects.get(id=communityId)
            serializer = SignleCommunitySerializer(community, context={'communityId': pk})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class CommunitiesInRadius(CustomAPIView):
    serializer_class = CommunitySerializer
    model = Community.objects.prefetch_related("members")
    not_allowed_actions = []

    def get(self, request):
        try:
            user = request.user
            userQuery = UserProfile.objects.get(user=user)
            target_longitude  = userQuery.longitude
            target_latitude  = userQuery.latitude
            radius_km  = request.GET.get("radius")
            earth_radius_km = 6371.0

            target_latitude_rad = Radians(target_latitude)
            target_longitude_rad = Radians(target_longitude)

            delta_latitude = Radians(F('latitude')) - target_latitude_rad
            delta_longitude = Radians(F('longitude')) - target_longitude_rad

            haversine = (Sin(delta_latitude / 2) ** 2 +
             Cos(target_latitude_rad) * Cos(Radians(F('latitude'))) *
             (Sin(delta_longitude / 2) ** 2))
            
            asin_expression = ExpressionWrapper(Sqrt(haversine), output_field=FloatField())
            
            communities_within_radius = Community.objects.annotate(distance=earth_radius_km * 2 * asin_expression
            ).filter(distance__lte=radius_km).order_by('distance')

            serializer = CommunityTwoSerializer(communities_within_radius, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CommunityCRUDView(CustomAPIView):
    serializer_class = CommunitySerializer
    model = Community.objects
    not_allowed_actions = []

    def post(self, request):
        try:
            user = request.user
            data = request.data
            community = self.model.create(
                name=data.get("name"), 
                longitude=data.get("longitude"), 
                latitude=data.get("latitude"),
            )

            Membership.objects.create(
                user=user,
                community=community,
                position="owner"
            )
            serializer = self.serializer_class(community, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        try:
            user = request.user
            data = request.data
            community = Community.objects.get(id=pk)
            if Membership.objects.get(user=user, community=community).position != "owner":
                return Response({'detail': "You are not the owner of this community"}, status=status.HTTP_400_BAD_REQUEST)
            community.name = data.get("name")
            community.longitude = data.get("longitude")
            community.latitude = data.get("latitude")
            community.save()
            return Response({'detail': "updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LeaveCommunityView(CustomAPIView):
    serializer_class = CommunitySerializer
    model = Community.objects
    not_allowed_actions = []

    def patch(self, request, pk):
        try:
            user = request.user
            community = Community.objects.get(id=pk)
            if Membership.objects.get(user=user, community=community).position == "owner":
                community.delete()
                return Response({'detail': "deleted successfully"}, status=status.HTTP_200_OK)
            community.members.remove(user)
            community.save()
            return Response({'detail': "left successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class YourOwnComunities(CustomAPIView):
    serializer_class = CommunitySerializer
    model = Community.objects
    not_allowed_actions = []

    def get(self, request):
        try:
            user = request.user
            memberships = Membership.objects.filter(user=user, position="owner")
            communities = []
            for membership in memberships:
                communities.append(membership.community)
            serializer = self.serializer_class(communities, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class JoinCommunityView(CustomAPIView):
    serializer_class = CommunitySerializer
    model = Community.objects
    not_allowed_actions = []

    def patch(self, request, pk):
        try:
            user = request.user
            community = Community.objects.get(id=pk)
            if Membership.objects.filter(user=user, community=community).exists():
                return Response({'detail': "You are already a member of this community"}, status=status.HTTP_400_BAD_REQUEST)
            Membership.objects.create(
                user=user,
                community=community,
                position="member"
            )
            return Response({'detail': "joined successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)