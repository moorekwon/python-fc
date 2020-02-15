# Views

## Class-based Views(클래스 기반 뷰)

REST framework의 `APIView` 클래스

- Django의 `View` 클래스를 서브클래스로 하는 클래스
- 일반 `View` 클래스와 다른 방식
  - 핸들러 메소드에 전달된 요청은 DJango의 ` HttpRequest` 인스턴스가 아니라 REST framework의 `Request` 인스턴스
  - 핸들러 메소드는 Django의 `HttpResponse` 대신 REST framework의 `Response`를 리턴할 수 있음
    - 뷰는 콘텐츠 협상을 관리하고 응답에 올바른 renderer을 설정
  - 모든 `APIException` 예외가 포착되어 적절한 응답으로 중재됨
  - 들어오는 요청이 인증되고, 요청을 핸들러 메소드로 디스패치하기 전에 적절한 권한 and/or 스로틀 검사가 실행됨 

- 일반적인 `View` 클래스를 사용하는 것과 거의 동일

- 일반적으로 들어오는 요청은 `.get()` 또는 `.post()`와 같은 적절한 핸들러 메소드로 전달

- API 정책의 다양한 측면을 제어하는 많은 속성이 클래스에 설정될 수 있음

  ```python
  from rest_framework.views import APIView
  from rest_framework.responses import Response
  from rest_framework import authentication, permissions
  from django.contrib.auth.models import User
  
  class ListUsers(APIView):
      # 시스템의 모든 user를 표시
      # 토큰 인증 필요
      # admin user만 뷰에 액세스할 수 있음
  	authentication_classes = [authentication.TokenAuthentication]
      permission_classes = [permissions.IsAdminUser]
      
      def get(self, request, format=None):
          # 모든 user의 목록을 리턴
          usernames = [user.username for user in User.objects.all()]
          return Response(usernames)
  ```



Django REST Framework의 `APIView`, `GenericAPIView`, 다양한 `Mixins` 및 `Viewsets` 간 전체 메소드, 속성 및 관계는 초기에 복잡 할 수 있음



### API policy attributes(API 정책 속성)

API 뷰의 플러그가능한 측면을 제어하는 속성

- `.renderer_classes`
- `.parser_classes`
- `.authentication_classes`
- `.throttle_classes`
- `.permission_classes`
- `.content_negotiation_class`



### API policy instantiation methods(API 정책 인스턴스화 방법)

다양한 플러그가능한 API 정책을 인스턴스화 하기 위해 REST framework에서 사용되는 메소드

일반적으로 재정의할 필요는 없음

- `.get_renderers(self)`
- `.get_parsers(self)`
- `.get_authenticators(self)`
- `.get_throttles(self)`
- `.get_permissions(self)`
- `.get_content_negotiator(self)`
- `.get_exception_handler(self)`



### API policy implementation methods(API 정책 구현 방법)

핸들러 메소드로 디스패치하기 전에 호출되는 메소드

- `.check_permissions(self, request)`
- `.check_throttles(self, request)`
- `.perform_content_negotiatioin(self, request, force=False)`



### Dispatch methods

뷰의 `.dispatch()` 메소드에 의해 직접 호출되는 메소드

`.get()`, `.post()`, `.put()`, `.patch()` 및 `.delete()`와 같은 핸들러 메소드를 호출하기 전 또는 후에 발생하는 모든 조치를 수행

- `.initial(self, request, *args, **kwargs)`
  - 핸들러 메소드가 호출되기 전에 발생해야 하는 조치를 수행
  - 권한 및 제한(throttling)을 시행하고, 콘텐츠 협상을 수행하는 데 사용
  - 일반적으로 재정의할 필요는 없음
- `.handle_exception(self, exc)`
  - 핸들러 메소드에 의해 발생된 예외가 전달되어 `Response` 인스턴스를 리턴하거나 예외를 다시 발생시킴
  - 기본 구현은 `rest_framework.exceptions.APIException`의 하위 클래스와 Django의 `Http404` 및 `PermissionDenied` 예외를 처리하고, 적절한 오류 응답을 리턴
  - 오류 응답을 사용자 정의해야 하는 경우, API가 이 메소드를 서브클래스로 리턴
