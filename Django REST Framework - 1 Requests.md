# Requests

REST framework의 `Request` 클래스

- 표준 HttpRequest를 확장
- REST framework의 유연한 요청 구문 분석 및 인증에 대한 지원을 추가



## Request parsing

REST framework의 Request 오브젝트

- 일반적으로 양식 데이터를 처리하는 것과 동일한 방식
- JSON 데이터 또는 기타 매체 유형으로 요청을 처리할 수 있는 유연한 요청 구문분석(parsing)을 제공



### .data

`request.data`

- 요청 본문의 구문분석된 콘텐츠를 리턴
- 표준 `request.POST` 및 `request.FILES` 속성과 유사
- 표준 `request.POST` 및 `request.FILES` 속성과 다른 부분
  - 파일 및 비파일 입력을 포함해 모든 구문분석된 콘텐츠를 포함
  - POST 외의 HTTP 메소드 콘텐츠 구문분석을 지원
    - PUT 및 PATCH 요청의 콘텐츠에 액세스할 수 있음
  - (양식 데이터만 지원하는 것이 아니라) REST framework의 유연한 요청구문 분석을 지원
    - (들어오는 양식 데이터를 처리하는 것과 같은 방식으로) 들어오는 JSON 데이터를 처리할 수 있음



### .query_params

`request.query_params`

- `request.GET`에 대한 보다 정확한 이름의 동의어
- 코드 내부의 명확성을 위해 Django의 표준 `request.GET` 대신 사용 권장
- 보다 정확하고 명확한 codebase를 유지
- HTTP 메소드 유형에는 `GET` 요청뿐만 아니라 쿼리 매개변수가 포함될 수 있음



### .parsers

`APIView` 클래스 또는 `@api_view` 데코레이터

- 이 속성(property)이 뷰에 설정된 `parser_classes` 또는 `DEFAULT_PARSER_CLASSES` 설정에 따라 `Parser` 인스턴스 목록으로 자동 설정되도록 함
- 일반적으로 이 속성에 액세스할 필요는 없음
- 클라이언트가 잘못된 콘텐츠를 보낸 경우, `request.data`에 액세스하면 `ParseError` 발생
  - 기본적으로 오류를 포착하고 `400 Bad Request` 응답을 리턴
- 클라이언트가 구문분석할 수 없는 콘텐츠 유형을 요청을 보낸 경우, `UnsupportedMedialType` 예외 발생
  - 이 예외는 기본적으로 잡히고 `415 Unsupported Media Type` 응답을 리턴



## Content negotiaion(콘텐츠 협상)

요청은 콘텐츠 협상 단계의 결과를 판별할 수 있는 일부 특성을 노출

다른 매체 유형에 대해 다른 직렬화(serialization) 체계를 선택하는 등의 동작을 구현할 수 있음



### .accepted_renderer

콘텐츠 협상 단계에서 선택된 renderer 인스턴스



### .accepted_media_type

콘텐츠 협상 단계에서 승인한 미디어 유형을 나타내는 문자열



## Authentication(입증)

REST framework는 유연한 요청당 인증을 제공

- API의 다른 부분마다 다른 인증 정책을 사용
- 여러 인증 정책 사용을 지원
- 수신 요청과 관련된 사용자와 토큰 정보 모두 제공



### .user

`request.user`

- 일반적으로 `django.contrib.auth.models.User`의 인스턴스를 리턴
- 동작은 사용 중인 인증 정책에 따라 다름
- 요청이 인증되지 않은 경우, 기본값은 `django.contrib.auth.models.AnonymousUser`의 인스턴스



### .auth

`request.auth`

- 추가 인증 컨텍스트를 리턴
- 정확한 동작은 사용 중인 인증 정책에 따라 다름
- 일반적인 동작은 요청이 인증된 토큰의 인스턴스(일 수 있음)
- 요청이 인증되지 않았거나 추가 컨텍스트가 없는 경우, 기본값은 `None`



### .authenticators

`APIView` 클래스 또는 `@api_view` 데코레이터

- 이 속성이 뷰에 설정된 `authentication_classes` 또는 `DEFAULT_AUTHENTICATORS` 설정에 따라 `Authentication` 인스턴스 목록으로 자동 설정되도록 함
- 일반적으로 이 속성에 액세스할 필요는 없음
- `.user` 또는 `.auth` 속성을 호출할 때, `WrappedAttributeError` 발생할 수 있음
  - 인증자에서 표준 `AttributeError`로 발생
  - 외부 속성 액세스로 인해 오류가 억제되지 않도록 다른 예외 유형으로 다시 발생해야 함
  - 파이썬은 `AttributeError`가 인증자에서 비롯된 것을 인식하지 못하고, 대신 요청 객체에 `.user` 또는 `.auth` 속성이 없다고 가정
  - 인증자는 수정되어야 함



## Browser enhancements(브라우저 향상)

REST framework는 브라우저 기반 `PUT`, `PATCH` 및 `DELETE` 양식과 같은 몇가지 브라우저 개선 사항을 지원



### .method

`request.method`

- 요청의 HTTP 메소드의 **대문자** 문자열 표현을 리턴
- 브라우저 기반 `PUT`, `PATCH` 및 `DELETE` 양식을 투명하게 지원



### .content_type

`request.content_type`

- HTTP 요청 본문의 미디어 유형을 나타내는 문자열 객체 또는 (미디어 유형이 제공되지 않은 경우) 빈 문자열을 리턴
- 일반적으로 요청의 콘텐츠 유형에 직접 액세스할 필요 없음
  - 일반적으로 REST framework의 기본 요청 구문분석 동작에 의존
- 요청의 콘텐츠 유형에 직접 액세스해야 하는 경우, `request.META.get('HTTP_CONTENT_TYPE')`을 사용하는 것보다 `.content_type` 특성을 사용해야 함
  - 브라우저 기반 비형식(non-form) 콘텐츠에 대한 투명한 지원을 제공



### .stream

`request.stream`

- 요청 본문의 내용을 나타내는 스트림을 리턴
- 일반적으로 요청의 콘텐츠에 직접 액세스할 필요 없음
  - 일반적으로 REST framework의 기본 요청 구문분석 동작에 의존



## Standard HttpRequest attributes(표준 HttpRequest 속성)

REST framework의 `Request`

- Django의 `HttpRequest`를 확장
- 다른 모든 표준 속성 및 메소드도 사용 가능
- `request.META` 및 `request.session` 사전 등을 정상적으로 사용할 수 있음
- (구현 이유 때문에) `HttpRequest` 클래스에서 상속되지 않고, composition을 사용하여 클래스를 확장