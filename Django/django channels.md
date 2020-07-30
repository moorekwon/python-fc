```python
import json
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
```

- 모든 연결을 수락하고 클라이언트에서 메시지를 수신한 다음 해당 메시지를 동일한 클라이언트로 다시 에코하는 동기식 WebSocket consumer

- 같은 방에 있는 다른 클라이언트에게 메시지를 브로드캐스트하지 않음



채널은 성능 향상을 위해 비동기 consumer 작성을 지원

모든 비동기 consumer는 Django 모델 액세스와 같은 직접 차단 작업을 수행하지 않도록 주의



```python
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # consumer에 대한 WebSocket 연결을 연 chat/routing.py의 URL 경로에서
        # 'room_name' 매개 변수를 가져옴
        # 모든 consumer는 연결에 대한 정보를 포함하는 범위를 가지고 있음
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        
        # 인용하거나 이탈하지 않고 사용자가 지정한 회의실 이름에서 직접 채널 그룹 이름을 구성
        # 그룹 이름에는 문자, 숫자, 하이픈 및 마침표만 포함 가능
        # 다른 문자가 있는 회의실 이름에서 실패
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        # ChatConsumer가 동기 WebsocketConsumer이지만 비동기 채널 계층 메소드를 호출
        # async_to_sync(…) 랩퍼 필요
        # 모든 채널 레이어 방법은 비동기식
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        # WebSocket 연결 수락
        # connect() 메서드 내에서 accept()를 호출하지 않으면 연결이 거부되고 닫힘
        # 연결을 수락하도록 선택한 경우 connect()의 마지막 작업으로 accept()를 호출하는 것이 좋음
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        # 이벤트에는 이벤트를 받는 consumer에서 호출해야 하는 메서드 이름에 해당하는 특수한 'type'키 존재
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
```

- 사용자가 메시지를 게시하면 JavaScript 함수가 WebSocket을 통해 메시지를 ChatConsumer로 전송
- ChatConsumer는 해당 메시지를 수신하여 회의실 이름에 해당하는 그룹으로 전달
- 동일한 그룹 (및 같은 방)에 있는 모든 ChatConsumer는 그룹으로부터 메시지를 수신하여 WebSocket을 통해 JavaScript로 다시 전달하여 채팅 로그에 추가



ChatConsumer를 비동기식으로 다시 작성

```python
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
```

- ChatConsumer는 이제 WebsocketConsumer가 아닌 AsyncWebsocketConsumer에서 상속
- 모든 메소드는 단순한 def가 아닌 비동기 def(async def)

- await는 I/O를 수행하는 비동기 함수를 호출하는 데 사용
- 채널 계층에서 메소드를 호출할 때 async_to_sync가 더 이상 필요하지 않음