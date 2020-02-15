# Responses

REST framework의 `Response` 클래스

- 클라이언트 요청에 따라 여러 콘텐츠 유형으로 렌더링 될 수 있는 콘텐츠를 리턴

- Django의 `SimpleTemplateResponse`를 서브클래스함
- `Response` 객체는 데이터로 초기화되며, 기본 파이썬 프리미티브로 구성돼야 함
- REST framework는 표준 HTTP 콘텐츠 협상을 사용해 최종 응답 콘텐츠를 렌더링하는 방법을 결정
- `Response` 클래스를 사용할 필요는 없으며, 필요한 경우 뷰에서 일반 `HttpResponse` 또는 `StreamingHttpResponse` 객체를 반환할 수도 있음
- 콘텐츠 협상 웹 API 응답을 리턴하기 위한 더 좋은 인터페이스를 제공하고, 여러 형식으로 렌더링 될 수 있음
- (REST framework를 심하게 사용자 정의하지 않는 한) 항상 `Response` 객체를 리턴하는 뷰를 위한 `APIView` 클래스 또는 `@api_view` 함수를 사용해야 함
- 뷰는 콘텐츠 협상을 수행하고 뷰에서 리턴되기 전에 응답에 적합한 renderer을 선택할 수 있음



## Creating responses(응답 만들기)

### Response()

`Response(data, status=None, template_name=None, headers=None, content_type=None)`

- (일반 `HttpResponse` 객체와 달리) 렌더링된 내용으로 `Response` 객체를 인스턴스화 하지 않고, 대신 (파이썬 프리미티브로 구성될 수 있는) 렌더링되지 않은 데이터를 전달
- `Response` 객체를 만들기 전에 데이터를 기본 데이터 유형으로 직렬화 해야 함
  - `Response` 클래스가 사용하는 renderer는 Django 모델 인스턴스와 같은 복잡한 데이터 유형을 기본적으로 처리할 수 없음
  - REST frameowrk의 `Serializer` 클래스를 사용해  데이터 직렬화 수행하거나 고유한 사용자 정의 직렬화 사용
- 인수
  - `data`: 응답에 대한 직렬화된 데이터
  - `status`: 응답의 상태 코드. 기본값은 200
  - `template_name`: `HTMLRenderer`을 선택한 경우 사용할 템플릿 이름
  - `headers`: 응답에 사용할 HTTP 헤더의 사전(dictionary)
  - `content_type`: 응답의 콘텐츠 유형
    - 일반적으로 콘텐츠 협상에 따라 renderer에서 자동으로 설정됨
    - 콘텐츠 유형을 명시적으로 지정해야 하는 경우도 있음



## Attrbutes(속성)

### .data

렌더링되지 않은 일련의 응답 데이터



### .status_code

HTTP 응답의 숫자 상태 코드



### .content

응답의 렌더링된 콘텐츠

`.render()` 메소드를 호출하여 액세스



### .template_name

`HTMLRenderer` 또는 다른 사용자 정의 템플릿 renderer가 응답에 허용되는 rendere인 경우에만 필요



### .accepted_renderer

응답을 렌더링 하는데 사용되는 renderer 인스턴스

응답이 뷰에서 리턴되기 직전에 `APIView` 또는 `@api_view`에 의해 자동으로 설정



### .accepted_media_type

콘텐츠 협상 단계에서 선택한 미디어 유형 응답

응답이 뷰에서 리턴되기 직전에 `APIView` 또는 `@api_view`에 의해 자동으로 설정



### .renderer_context

renderer의 `.render()` 메소드에 전달될 추가 컨텍스트 정보 사전

응답이 뷰에서 리턴되기 직전에 `APIView` 또는 `@api_view`에 의해 자동으로 설정



## Standard HttpResponse attributes(표준 HttpResponse 속성)

`Response` 클래스는 `SimpleTemplateResponse`를 확장하여 모든 일반 속성 및 메소드도 응답에서 사용 가능



표준 방식으로 응답에 헤더를 설정

```django
response = Response()
response['Cache-Control'] = 'no-cache'
```



### .render()

`.render()`

- (`TemplateResponse`와 마찬가지로) 응답의 직렬화된 데이터를 최종 응답 콘텐츠로 렌더링하기 위해 호출
- 호출될 때, 응답 콘텐츠는 `accepted_renderer` 인스턴스에서 `.render(data, accepted_media_type, renderer_context)` 메소드를 호출한 결과로 설정
- 일반적으로 직접 호출할 필요는 없음
  - Django의 표준 응답 주기에 의해 처리