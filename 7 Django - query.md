

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

모델 필드의 값을 동일한 모델의 다른 필드와 비교





### `pk` 조회 shortcut

### `LIKE` 문장에서 퍼센트 부호와 밑줄 이스케이프

### 캐싱 및 `QuerySet`

#### `QuerySet`이 캐시되지 않을 때



## `Q` 객체가 포함된 복잡한 조회



## 객체 비교



## 객체 삭제



## 모델 인스턴스 복사



## 여러 객체를 한 번에 업데이트



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