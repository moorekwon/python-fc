

# 쿼리 만들기

데이터 모델 생성

- Django는 자동으로 데이터베이스 생성 API를 제공

- 객체를 생성, 검색, 업데이트 및 삭제 가능



웹 로그 애플리케이션 구성

```python
from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()
    
    def __str__(self):
        return self.name
    
class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    
    def __str(self):
        return self.name
    
class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    number_of_comments = models.IntegerField()
    number_or_pingbacks = models.IntegerField()
    rating = models.IntegerField()
    
    def __str__(self):
        return self.headline
```



## 객체 생성

Django

- Python 객체에서 데이터베이스 테이블 데이터를 나타내기 위해 직관적인 시스템을 사용
- 모델 클래스는 데이터베이스 테이블, 해당 클래스의 인스턴스는 데이터베이스 테이블의 특정 레코드를 나타냄



객체 생성

1. 객체를 인스턴스화: 모델 클래스에 키워드 인수를 사용
   
2. `save()`: 데이터베이스에 저장하도록 호출



mysite

- blog

  - models.py

    ```shell
    >>> from blog.models import Blog
    >>> b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
    >>> b.save()
    ```

    - 이면에서 `INSERT` SQL 문을 수행
    - `create()`: 단일 관계에서 객체를 생성하고 저장



## 객체 변경사항 저장

`save()`

- 데이터베이스에 이미 있는 객체에 변경 사항을 저장

  ```shell
  # 지정된 Blog 인스턴스 b5가 이미 데이터베이스에 저장
  # 이름을 변경하고 데이터베이스에 그 기록을 갱신
  >>> b5.name = 'New name'
  >>> b5.save()
  ```

  - 이면에서 `UPDATE` SQL 문을 수행
  - Django는 명시적으로 `save()`를 호출할 때까지 데이터베이스에 충돌하지 않음



### ForeignKey와 ManytoManyField 필드 저장

`ForeignKey` 필드 업데이트

- 일반 필드를 저장하는 것과 정확히 같은 방식으로 작동

- Entry와 Blog의 적절한 인스턴스가 이미 데이터베이스에 저장되어 있다고 가정하여, Entry 인스턴스 entry의 blog 속성을 업데이트

  ```shell
  >>> from blog.models import Blog, Entry
  >>> entry = Entry.objects.get(pk=1)
  >>> cheese_blog = Blog.objects.get(name="Cheddar Talk")
  >>> entry.blog = cheese_blog
  >>> entry.save()
  ```



`ManyToMany` 필드 업데이트

- 약간 다른 방식으로 작동

- 필드에서 `add()` 메소드 사용하여 관계에 레코드를 추가

- Author 인스턴스 joe를 entry 오브젝트에 추가

  ```shell
  >>> from blog.models import Author
  >>> joe = Author.objects.craete(naem="Joe")
  >>> entry.authors.add(joe)
  ```

- `add()` 호출에 여러 인수를 포함하여 여러 레코드를 한 번에 추가

  ```shell
  >>> john = Author.objects.create(name="John")
  >>> paul = Author.objects.create(name="Paul")
  >>> george = Author.objects.create(name="George")
  >>> ringo = Author.objects.create(name="Ringo")
  >>> entry.authors.add(john, paul, george, ringo)
  ```



## 객체 검색(조회)

QuerySet

- 데이터베이스의 개체 모음

- (데이터베이스에서 객체를 검색하기 위해) 모델 클래스의 `Manager`를 통하여 구성
  - 모델의 `Manager`를 사용하여 QuerySet을 얻음
  - 각 모델에는 하나 이상의 `Manager`가 있으며, 기본적으로 개체(object) 라고 함
- SQL에서 `SELECT` 문과 같음

필터

- 0개, 1개, 혹은 2개 이상의 필터를 가질 수 있음
- SQL에서 `WHERE` 또는 `LIMIT`과 같은 제한 절



`Manager`

- 모델의 주요 QuerySet 소스

- 모델 인스턴스가 아닌 모델 클래스를 통해서만 액세스 할 수 있음
  - "table-level" 작업과 "record-level" 작업을 분리하기 위해

```shell
>>> Blog.objects
# <django.db.models.manager.Manager object at ...>
>>> b = Blog(name='Foo', tagline='Bar')
>>> b.objects
# Traceback:
#     ...
# AttributeError: "Manager isn't accessible via Blog instances."
```

- `Blog.objects.all()`은 데이터베이스의 모든 Blog 객체가 포함된 QuerySet을 리턴



### 모든 객체 검색