- `.initialize_request(self, request, *args, **kwargs)`
  - 핸들러 메소드에 전달된 요청 객체가 일반적은 Django `HttpRequest`가 아닌 `Request`의 인스턴스인지 확인
  - 일반적으로 재정의할 필요는 없음
- `.finalize_response(self, request, response, *args, **kwargs)`
  - 핸들러 메소드에서 리턴된 `Response` 객체가 (콘텐츠 협상에 의해 결정된대로) 올바른 콘텐츠 유형으로 렌더링 되도록 함
  - 일반적으로 재정의할 필요는 없음



## Function Based Views(함수 기반 뷰)

REST framework

- 일반 함수 기반 뷰로 작업할 수도 있음
- 함수 기반 뷰를 래핑하여 (일반적인 Django `HttpRequest` 대신) `Request` 인스턴스를 수신하고 (Django `HttpRequest` 대신) `Response`를 리턴하도록 하는 간단한 데코레이터 세트를 제공
- 요청 처리 방법을 구성할 수 있음



```python

```



### @api_view()

`@api_view(http_method_names=['GET'])`

- 핵심은 `api_view` 데코레이터
- 뷰가 응답해야 하는 HTTP 메소드 목록을 가져옴



데이터를 수동으로 리턴하는 뷰 작성

```python
from rest_framework.decorators import api_view

@api_view()
def hello_world(request):
    return Response({"message": "Hello, world!"})
```

- setttings에 지정된 기본 renderer, 파서, 인증 클래스 등을 사용
- 기본적으로 `GET` 메소드만 허용 (다른 메소드는 "405 Method Not Allowed"로 응답)



뷰가 허용하는 메소드를 지정

```python
@api_view(['GET', 'POST'])
def hello_world(request):
    if request.method == 'POST':
        return Response({"message": "Got some data!", "data": request.data})
    return Response({"message": "Hellow, world!"})
```



### API policy decorators(API 정책 데코레이터)

REST framework

- 기본 설정을 재정의하기 위해 뷰에 추가할 수 있는 추가 데코레이터 세트를 제공
- `@api_view` 데코레이터 뒤(아래)에 와야 함
- 사용가능한 데코레이터 (하나의 인수를 취하고, 리스트 또는 튜플이어야 함)
  - `@renderer_classes(...)`
  - `@parser_classes(...)`
  - `@authentication_classes(...)`
  - `@throttle_classes(...)`
  - `@permission_classes(...)`



스로틀을 사용하여 뷰 작성

```python
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import UserRateThrottle

# 특정 사용자가 하루에 한 번만 호출
class OncePerDayUserThrottle(UserRateThrottle):
    rate = '1/day'
    
@api_view(['GET'])
# @throttle_classes 데코레이터를 사용하여 스로틀 클래스 목록을 전달
@throttle_classes([OncePerDayUserThrottle])
def view(request):
    return Response({"message": "Hello for today! See you tomrrow!"})
```

- `APIView` 서브클래스에 설정된 속성에 해당하는 데코레이터



### View schema decorator

`@schema` 데코레이터

- 함수 기반 뷰의 기본 스키마 생성을 무시할(override) 수 있음
- `@api_view` 데코레이터 뒤(아래)에 와야 함



```python
from rest_framework.decorators import api_view, schema
from rest_framework.schemas import AutoSchema

class CustomAutoSchema(AutoSchema):
    def get_link(self, path, method, base_url):
        # 뷰 내부검사를 무시
        
@api_view(['GET'])
@schema(CustomAutoSchema())
def view(request):
    return Response({"message": "HEllow for today! See you tomorrow!"})
```

- 단일 `AutoSchema` 인스턴스, `AutoSchema` 하위 클래스 인스턴스 또는 `ManualSchema` 인스턴스를 사용하는 데코레이터
- 스키마 생성에서 뷰를 제외하기 위해 `None`을 전달할 수 있음