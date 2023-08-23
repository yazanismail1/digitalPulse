from math import e
from multiprocessing import context
from rest_framework import serializers
from account.api.serializers import CustomUsertwoSerializer
from community.models import Community, Membership


class CommunitySerializer(serializers.ModelSerializer):
    membersCount = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Community
        fields = "__all__"
    
    def get_membersCount(self, obj):
        return obj.members.count()

class CommunityTwoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = "__all__"
    

class MembershipSerializer(serializers.ModelSerializer):
    user = CustomUsertwoSerializer(read_only=True)
    class Meta:
        model = Membership
        fields = "__all__"

class SignleCommunitySerializer(serializers.ModelSerializer):
    membership = serializers.SerializerMethodField(read_only=True)
    membersCount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Community
        exclude = ("members",)
    
    def get_membership(self, obj):
        context = self.context
        communityId = context.get("communityId")
        query = Membership.objects.filter(community=communityId)
        return MembershipSerializer(query, many=True).data
    
    def get_membersCount(self, obj):
        return obj.members.count()
        

