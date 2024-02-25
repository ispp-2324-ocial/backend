from django.test import TestCase
from rest_framework.test import APIRequestFactory
from .models import Chat, Message
from .views import ChatList, ChatDetail, MessageCreate, MessageDelete, ChatCreate, ChatDelete

class ChatDetailTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.chat = Chat.objects.create()
        self.message1 = Message.objects.create(chat=self.chat, content="Hola")
        self.message2 = Message.objects.create(chat=self.chat, content="PRUEBA")
        self.message3 = Message.objects.create(chat=self.chat, content="Real Betis Balompié")

    def test_chat_detail(self):
        view = ChatDetail.as_view()
        request = self.factory.get(f"/chat/{self.chat.id}/")
        response = view(request, pk=self.chat.id)
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data['id'], self.chat.id)
        self.assertEqual(data['messages'], [
            f"{self.message1.id}: {self.message1.content}",
            f"{self.message2.id}: {self.message2.content}",
            f"{self.message3.id}: {self.message3.content}"
        ])

class ChatListTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.chat1 = Chat.objects.create()
        self.chat2 = Chat.objects.create()

    def test_chat_list(self):
        view = ChatList.as_view()
        request = self.factory.get("/chat/list/")
        response = view(request)
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(len(data), 2)  # Verificar que se devuelvan todos los chats

class MessageCreateTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.chat = Chat.objects.create()

    def test_message_create(self):
        view = MessageCreate.as_view()
        request = self.factory.post("/chat/1/create/", {'content': 'New message', 'chat': self.chat.id})
        response = view(request)
        self.assertEqual(response.status_code, 201)
        # Verificar si el mensaje se ha creado correctamente

class ChatCreateTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_chat_create(self):
        view = ChatCreate.as_view()
        request = self.factory.post("/chat/create/", {'id': 1})
        response = view(request)
        self.assertEqual(response.status_code, 201)
        # Verificar si el chat se ha creado correctamente

class MessageDeleteTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.chat = Chat.objects.create()
        self.message = Message.objects.create(chat=self.chat, content="Hello")

    def test_message_delete(self):
        view = MessageDelete.as_view()
        request = self.factory.delete(f"/chat/message/{self.message.id}/delete/")
        response = view(request, pk=self.message.id)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Message.objects.filter(id=self.message.id).exists())

class ChatDeleteTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.chat = Chat.objects.create()

    def test_chat_delete(self):
        view = ChatDelete.as_view()
        request = self.factory.delete(f"/chat/{self.chat.id}/delete/")
        response = view(request, pk=self.chat.id)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Chat.objects.filter(id=self.chat.id).exists())
