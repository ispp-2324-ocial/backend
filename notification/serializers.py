from rest_framework import serializers

from .models import Notification, STATUS


class NotificationSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = "__all__"

    def get_author(self, obj):
        return obj.author.name
    
    def get_status(self, obj):
        return STATUS[obj.status][1]

class NotificationCreateSerializer(serializers.Serializer):

    title = serializers.CharField()
    content = serializers.CharField()