# -*- coding:utf-8 -*-

import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationsConsumer(AsyncWebsocketConsumer):
    """处理通知应用中的 WebSocket 请求"""

    async def connect(self):
        """建立连接"""
        if self.scope['user'].is_anonymous:
            # 未登录用户拒绝连接
            await self.close()
        else:
            await self.channel_layer.group_add('notifications', self.channel_name)
            await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        """将接收到的消息返回给前端"""
        await self.send(text_data=json.dumps(text_data))

    async def disconnect(self, code):
        """断开连接"""
        await self.channel_layer.group_discard('notifications', self.channel_name)