모든 객체 얻기

- 테이블에서 객체를 검색하는 가장 간단한 방법

- `Manager`에서 `all()` 메소드 사용
- 데이터베이스에 있는 모든 object의 QuerySet을 리턴
- 리턴된 QuerySet은 데이터베이스 테이블의 모든 object를 설명

```shell
>>> all_entries = Entry.objects.all()
```



### 필터를 사용하여 특정 객체 검색

전체 개체 집합의 하위 집합만 선택

- (하위 집합을 만들기 위해) 필터 조건을 추가하여 초기 QuerySet을 세분화(구체화)

- QuerySet을 세분화하는 일반적인 방법

  1. `filter(**kwargs)`

     - 주어진 조회 매개변수(**kwargs)와 일치하는 객체를 포함하는 새로운 QuerySet을 리턴

       ```python
       # 2006년부터 blog entry들의 QuerySet 가져오기
       Entry.objects.filter(pub_date__year=2006)
       
       # 기본 관리자 클래스 사용
       Entry.objects.all().filter(pub_date__year=2006)
       ```

  2. `exclude(**kwargs)`

     - 주어진 조회 매개변수(`**kwargs`)와 일치하지 않는 객체를 포함하는 새로운 QuerySet을 리턴



#### 체인 필터

QuerySet을 세분화한 결과는 QuerySet 자체

- 세분화를 함께 연결할 수 있음

```shell
# 2005년 1월 30일과 현재 날짜 사이에 "What"으로 시작하는 제목이 있는 모든 entry들을 포함하는 QuerySet

# 데이터베이스에 있는 모든 entry들의 초기 QuerySet을 가져 와서 필터를 추가
>>> Entry.objects.filter(
	headline__startswith='What'
# 제외
).exclude(
	pub_date__gte=datetime.date.today()
# 필터
).filter(
	pub_date__gte=datetime.date(2005, 1, 30)
)
```



#### 필터링된 `QuerySet`은 고유하다

QuerySet을 세분화할 때마다 이전 QuerySet에 바인딩되지 않은 완전히 새로운 QuerySet을 얻음

각 세분화는 저장, 사용 및 재사용 할 수 있는 별도의 고유한 QuerySet을 작성

```shell
# 세 QuerySet은 분리되어 있음

# "What"으로 시작하는 headline을 포함하는 모든 entry들을 포함하는 기본 QuerySet
# 세분화 프로세스의 영향을 받지 않음
>>> q1 = Entry.objects.filter(headline__startswith="What")

# 첫 번째의 하위 집합
# pub_date가 오늘 또는 미래인 레코드를 제외
>>> q2 = q1.exclude(pub_date__gte=datetime.date.today())

# 첫 번째의 하위 집합
# pub_date가 오늘 또는 미래인 레코드만 선택
>>> q3 = q1.filter(pub_date__gte=datetime.date.today())
```



#### `QuerySet`들은 게으르다

QuerySet을 만드는 것은 데이터베이스 활동과 관련이 없음

Django는 QuerySet이 평가될 때까지 실제로 쿼리를 실행하지 않음

```shell
>>> q = Entry.objects.filter(headline__startswith="What")
>>> q = q.filter(pub_date__lte=datetime.date.today())
>>> q = q.exclude(body_text__icontains="food")

# 실제로 한 번만 데이터베이스에 적중
>>> print(q)
```

- 일반적으로 QuerySet의 결과는 "요청"할 때까지 데이터베이스에서 가져오지 않음
- "요청"하면 데이터베이스에 액세스하여 QuerySet이 평가



### `get()`로 단일 객체 검색

`filter()`

- 모든 쿼리 표현식을 사용할 수 있음

- 단일 객체만 쿼리와 일치하더라도 QuerySet을 항상 제공
  - 단일 요소를 포함하는 QuerySet이 됨

`get()`

- 모든 쿼리 표현식을 사용할 수 있음

- 쿼리와 일치하는 객체가 하나만 있는 경우 사용

- `Manager`에서 객체를 직접 반환

  ```shell
  # 기본 키가 1인 Entry 객체가 없으면 Django는 Entry.DoesNotExist를 발생시킴
  >>> one_entry = Entry.objects.get(pk=1)
  ```

- `[0]` 슬라이스로 `filter()`를 사용하는 것과 차이
  - 쿼리와 일치하는 결과가 없으면 `DoesNotExist` 예외 발생
    - 이 예외는 쿼리가 수행되는 모델 클래스의 속성
  - 둘 이상의 항목이 get() 쿼리와 일치하면 `MultipleObjectsReturned` 예외 발생
    - 이 예외는 모델 클래스 자체의 속성



