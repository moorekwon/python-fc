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
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
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

1. 객체를 인스턴스화
   - 모델 클래스에 키워드 인수를 사용

2. save()
   - 데이터베이스에 저장하도록 호출



mysite

- blog

  - models.py

    ```shell
    >>> from blog.models import Blog
    >>> b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
    >>> b.save()
    ```

    - Django는 명시적으로 save() 호출할 때까지 데이터베이스에서 충돌하지 않음
    - create(): 단일 관계에서 객체를 생성하고 저장



## 객체 변경사항 저장

save()

- 데이터베이스에 이미 있는 객체에 변경 사항을 저장

- 지정된 Blog 인스턴스 b5가 이미 데이터베이스에 저장

  ```shell
  # 이름을 변경하고 데이터베이스에 그 기록을 갱신
  >>> b5.name = 'New name'
  >>> b5.save()
  ```



### ForeignKey와 ManytoManyField 필드 저장

ForeignKey 필드 업데이트

- 일반 필드를 저장하는 것과 정확히 같은 방식으로 작동

- Entry와 Blog의 적절한 인스턴스가 이미 데이터베이스에 저장되어 있다고 가정하여, Entry 인스턴스 entry 항목의 블로그 속성을 업데이트

  ```shell
  >>> from blog.models import Blog, Entry
  >>> entry = Entry.objects.get(pk=1)
  >>> cheese_blog = Blog.objects.get(name="Cheddar Talk")
  >>> entry.blog = cheese_blog
  >>> entry.save()
  ```



ManyToMany 필드 업데이트

- 약간 다른 방식으로 작동

- 필드에서 add() 메소드 사용하여 관계에 레코드를 추가

- Author 인스턴스 joe를 entry 오브젝트에 추가

  ```shell
  >>> from blog.models import Author
  >>> joe = Author.objects.craete(naem="Joe")
  >>> entry.authors.add(joe)
  ```

- add() 호출에 여러 인수를 포함하여 여러 레코드를 한 번에 추가

  ```shell
  >>> john = Author.objects.create(name="John")
  >>> paul = Author.objects.create(name="Paul")
  >>> george = Author.objects.create(name="George")
  >>> ringo = Author.objects.create(name="Ringo")
  >>> entry.authors.add(john, paul, george, ringo)
  ```



## 객체 검색(조회)





### 모든 객체 검색

### 필터를 사용하여 특정 객체 검색

#### 체인 필터

#### 필터링된 `QuerySet`은 고유하다

#### `QuerySet`들은 게으르다

### `get()`로 단일 객체 검색

### 다른 `QuerySet` 방법

### 제한 `QuerySet`들

### 필드 조회

### 관계에 걸친 조회

#### 다중 값 관계 스패닝

### 필터는 모델에 필드를 참조할 수 있다

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