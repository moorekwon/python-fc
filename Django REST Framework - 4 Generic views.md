[Django REST framework 공식문서 - Generic views]( https://www.django-rest-framework.org/api-guide/generic-views/  ) 정리본

# Generic views

클래스 기반 뷰

- 재사용 가능한 동작을 작성할 수 있음

- REST framework는 일반적으로 사용되는 패턴을 제공하는 사전에 빌드된 여러 뷰를 제공하여 이를 활용



REST framework에서 제공하는 generic views

- 데이터베이스 모델과 밀접하게 맵핑되는 API 뷰를 신속하게 빌드할 수 있음

- generic view가 API 요구에 맞지 않는 경우

  - `APIView` 클래스를 사용하여 드롭다운하거나, generic view에서 사용하는 mixin과 기본 클래스를 재사용하여 고유의 재사용 가능한 generic view 세트를 구성할 수 있음

- 일반적으로 뷰를 재정의하고 여러 클래스 속성을 설정

  ```python
  from django.contrib.auth.models import User
  from myapp.serializers import UserSerializer
  from rest_framework import generics
  from rest_framework.permissions import IsAdminUser
  
  class UserList(generics.ListCreateAPIView):
      queryset = User.objects.all()
      serializer_class = UserSerializer
      permisson_classes = [IsAdminUser]
  ```

- 더 복잡한 경우, 뷰 클래스에서 다양한 메소드를 대체할 수도 있음

  ```python
  class UserList(generics.ListCreateAPIView):
      queryset = User.objects.all()
      serializer_class = UserSerializer
      permission_classes = [IsAdminUser]
      
      def list(self, request):
          # 'self.queryset' 대신 'get_queryset()' 사용에 주목
          queryset = self.get_queryset()
          serializer = UserSerializer(queryset, many=True)
          return Response(serializer.data)
  ```

- 아주 간단한 경우, `.as_view()` 메소드를 사용하여 클래스 속성을 전달할 수 있음

  ```python
  # URLconf에 항목이 포함될 수 있음
  url(r'^/users/', ListCreateAPIView.as_view(queryset=User.objects.all(), serializer_class=UserSerializer), name='user-list')
  ```



## API Reference(API 참조)

### GenericAPIView

REST framework의 `APIView` 클래스를 확장

- 표준 framework 및 세부적인 뷰에 일반적으로 필요한 동작을 추가
- 제공된 각 구체적인 generic view는 `GenericAPIView`를 하나 이상의 mixin 클래스와 병합하여 빌드됨



#### Attributes

##### Basic settings

기본 뷰 동작을 제어하는 속성

- `queryset`
  - 이 뷰에서 객체를 반환하는데 사용하는 쿼리 집합
  - 일반적으로 이 속성을 설정하거나, `get_queryset() ` 메소드를 대체(override)해야 함
  - 뷰 메소드를 대체하는 경우, 직접 액세스 하는 대신 `get_queryset()`을 호출해야 함
    - `queryset`이 한 번 평가되고, 결과는 모든 후속 요청에 대해 캐시됨
- `serializer_class`
  - 입력의 유효성을 검사 및 역직렬화하고, 출력을 직렬화하는 데 사용하는 직렬화 클래스
  - 일반적으로 이 속성을 설정하거나, `get_serializer_class()` 메소드를 대체해야 함
- `lookup_field`
  - 개별 모델 인스턴스의 객체 조회를 수행하는 데 사용하는 모델 필드
  - 기본값은 `'pk'`
  - 하이퍼링크된 API를 사용할 때, 사용자 지정 값을 사용해야 하는 경우 API 뷰와 serializer 클래스 모두 조회 필드를 설정해야 함
- `lookup_url_kwarg`
  - 객체 조회에 사용하는 URL 키워드 인수
  - URL conf에는 이 값에 해당하는 키워드 인수가 포함되어야 함
  - 설정하지 않으면 기본적으로 `lookup_field`와 동일한 값을 사용



##### Pagination





##### Filtering



#### Methods

##### Basic methods

##### Save and deletion hooks

##### Other methods



## Mixins

### ListModelMixin

### CreateModelMixin

### RetrieveModelMixin

### UpdateModelMixin

### DestroyModelMixin



## Concrete View Classes

### CreateAPIView

### ListAPIView

### RetrieveAPIView

### DestroyAPIView

### UpdateAPIView

### ListCreateAPIView

### RetrieveUpdateAPIView

### RetrieveDestroyAPIView

### RetrieveUpdateDestroyAPIView



## Customizing the generic views(일반 뷰 사용자정의)

### Creating custom mixins(커스텀 mixins 작성)

### Creating custom base classes(사용자정의 기본 클래스 작성)



## PUT as create



## Third party packages

### Django Rest Multiple Models