### 다른 `QuerySet` 방법

대부분의 경우 데이터베이스에서 객체를 찾을 때 사용하는 QuerySet 메소드

- `all()`
- `get()`
- `filter()`
- `exclude()`



### 제한 `QuerySet`들

QuerySet을 슬라이스

- Python의 배열 분할 구문의 하위 집합을 사용하여 QuerySet을 특정 개수의 결과로 제한

- SQL에서 `LIMIT` 및 `OFFSET` 절과 같음

  ```shell
  # 처음 5개의 객체를 반환 (LIMIT 5)
  >>> Entry.objects.all()[:5]
  
  # 6번째부터 10번째 개체를 반환(OFFSET 5 LIMIT 5)
  >>> Entry.objects.all()[5:10]
  ```

- 음수 인덱싱은 지원되지 않음

- 일반적으로 새 QuerySet이 반환되며, 쿼리를 평가하지 않음

  - Python 슬라이스 구문의 "step" 매개 변수를 사용하는 경우는 예외

    ```shell
    # 처음 10의 모든 두번째 객체 목록을 반환하기 위해 실제로 쿼리를 실행
    >>> Entry.objects.all()[:10:2]
    ```

- 슬라이스된 QuerySet의 추가 필터링 또는 순서는 작동 방식의 모호한 특성으로 인해 금지

- (목록이 아닌) 단일 객체를 검색하려면 슬라이스 대신 인덱스를 사용

  ```shell
  # headline 기준으로 알파벳순으로 entry들을 정렬한 후, 데이터베이스의 첫번째 Entry를 반환
  >>> Entry.objects.order_by('headline')[0]
  
  # 첫번째는, IndexError 발생
  # 두번째는, 지정된 기준과 일치하는 개체가 없으면 DoesNotExist 발생
  >>> Entry.objects.order_by('headline')[0:1].get()
  ```



### 필드 조회

SQL에서 `WHERE` 절의 meat를 지정하는 방법

QuerySet 메소드 `filter()`, `exclude()` 및 `get()`에 키워드 인수로 지정됨

기본 조회 키워드 인수는 `field__lookuptype=value` 형식을 사용

```shell
>>> Entry.objects.filter(pub_date__lte='2006-01-01')
```

```sql
# SQL로 변환
SELECT * FROM blog_entry WHERE pub_date <= '2006-01-01';
```



Python의 키워드 인수

- 런타임에 이름과 값이 평가되는 임의의 이름-값 인수를 허용하는 함수를 정의할 수 있음



조회에 지정된 필드

- 모델 필드의 이름이어야 함

- `ForeignKey`의 경우

  - `_id` 접미사로 필드 이름을 지정할 수 있음

  - value 매개 변수는 외부 모델 기본 키의 원시 값을 포함해야 함

  ```shell
  >>> Entry.objects.filter(blog_id=4)
  ```

  - 잘못된 키워드 인수를 전달하면 조회 함수가 `TypeError`을 발생



데이터베이스 API는 약 24가지 조회 유형을 지원

자주 사용되는 조회

- `exact`

  ```shell
  >>> Entry.objects.get(headline__exact="Cat bites dog")
  ```

  ```sql
  # SQL로 변환
  SELECT ... WHERE headline = 'Cat bites dog';
  ```

  - 조회 유형을 제공하지 않은 경우(키워드 인수에 이중 밑줄이 없는 경우), 조회 유형은 `exact`로 간주됨

    ```shell
    # 동일한 문장
    >>> Blog.objects.get(id__exact=14)
    >>> Blog.objects.get(id=14)
    ```

- `iexact`

  - 대소문자를 구분하지 않음

    ```shell
    # "Beatles Blog" 또는 "BeAtlES blOG" 라는 제목의 Blog와도 일치
    >>> Blog.objects.get(name__iexact="beatles blog")
    ```

- `contains`

  - 대소문자를 구분함

    ```shell
    # 'Today Lennon honored'와 일치하지만 'today lennon honored'와는 일치하지 않음
    >>> Entry.objects.get(headline__contains='Lennon')
    ```

    ```sql
    # SQL로 변환
    SELECT ... WHERE headline LIKE '%Lennon%';
    ```

  - 대소문자를 구분하지 않는 `icontains`도 있음

- `startswith`, `endswith`

  - 검색으로 시작 및 종료
  - 대소문자를 구분하지 않는 `istartswith`, `iendswith`도 있음



### 관계에 걸친 조회

