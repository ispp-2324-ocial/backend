from rest_framework import serializers

from .models import Notification, STATUS


class NotificationSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = "__all__"

    def get_author(self, obj):
        return obj.author.username
    
    def get_status(self, obj):
        return STATUS[obj.status][1]