from djangochannelsrestframework import permissions
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import ListModelMixin
from djangochannelsrestframework.observer import model_observer

from .models import Notification
from .serializers import NotificationSerializer


class NotificationConsumer(ListModelMixin, GenericAsyncAPIConsumer):

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permissions = (permissions.AllowAny,) #cambiar

    async def connect(self, **kwargs):
        await self.model_change.subscribe()
        await super().connect()

    @model_observer(Notification)
    async def model_change(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @model_change.serializer
    def model_serialize(self, instance, action, **kwargs):
        return dict(data=NotificationSerializer(instance=instance).data, action=action.value)