Django

- 자동으로 SQL `JOIN`을 관리

- 조회에서 관계를 "따르는" 강력하고 직관적인 방법을 제공



관계 확장

- 원하는 필드에 도달할 때까지 모델에서 관련 필드의 필드 이름을 이중 밑줄로 구분하여 사용
- 원하는만큼 깊을 수 있음

```shell
# 이름이 'Beatles Blog'인 Blog를 가진 모든 Entry 오브젝트를 검색
>>> Entry.objects.filter(blog__name='Beatles Blog')
```

"역방향" 관계 참조

- 거꾸로도 작동
- 모델의 소문자 이름을 사용

```shell
# headline에 'Lennon'이 포함된 하나 이상의 Entry가 있는 모든 Blog 오브젝트를 검색
>>> Blog.objects.filter(entry__headline__contains='Lennon')
```

- 여러 관계를 필터링하고 중간 모델 중 하나에 필터 조건을 충족하는 값이 없는 경우

  - Django는 비어 있지만(모든 값이 NULL) 유효한 객체가 있는 것으로 처리
  - 이것은 오류가 발생하지 않는다는 것

  ```shell
  # (관련 Author 모델이 있는 경우) entry와 관련된 author가 없는 경우, 그 없는 author로 인해 오류가 발생하지 않고, 대신 첨부된 이름도 없는 것으로 간주
  >>> Blog.objects.filter(entry__authors__name='Lennon')
  
  # isnull을 사용
  # author의 이름이 비어있는 Blog 객체와 entry의 author가 비어있는 Blog 객체를 반환
  >>> Blog.objects.filter(entry__authors__name__isnull=True)
  
  # entry의 author가 비어있는 Blog 객체를 원하지 않는 경우
  >>> Blog.ojbects.filter(entry__authors__isnull=False, entry__authors__name__isnull=True)
  ```



#### 다중 값 관계 스패닝

`ManyToManyField` 또는 역 `ForeignKey` 기준으로 개체를 필터링

- Blog/Entry 관계를 고려 (Blog to Entry는 일대다 관계)
- 단일 Blog와 연관된 entry들이 여러 개 있음
  - 제목에 "Lennon"이 있고 2008년에 출판된 entry가 있는 blog들 찾기
  - 제목에 "Lennon"이 있는 entry와 2008년에 출판된 entry가 있는 blog들 찾기
- Entry에 tags 라는 `ManyToManyField`가 있는 경우
  - "music"과 "bands" 라는 tags에 연결된 entry들 찾기
  - 이름이 "music"이고 상태가 "public"인 태그를 포함하는 entry 찾기



(두 가지 상황을 처리하기 위해) Django는 일관된 `filter()` 호출 처리 방법을 갖고 있음

- 단일 `filter()` 호출 내의 모든 것이 동시에 적용되어 모든 해당 요구 사항과 일치하는 항목을 필터링

- 연속적인 `filter()` 호출은 객체 집합을 추가로 제한

  - 그러나 **다중 값 관계**의 경우, 기본 모델에 연결된 모든 객체에 적용 (반드시 이전 `filter()` 호출에 의해 선택된 객체는 아님)

  ```shell
  # 제목에 "Lennon"이 있고 2008년에 게시된 entry들이 포함된 모든 blog들 찾기 (두 조건을 모두 만족하는 동일한 enrty)
  >>> Blog.objects.filter(
  	entry__headline__contains='Lennon',
  	entry__pub_date__year=2008
  )
  ```

  ```shell
  # 제목에 "Lennon"이 있는 entry와 2008년에 게시된 entry가 포함된 모든 blog들 찾기
  >>> Blog.objects.filter(
  	# 첫번째 필터
  	# heandline에서 "Lennon"이 있는 entry들에 연결된 모든 blog로 제한
  	entry__headline__contains='Lennon'
  ).filter(
  	# 두번째 필터
  	# 2008년에 게시된 entry들에 연결된 blog들로 더욱 제한
  	# 선택된 entry들은 첫번째 필터의 entry들과 같거나 같지 않을 수 있음
  	entry__pub_date__year=2008
  )
  ```

  - "Lennon"을 포함하는 entry들과 2008년의 entry들이 각각 있지만, 2008년의 "Lennon"을 포함하는 entry들이 없는 blog가 하나만 있는 경우
    - `entry__headline__contains='Lennon'`: blog를 반환하지 않음
    - `entry__pub_date__year=2008`: 해당 blog를 반환
  - Entry 항목이 아니라 각 필터 명령문으로 Blog 항목을 필터링



