import asyncio
import json

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from channels.exceptions import StopConsumer

class PaymentConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Websocket connect event", event)
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_disconnect(self, event):
        print("Websocket disconnect event", event)
        await self.send({
            'type': 'websocket.close'
        })

        #raise StopConsumer()


    async def websocket_receive(self, event):
        pass
        # print("Received event", event)
        # print(self.scope)
        # comment = event.get('text')
        # new_comment = json.loads(comment)
        #
        # user = self.scope["user"]
        #
        # article_id = self.scope["url_route"]["kwargs"]["id"]
        # article = Article.objects.get(id = article_id)
        #
        # comment_text = new_comment['comment_text']
        #await self.create_comment(user, article, comment_text)

    #
    # @database_sync_to_async
    # def create_payment(self, user, article, comment_text):
    #     Comment.objects.create(user=user, article=article, text = comment_text)
