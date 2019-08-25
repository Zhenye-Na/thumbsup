# -*- coding:utf-8 -*-

from django.urls import path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from thumbsup.messager.consumers import MessagesConsumer
from thumbsup.notifications.consumers import NotificationsConsumer

# self.scope['type'] 获取协议类型
# self.scope['url_route']['kwargs']['username'] 获取url中关键字参数
# channels routing 是 scope 级别的, 一个连接只能由一个 consumer 接收和处理
application = ProtocolTypeRouter({
    # 普通的 HTTP 请求不需要我们手动在这里添加, 框架会自动加载
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path('ws/notifications/', NotificationsConsumer),
                path('ws/<str:username>/', MessagesConsumer),
            ])
        )
    )
})