다중 값 관계에 걸쳐있는 쿼리에 대한 `filter()` 동작은 `exclude()`에 대해 동일하게 구현되지 않음

대신 단일 `exclude()` 호출의 조건이 반드시 동일한 항목을 참조하지는 않음

```shell
# 제목에 "Lennon"이 있는 entry들과 2008년에 게시된 entry들이 모두 포함된 blog들 제외
>>> Blog.objects.exclude(
	entry__headline__contains='Lennon',
	entry__pub_date__year=2008
)
```

(`filter()`를 사용할 때의 동작과 달리) 두 조건을 모두 만족하는 entry들을 기반으로 blog를 제한하지는 않음

```shell
# 2008년에 "Lennon"으로 게시된 entry들이 포함되지 않은 모든 blog들 선택
>>> Blog.objects.exclude(
	entry__in=Entry.objects.filter(
		headline__contains='Lennon',
		pub_date__year=2008
	)
)
```



### 필터는 모델에 필드를 참조할 수 있다

`F()` 인스턴스

- Django는 모델 필드의 값을 동일한 모델의 다른 필드와 비교하기 위해 **F 표현**을 제공
- 쿼리 내 모델 필드에 대한 참조로 작동
- 쿼리 필터에서 사용하여 동일한 모델 인스턴스에서 서로 다른 두 필드의 값을 비교

```shell
# 핑백보다 더 많은 주석이 있는 모든 blog entry들의 목록 찾기
# 핑백 수를 참조하는 f() 객체를 구성하고 쿼리에서 해당 F() 객체를 사용
>>> from django.db.models import F
>>> Entry.objects.filter(
	number_of_comments__gt=F('number_of_pingbacks')
)
```

- Django는 (상수와 다른 `F()` 객체 둘 다와 함께) `F()` 객체를 사용하여 더하기, 빼기, 곱하기, 나누기, 모듈로 및 거듭 제곱 연산을 지원

```shell
# 핑백보다 두 배 이상의 주석이 있는 모든 blog entry들 찾기
>>> Entry.objects.filter(
	number_of_comments__gt=F('number_of_pingbacks') * 2
)

# entry의 등급이 핑백 수와 주석 수의 합보다 작은 모든 entry들 찾기
>>> Entry.objects.filter(
	rating__lt=F('number_of_comments') + F('number_of_pingbacks')
)
```

- 이중 밑줄 표기법을 사용하여 `F()` 객체의 관계를 확장
  - 밑줄이 이중인 `F()` 객체는 관련 객체에 액세스하는 데 필요한 조인을 소개

```shell
# author 이름이 blog 이름과 동일한 entry들 모두 찾기
>>> Entry.objects.filter(
	authors__name=F('blog__name')
)
```

- 날짜 및 날짜/시간 필드의 경우, `timedelta` 객체를 추가하거나 뺄 수 있음

```shell
# 게시된 후 3일 이상 수정된 모든 entry들 찾기
>>> from datetime import timedelta
>>> Entry.objects.filter(
	mod_date__gt=F('pub_date') + timedelta(days=3)
)
```

- `.bitand()`, `.bitor()`, `.bitrightshift()` 및 `.bitleftshift()`에 의한 비트 연산을 지원

```shell
>>> F('somefield').bitand(16)
```



### `pk` 조회 shortcut

`pk` 조회

- Django는 "기본 키"를 나타내는 `pk` 조회 shortcut을 제공

```shell
# Blog 모델에서 기본 키는 id 필드
# 셋 다 동일한 명령문
>>> Blog.objects.get(id__exact=14)
>>> Blog.objects.get(id=14)
>>> Blog.objects.get(pk=14)
```

- `pk` 사용은 `__exact` 쿼리로 제한되지 않음
  - 모든 쿼리 용어를 `pk`와 결합하여 모델의 기본 키에서 쿼리를 수행할 수 있음

```shell
>>> Blog.objects.filter(pk__in=[1, 4, 7])
>>> Blog.objects.filter(pk__gt=14)
```

- 조인에서도 작동

```shell
# 셋 다 동일한 문장
>>> Entry.objects.filter(blog__id__exact=3)
>>> Entry.objects.filter(blog__id=3)
>>> Entry.objects.filter(blog__pk=3)
```



### `LIKE` 문장에서 퍼센트 부호와 밑줄 이스케이프

`LIKE` SQL 문과 같은 필드 조회

- `iexact`, `contains`, `icontains`, `startswith`, `istartswith`, `endswith` 및 `iendswith`

