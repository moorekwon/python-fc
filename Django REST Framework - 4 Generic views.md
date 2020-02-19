[Django REST framework 공식문서 - Generic views]( https://www.django-rest-framework.org/api-guide/generic-views/  ) 정리본

# Generic views

클래스 기반 뷰

- 재사용 가능한 동작을 작성할 수 있음

- REST framework는 일반적으로 사용되는 패턴을 제공하는 사전에 빌드된 여러 뷰를 제공하여 이를 활용



REST framework에서 제공하는 generic views

- 데이터베이스 모델과 밀접하게 맵핑되는 API 뷰를 신속하게 빌드할 수 있음

- generic view가 API 요구에 맞지 않는 경우

  - `APIView` 클래스를 사용하여 드롭다운하거나, generic view에서 사용하는 mixin과 기본 클래스를 재사용하여 고유의 재사용 가능한 generic view 셋를 구성할 수 있음

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

목록 뷰와 함께 사용될 때 페이지매김(pagination)을 제어하는 데 사용되는 속성

- `pagination_class`
  - 목록 결과를 페이지매김할 때 사용하는 클래스
  - 기본값은 `DEFAULT_PAGINATION_CLASS` 설정과 동일한 값(`rest_framework.pagination.PageNumberPagination`)
  - `pagination_class=None`을 설정하면, 이 뷰에서 페이지매김이 비활성화됨



##### Filtering

- `filter_backends`
  - 쿼리셋을 필터링하는 데 사용하는 필터 백엔드 클래스 목록
  - 기본값은 `DEFAULT_FILTER_BACKENDS` 설정과 동일한 값



#### Methods

##### Basic methods

`get_queryset(self)`

- 목록 뷰에 사용하고 상세 뷰에서 조회의 기준으로 사용하는 쿼리 집합을 반환

- `queryset` 속성으로 지정된 쿼리 집합을 반환하도록 기본 설정

- (`self.queryset`에 직접 액세스하는 대신) 항상 사용해야 함

  - `self.queryset`은 한 번만 평가되고 결과는 모든 후속 요청에 대해 캐시됨

- 요청한 사용자에게 고유한 쿼리셋 반환과 같은 동적 동작을 제공하도록 재정의(override) 가능

  ```python
  def get_queryset(self):
      user = self.request.user
      return user.accounts.all()
  ```

  

`get_object(self)`

- 상세 뷰에 사용하는 객체 인스턴스를 반환

- 기본 쿼리셋을 필터링하기 위해 `lookup_field` 매개 변수를 사용하도록 기본 설정

- 둘 이상의 URL kwarg에 기반한 객체 조회 등 보다 복잡한 동작을 제공하도록 재정의 가능

  ```python
  def get_object(self):
      queryset = self.get_queryset()
    fileter = {}
      for field in self.multiple_lookup_fields:
          filter[field] = self.kwargs[field]
          
      obj = get_object_or_404(queryset, **filter)
      self.check_object_permissions(self.request, obj)
      return obj
  ```
  
- API에 객체 수준 권한이 포함되어 있지 않은 경우

  - 선택적으로 `self.check_object_permissions`를 제외하고, `get_object_or_404` 조회에서 객체를 리턴할 수 있음



`filter_queryset(self, queryset)`

- 쿼리셋이 주어지면 사용중인 필터 백엔드로 필터링하여 새 쿼리셋을 리턴

  ```python
  def filter_queryset(self, queryset):
      filter_backends = [CategoryFilter]
      
      if 'geo_route' in self.request.query_params:
          filter_backends = [GeoRouteFilter, CategoryFilter]
      elif 'geo_point' in self.request.query_params:
          filter_backends = [GeoPointFilter, CategoryFilter]
          
      for backend in list(filter_backends):
          queryset = backend().filter_queryset(self.request, queryset, view=self)
          
      return queryset
  ```



`get_serializer_clasS(self)`

- serializer에 사용되는 클래스를 리턴

- `serializer_class` 속성을 반환하도록 기본 설정

- 읽기 및 쓰기 작업에 다른 serializer를 사용하거나, 다른 유형의 사용자에게 다른 serializer를 제공하는 등 동적 동적을 제공하도록 재정의 가능

  ```python
  def get_serializer_class(self):
      if self.request.user.is_staff:
          return FullAccountSerializer
      return BasicAccountSerializer
  ```



##### Save and deletion hooks

mixin 클래스에서 제공되며, 객체 저장 또는 삭제 동작을 쉽게 대체하는 메소드

(더이상 사용할 수 없는) 이전 스타일 버전 2.x `pre.save`, `post_save`, `pre_delete` 및 `post_delete` 메소드를 대체

- `perform_create(self, serializer)`
  - 새 객체 인스턴스를 저장할 때 `CreateModelMixin`에 의해 호출
- `perform_update(self, serializer)`
  - 기존 객체 인스턴스를 저장할 때 `UpdateModelMixin`에 의해 호출
- `perform_destroy(self, instance)`
  - 객체 인스턴스를 삭제할 때 `DestroyModelMixin`에 의해 호출



요청에 암시적이지만 요청 데이터의 일부가 아닌 속성을 설정

- 요청 사용자 또는 URL 키워드인수를 기반으로 객체에 속성을 설정

  ```python
  def perform_create(self, serializer):
      serializer.save(user=self.request.user)
  ```

객체를 저장하기 전후 발생하는 동작을 추가

- 확인 이메일 보내기 또는 업데이트 로깅 등

  ```python
  def perform_update(self, serializer):
      instance = serializer.save()
      send_email_confirmation(user=self.request.user, modified=instance)
  ```

`ValidationError()`을 발생시켜 추가 유효성 검사를 제공

- 데이터베이스 저장 시점에 적용할 유효성 검증 논리가 필요한 경우 유용

  ```python
  def perform_create(self, serializer):
      queryset = SignupRequest.objects.filter(user=self.request.user)
      if queryset.exists():
          raise ValidationError('You have already signed up.')
      serializer.save(user=self.request.user)
  ```



##### Other methods

`GenericAPIView`를 사용하여 커스텀 뷰를 작성하는 경우 호출해야 할 수도 있지만, 일반적으로 대체하지 않아도 되는 메소드

- `get_serializer_context(self)`
  - serializer에 제공해야 하는 추가 컨텍스트가 포함된 사전을 리턴
  - 기본값은 `request`, `view` 및 `format` 키를 포함
- `get_serializer(self, instance=None, data=None, many=False, partial=False)`
  - serializer 인스턴스를 리턴
- `get_paginated_response(self, data)`
  - 페이지매김 스타일 `Response` 객체를 리턴
- `paginate_queryset(self, queryset)`
  - (필요한 경우) 페이지 객체를 리턴 혹은 이 뷰에 페이지매김을 구성하지 않은 경우 `None`을 사용하여 쿼리셋을 페이지매김
- `filter_queryset(self, queryset)`
  - 쿼리셋이 주어지면 사용 중인 필터 백엔드로 필터링하여 새 쿼리셋을 리턴



## Mixins

mixin 클래스

- 기본 뷰 동작을 제공하는데 사용되는 동작을 제공

- `.get()`, `.post()` 같은 핸들러 메소드를 직접 정의하는 대신 조치(action) 메소드를 제공

- 보다 유연한 행동 구성 가능

- `rest_framework.mixins`에서 가져올 수 있음



### ListModelMixin

쿼리셋을 나열하는 `.list(request, *args, **kwargs)` 메소드를 제공

쿼리셋이 채워지면, 응답의 본문으로 쿼리셋의 직렬화된 표현과 함께 `200 OK` 응답을 리턴

응답 데이터는 선택적으로 페이지매김 될 수 있음



### CreateModelMixin

새 모델 인스턴스 작성(create) 및 저장(save)을 구현하는 `.create(request, *args, **kwargs)` 메소드를 제공

객체가 생성되면 객체의 직렬화된 표현을 응답의 본문으로 하여 `201 Created` 응답을 리턴

표현에 `url` 이라는 키가 포함된 경우, `Location` 헤더가 해당 값을 채워짐

객체 작성(create)을 위해 제공된 요청 데이터가 유효하지 않은 경우

- `400 Bad Request` 응답이 리턴
- 오류 세부 사항은 응답 본문으로 리턴



### RetrieveModelMixin

응답으로 기존 모델 인스턴스를 리턴하는 `.retrieve(request, *args, **kwargs)` 메소드를 제공

객체를 검색할 수 있으면 객체의 직렬화된 표현이 응답 본문으로 `200 OK` 응답이 리턴

그렇지 않으면 `404 Not Found` 리턴



### UpdateModelMixin

기존 모델 인스턴스의 업데이트(update) 및 저장(save)을 구현하는 `.update(request, *args, **kwargs)` 메소드를 제공

`.partial_update(request, *args, **kwargs)` 메소드 또한 제공

- 업데이트의 모든 필드가 선택적이라는 점을 제외하고는 `update` 메소드와 유사
- HTTP `PATCH` 요청을 지원할 수 있음

객체가 업데이트되면 객체의 직렬화된 표현이 응답 본문으로 `200 OK` 응답이 리턴

객체 업데이트를 위해 제공된 요청 데이터가 유효하지 않은 경우

- `400 Bad Request` 응답이 리턴
- 오류 세부 사항은 응답 본문



### DestroyModelMixin

기존 모델 인스턴스의 삭제(delete)를 구현하는 `.destroy(request, *args, **kwargs)` 메소드를 제공

객체가 삭제되면 `204 No Content` 응답이 리턴

그렇지 않으면 `404 Not Found` 리턴



## Concrete View Classes

구체적인 generic view

generic view를 사용하는 경우, 일반적으로 심하게 커스텀된 동작이 필요하지 않다면 작업할 레벨

뷰 클래스는 `rest_framework.generics`에서 가져올 수 있음



### CreateAPIView

작성 전용(create-only) 엔드포인트에 사용

`post` 메소드 핸들러를 제공

확장: `GenericAPIView`, `CreateModelMixin`



### ListAPIView

모델 인스턴스의 모음을 나타내기 위해 읽기 전용(read-only) 엔드포인트에 사용

`get` 메소드 핸들러를 제공

확장: `GenericAPIView`, `ListModelMixin`



### RetrieveAPIView

단일 모델 인스턴스를 나타내기 위해 읽기 전용(read-only) 엔드포인트에 사용

`get` 메소드 핸들러를 제공

확장: `GenericAPIView`, `RetrieveModelMixin`



### DestroyAPIView

단일 모델 인스턴스의 삭제 전용(delete-only) 엔드포인트에 사용

`delete` 메소드 핸들러를 제공

확장: `GenericAPIView`, `DestroyModelMixin`



### UpdateAPIView

단일 모델 인스턴스의 업데이트 전용(update-only) 엔드포인트에 사용

`put` 및 `patch` 메소드 핸들러를 제공

확장: `GenericAPIView`, `UpdateModelMixin`



### ListCreateAPIView

모델 인스턴스의 모음을 나타내기 위해 읽기-쓰기(read-write) 엔드포인드에 사용

`get` 및 `post` 메소드 핸들러를 제공

확장: `GenericAPIView`, `ListModelMixin`, `CreateModelMixin`



### RetrieveUpdateAPIView

단일 모델 인스턴스를 나타내기 위해 읽기 또는 업데이트(read or update) 엔드포인트에 사용

`get`, `put` 및 `patch` 메소드 핸들러를 제공

확장: `GenericAPIView`, `RetrieveModelMixin`, `UpdateModelMixin`



### RetrieveDestroyAPIView

단일 모델 인스턴스를 나타내기 위해 읽기 또는 삭제(read or delete) 엔드포인트에 사용

`get` 및 `delete` 메소드 핸들러를 제공

확장: `GenericAPIView`, `RetrieveModelMixin`, `DestroyModelMixin`



### RetrieveUpdateDestroyAPIView

단일 모델 인스턴스를 나타내기 위해 읽기-쓰기-삭제(read-write-delete) 엔드포인트에 사용

`get`, `put`, `patch` 및 `delete` 메소드 핸들러를 제공

확장: `GenericAPIView`, `RetrieveModelMixin`, `UpdateModelMixin`, `DestroyModelMixin`



## Customizing the generic views(일반 뷰 사용자정의)

기존의 일반 뷰를 사용하고 싶지만 약간 맞춤화된 동작을 사용하는 경우가 있음

여러 위치에서 약간의 커스텀된 동작을 다시 사용하는 경우, 동작을 공통 클래스로 리팩토링한 다음 필요에 따라 모든 뷰 또는 뷰셋에 적용할 수 있음

사용해야 하는 커스텀 동작이 있는 경우 커스텀 mixin을 사용하는 것이 좋음



### Creating custom mixins(커스텀 mixins 작성)

URL conf의 여러 필드를 기반으로 객체를 조회해야 하는 경우 mixin 클래스 만들기

```python
class MultipleFieldLookupMixin(object):
    # 임의의 뷰나 뷰셋에 적용되는 mixin
    def get_object(self):
        # 기본 쿼리셋 가져옴
        queryset = self.get_queryset()
        # 모든 필터 백엔드 적용
        queryset = self.filter_queryset(queryset)
        filter = {}
        # 기본 단일 필드 필터링 대신 'lookup_fields' 특성 기반으로 다중 필드 필터링을 얻음
        for field in self.lookup_fields:
            # 빈 필드 무시
            if self.kwargs[field]:
                filter[field] = self.kwargs[field]
        # 객체 검색
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj
```

커스텀 동작을 적용해야 할 때마다 이 mixin을 뷰나 뷰셋에 간단히 적용

```python
class RetrieveUserView(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_fields = ['account', 'username']
```



### Creating custom base classes(커스텀 기본 클래스 작성)

여러 뷰에서 mixin을 사용하는 경우, 프로젝트 전체에서 사용할 수 있는 고유한 기본 뷰셋을 작성할 수 있음

```python
class 
```



## PUT as create



## Third party packages

### Django Rest Multiple Models