- `LIKE` 문에 사용된 두 개의 특수문자(퍼센트 부호 및 밑줄)를 자동으로 이스케이프

- (`LIKE` 문에서) 백분율 기호와 밑줄은 모두 투명하게 처리됨

  - 백분율 기호: 여러 문자 와일드 카드
  - 밑줄: 단일 문자 와일트 카드

  - 직관적으로 작동해야 하므로 추상화가 유출되지 않음

  ```shell
  # 백분율 기호가 포함된 모든 entry들 찾기
  # 백분율 기호를 다른 문자로 사용
  >>> Entry.objects.filter(headline__contains='%')
  ```

  ```sql
  # Django는 인용을 처리함
  SELECT ... WHERE headline LIKE '%\%%';
  ```



### 캐싱 및 `QuerySet`

각 QuerySet에는 데이터베이스 액세스를 최소화하기 위한 캐시가 포함되어 있음

새로 작성된 QuerySet에서 캐시가 비어 있음

QuerySet을 처음 평가할 때(데이터베이스 쿼리 발생), Django는 QuerySet의 캐시에 쿼리 결과를 저장하고 명시적으로 요청된 결과를 반환

이후의 QuerySet 평가는 캐시된 결과를 재사용

```shell
# QuerySet을 작성하고 평가하여 버림
# 동일한 데이터베이스 쿼리가 두 번 실행
# 효과적으로 데이터베이스 로드가 두 배가 됨
>>> print([e.headline for e in Entry.objects.all()])
>>> print([e.pub_date for e in Entry.objects.all()])

# 두 요청 사이에 순간적으로 Entry가 추가 또는 삭제되었을 수 있음
# 두 목록에 동일한 데이터베이스 레코드가 포함되지 않을 수 있음
# 이 문제를 피하기 위해 QuerySet을 저장하고 재사용
>>> queryset = Entry.objects.all()
>>> print([p.headline for p in queryset])
>>> print([p.pub_date for p in queryset])
```



#### `QuerySet`이 캐시되지 않을 때

QuerySet이 항상 결과를 캐시하지는 않음

QuerySet의 일부만 평가할 때 캐시가 검사되지만, 채워지지 않으면 후속 쿼리에서 반환된 항목이 캐시되지 않음

- 배열 슬라이스 또는 인덱스를 사용하여 QuerySet을 제한하면 캐시가 채워지지 않음

```shell
# QuerySet 객체에서 특정 인덱스를 반복적으로 가져옴
>>> queryset = Entry.objects.all()
# 데이터베이스를 쿼리
>>> print(queryset[5])
# 데이터베이스를 다시 쿼리
>>> print(queryset[5])
```

전체 QuerySet이 이미 평가된 경우, 캐시가 대신 검사됨(캐시를 채움)

```shell
>>> queryset = Entry.objects.all()
# 데이터베이스를 쿼리
>>> [entry for entry in queryset]
# 캐시 사용
>>> print(queryset[5])
# 캐시 사용
>>> print(queryset[5])

# 다른 작업의 예
>>> [entry for entry in queryset]
>>> bool(queryset)
>>> entry in queryset
>>> list(queryset)
```

QuerySet을 인쇄하는 것만으로는 캐시가 채워지지 않음

- `__repr__()`에 대한 호출은 전체 QuerySet의 슬라이스만 반환하기 때문



## `Q` 객체가 포함된 복잡한 조회

`filter()` 등의 키워드 인수 쿼리는 "AND"

보다 복잡한 쿼리를 실행해야 하는 경우(`OR` 문이 있는 쿼리 등) **`Q` 객체**를 사용



`Q` 객체(django.db.models.Q)

- 키워드 인수 컬렉션을 캡슐화 하는데 사용되는 객체
- 키워드 인수는 "필드 조회"와 같이 지정됨

```python
# 단일 LIKE 쿼리를 캡슐화하는 Q 객체
from django.db.models import Q
Q(question__startswith='What')
```

- `&` 및 `|`를 사용하여 `Q` 객체를 결합할 수 있음

  - 연산자가 두 개의 `Q` 객체에 사용되면 새 `Q` 객체가 생성

  ```python
  # 두 개의 "question__startswith" 쿼리의 "OR"을 나타내는 단일 Q 객체를 생성
  Q(question__startswith='Who') | Q(question__startswith='What')
  ```

  ```sql
  # SQL에서 WHERE 절과 같음
  WHERE question LIKE 'Who%' OR question LIKE 'What%'
  ```

- ~ 연산자를 사용하여 `Q` 객체를 무효화 할 수 있음

  - 일반 쿼리와 부정(`NOT`) 쿼리를 모두 결합한 조합 조회

  ```shell
  Q(question__startswith='Who') | ~Q(pub_date__year=2005)
  ```

- 키워드 인수를 사용하는 각 조회 함수(`filter()`, `exclude()`, `get()`)에는 위치 (이름이 지정되지 않음) 인수로 하나 이상의 `Q` 객체가 전달될 수 있음

  - 조회 함수에 여러 개의 `Q` 객체 인수를 제공하면 인수는 "AND"가 됨

  ```python
  Poll.objects.get(
  	Q(question__startswith='Who'),
      Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6))
  )
  ```

  ```sql
  # SQL로 변환
  SELECT * from polls WHERE question LIKE 'Who%'
  	AND (pub_date = '2005-05-02' OR pub_date = '2005-05-06')
  ```

- 조회 함수는 `Q` 객체와 키워드 인수를 혼합하여 사용할 수 있음

  - 검색 함수에 제공된 모든 인수(키워드 인수 또는 `Q` 객체)는 "AND"로 함께 표시됨
  - `Q` 객체가 제공되는 경우, 키워드 인수의 정의보다 우선해야 함

  ```python
  Poll.objects.get(
  	Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)),
      question__startswith='Who'
  )
  ```

  

## 객체 비교

표준 Python 비교 연산자 ==

- 두 모델 인스턴스를 비교
- 두 모델의 기본 키 값을 비교 (비교는 항상 기본 키를 사용)

```shell
# 두 명령문은 동일
>>> some_entry == other_entry
>>> some_entry.id == other_entry.id

# 모델의 기본 키를 id라고 부르지 않아도 문제 없음
# 모델의 기본 키 필드를 name 이라고 하면 두 문장은 동일
>>> some_obj == other_obj
>>> some_obj.name == other_obj.name
```



## 객체 삭제

삭제 메소드 `delete()`

- 즉시 오브젝트를 삭제하고, 삭제된 오브젝트 수와 오브젝트 유형 당 삭제 수가 있는 사전을 리턴

  ```shell
  >>> e.delete()
  # (1, {'weblog.Entry': 1})
  ```

- 객체를 대량으로 삭제할 수 있음

  - 모든 QuerySet에는 해당 QuerySet의 모든 멤버를 삭제하는 `delete()` 메소드가 있음

  ```shell
  # pub_date 연도가 2005인 모든 Entry 객체 삭제
  >>> Entry.objects.filter(pub_date__year=2005).delete()
  # (5, {'webapp.Entry': 5})
  ```

- 프로세스 중에 개별 객체 인스턴스의 `delete()` 메소드가 반드시 호출되는 것은 아님

  - 가능할 때마다 순수하게 SQL로 실행됨
  - 모델 클래스에 커스텀 `delete()` 메소드를 제공하고 호출됐는지 확인하려면 해당 모델의 인스턴스를 "수동으로" 삭제해야 함
  - Django는 객체를 삭제하면 기본적으로 SQL 제약 조건 `ON DELETE CASCADE`의 동작을 모방함
    - 삭제할 객체를 가리키는 외래 키가 있는 객체는 함께 삭제됨
    - 계단식(cascade) 동작은 `on_delete` 인수를 통해 `ForeignKey`로 사용자 지정할 수 있음

  ```python
  b = Blog.objects.get(pk=1)
  # Blog와 모든 해당 Entry 개체 삭제
  b.delete()
  ```

- `Manager` 자체에 공개되지 않은 유일한 QuerySet 메소드

  - 실수로 `Entry.objects.delete()`를 요청하고 모든 entry들을 삭제하지 못하게 하는 안전 메커니즘
  - 모든 객체를 삭제하려면 전체 QuerySet을 명시적으로 요청해야 함

  ```python
  Entry.objects.all().delete()
  ```



## 모델 인스턴스 복사

모델 인스턴스를 복사하기 위한 기본 제공 방법은 없음

모든 필드 값을 복사하여 새 인스턴스를 쉽게 만들 수 있음



`pk`를 None으로 설정

- 가장 간단한 경우

  ```python
  blog = Blog(name='My blog', tagline='Blogging is easy')
  # blog.pk == 1
  blog.save()
  
  blog.pk = None
  # blog.pk == 2
  blog.save()
  ```

- 상속 사용

  - Blog의 하위 클래스를 고려

  ```python
  class ThemeBlog(Blog):
      theme = models.CharField(max_length=200)
      
  django_blog = ThemeBlog(name='Django', tagline='Django is easy', theme='python')
  # django_blog.pk ==3
  django_blog.save()
  ```

  - (상속 작동 방식으로 인해) `pk`와 `id`를 None으로 설정

  ```python
  django_blog.pk = None
  django_blog.id = None
  # django_blog.pk == 4
  django_blog.save()
  ```

  - 모델의 데이터베이스 테이블에 포함되지 않은 관계를 복사하지 않음

  ```python
  # Entry에는 Author to ManyToManyField가 있음
  # entry를 복제한 후에는 새 entry에 대해 다대다 관계를 설정해야 함
  entry = Entry.objects.all()[0] # 몇몇 이전 entry
  old_authors = entry.authros.all()
  entry.pk = None
  entry.save()
  entry.authors.set(old_authors)
  
  # OneToOneField의 경우, 일대일 고유 제약조건을 위반하지 않도록 관련 객체를 복제하고 새 객체의 필드에 할당해야 함
  # entry가 이미 위와 같이 복제되었다고 가정
  detail = EntryDetail.objects.all()[0]
  detail.pk = None
  detail.entry = entry
  detail.save()
  ```



## 여러 객체를 한 번에 업데이트

`update()` 메소드

- QuerySet의 모든 객체에 대해 필드를 특정 값으로 설정하려는 경우

  ```python
  # 2007년 pub_date로 모든 headline 업데이트
  Entry.objects.filter(
  	pub_date__year=2007
  ).update(
  	headline='Everything is the same'
  )
  ```

- 관계형이 아닌 필드와 `ForeignKey` 필드만 설정할 수 있음

  - 비관계 필드를 업데이트: 새 값을 상수로 제공
  - `ForeignKey` 필드를 업데이트: 새 값을 지정하려는 새 모델 인스턴스로 설정

  ```shell
  >>> b = Blog.objects.get(pk=1)
  # 이 Blog에 속하도록 모든 Entry 변경
  >>> Entry.objects.all().update(blog=b)
  ```

- 즉시 적용되며, 쿼리와 일치하는 행 수를 반환

  - 일부 행에 이미 새 값이 있는 경우, 업데이트된 행 수와 같지 않을 수 있음

  - 모델의 기본 테이블인 하나의 데이터베이스 테이블에만 액세스할 수 있음

    - 관련 필드 기준으로 필터링할 수 있지만, 모델의 기본 테이블에서 열만 업데이트할 수 있음

    - 업데이트되는 QuerySet에 대한 유일한 제한

  ```shell
  >>> b = Blog.objects.get(pk=1)
  # 이 Blog에 속한 모든 headline 업데이트
  >>> Entry.objects.select_related().filter(
  	blog=b
  ).update(
  	headline='Everything is the same'
  )
  ```

- SQL 문으로 직접 변환됨 (직접 업데이트를 위해)

  - 모델에서 `save()` 메소드를 실행하거나 `pre_save` 또는 `post_save` 신호(`save()` 호출의 결과)를 내보내거나 `auto_now` 필드 옵션을 적용하지 않음
  - QuerySet에 모든 항목을 저장하고 각 인스턴스에서 `save()` 메소드가 호출되도록 하기 위한 어떠한 특별한 기능도 필요하지 않음
  - 반복하고 `save()` 호출

  ```python
  for item in my_queryset:
      item.save()
  ```

- 업데이트 호출은 F 표현식 사용

  - 모델의 다른 필드 값을 기반으로 한 필드를 업데이트
  - 현재 값 기준으로 카운터를 증가시킬 때 특히 유용

  ```shell
  # blog의 모든 entry에 대해 핑백 수 늘리기
  >>> Entry.objects.all().update(
  	number_of_pingbacks=F('number_of_pingbacks') + 1
  )
  ```

- filter와 exclude 절의 `F()` 객체와 달리, 업데이트에서 `F()` 객체를 사용할 때는 조인을 도입할 수 없음

  - 업데이트 중인 모델의 로컬 필드만 참조할 수 있음
  - `F()` 객체와의 조인을 시도하면 `FieldError` 발생

  ```shell
  # FieldError 발생
  >>> Entry.objects.update(headline=F('blog__name'))
  ```



## 관련 객체





### 일대다 관계

#### Forward

#### "backward" 관계 접근

#### 커스텀 리버스 매니저 사용

#### 관련 개체를 처리하는 추가 방법

### 다대다 관계

### 일대일 관계

### backward 관계는 어떻게 가능할까?

### 관련 개체에 대한 쿼리



## 원시 SQL로 폴백