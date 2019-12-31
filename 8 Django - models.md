# Django - models

## Models

모델

- 데이터에 대한 정보를 나타내는 최종 소스 (갖고 있는 데이터의 필수 필드와 행동(함수)를 포함)
- 각각의 모델은 데이터베이스의 테이블에 매핑
- 각각의 모델은 `django.db.models.Model`의 서브클래스
- 모델의 각 속성은 데이터베이스의 필드를 나타냄
  - 이것들을 이용하여 장고는 데이터베이스 액세스 API를 제공



```python
from django.db import models

# first_name과 last_name을 가진 Person을 정의한 모델
class Perosn(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
```

- `first_name`, `last_name`

  - 모델의 필드
  - 각각의 필드는 클래스의 속성을 나타내며, 데이터베이스의 컬럼에 매핑

- 데이터 테이블을 만듦

  ```python
  # 데이터 테이블
  CREATE TABLE myapp_person (
  	"id" serial NOT NULL PRIMARY KEY,
      "first_name" varchar(30) NOT NULL,
      "last_name" varchar(30) NOT NULL
  );
  ```

  - `myapp_person`: 테이블의 이름 (재정의 할 수 있음)
  - `id` 필드: 자동으로 추가 (오버라이드 할 수 있음)
  - `CREATE TABLE` SQL: `PostgreSQL` 문법이지만, 장고에서는 지정된 데이터베이스에 맞는 SQL을 사용



## Using models

모델을 정의하면, 장고에게 이 모델을 사용할 것임을 알려야 함

```python
# 설정 파일
INSTALLED_APPS = [
    # models.py를 포함하고 있는 모듈의 이름을 추가
    'myapp',
]
```

1. 새로운 애플리케이션을 `INSTALLED_APPS`에 추가
2. `manage.py makemigrations`를 사용하여 (선택적으로) 마이그레이션을 먼저 만듦
3. `manage.py migrate` 명령어를 실행



## Fields

모델에서 가장 중요한 부분 (반드시 필요)

데이터베이스의 필드를 정의

클래스 속성으로 사용됨

clean, save, delete와 같은 models API와 중복되지 않도록 함



```python
from django.db import models

class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)
    
class Album(models.Model):
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()
```



### Field types

필드 클래스

- 각각의 필드는 적절한 필드 클래스의 인스턴스여야 함

- 정의된 사항
  - 데이터베이스 컬럼의 데이터 형
  - form field를 렌더링할 때 사용할 기본 HTML 위젯
  - Django admin에서 자동으로 만들어지는 form의 검증 형태



장고는 다양한 내장 필드 타입을 제공

장고에서 제공하지 않는 자신만의 필드를 쉽게 만들 수 있음



### Field options

각 필드는 고유의 인수를 가짐

- `CharField`
  - `max_length` 인수를 반드시 가져야 함
  - 데이터베이스에서 VARCHAR 필드의 사이즈를 지정



모든 필드에 사용 가능한 공통 인수 (모두 선택사항)

- null

  - True일 경우, 장고는 빈 값을 NULL로 데이터베이스에 저장
  - 기본값은 False
  - 데이터베이스에 NULL 값이 들어가는 것을 허용

- blank

  - True일 경우, 필드는 빈 값을 허용
  - 기본값은 False
  - 데이터베이스에 빈 문자열 값("")을 허용
  - form validation
    - blank=True일 경우, 공백값을 허용
    - blank=False일 경우, 해당 필드는 반드시 채워져야 함

- choices

  - 반복가능한 튜플의 묶음을 선택 목록으로 사용

    ```python
    YEAR_IN_SCHOOL_CHOICES = (
        # 튜플의 첫 번째 요소는 데이터베이스에 저장되는 값
        # 튜플의 두 번째 요소는 기본 양식이나 위젯에 표시되는 값
    	('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('GR', 'Graduate'),
    )
    ```

  - 모델 인스턴스에서 표시되는 값을 액세스하기 위해 get_FOO_display() 함수를 사용

    ```python
    from django.db import models
    
    class Person(models.Model):
        SHIRT_SIZES = (
        	('S', 'Small'),
            ('M', 'Medium'),
            ('L', 'Large'),
        )
        
        name = models.CharField(max_length=60)
        shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)
    ```

    ```shell
    >>> p = Person(name="Fred Flintstone", shirt_size="L")
    >>> p.save()
    >>> p.shirt_size
    'L'
    >>> p.get_shirt_size_display()
    'Large'
    ```

- default

  - 필드에 기본값으로 설정됨

- help_text

  - 폼 위젯에서 추가적으로 보여줄 도움말 텍스트
  - 폼을 사용하지 않아도 문서화에 도움

- primary_key

  - True일 경우, 해당 필드는 모델의 primary key로 사용됨
  - 필드에 `primary_key=True`를 설정하지 않으면, 장고는 자동으로 `IntegerField`를 생성해 primary key로 사용
  - 반드시 `primary_key=True`를 어떤 필드에 추가할 필요는 없음
  - 읽기 전용
  - 기존 개체의 primary key 값을 변경한 후 저장하면, 이전 객체와는 별개의 새로운 객체가 생성됨

- unique

  - True일 경우, 이 필드의 값은 테이블 전체에서 고유해야 함



### Automatic primary key fields

auto-increment primary key

```python
id = models.AutoField(primary_key=True)
```

- 기본적으로 장고가 각 모델에 제공하는 필드
- 만약 임의의 primary key를 지정하고 싶다면, 필드 중 하나에 `primary_key=True`를 지정
- primary key 필드를 추가했을 경우, `id` 컬럼을 추가하지 않음
- 각각의 모델은 정확히 하나의 `primary_key=True` 필드를 가져야 함



### Verbose field names

필드에서 첫 번째 인수는 자세한 필드명 (`ForeignKey`, `ManyToManyField`, `OneToOneField` 필드 제외)

Verbose name이 주어지지 않을 경우, 장고는 자동으로 해당 필드의 이름을 사용해 Verbose name을 만들어 사용

```python
# verbose name은 person's first name
first_name = models.CharField("person's first name", max_length=30)
```

```python
# verbose name은 first name
first_name = models.Charfield(max_length=30)
```



`ForeignKey`, `ManyToManyField`, `OneToOneField`

- 첫 번째 인자로 모델 클래스를 가져야 하므로, `verbose_name` 인수를 사용

  ```python
  poll = models.ForeignKey(
  	Poll,
      on_delete=models.CASCADE,
      verbose_name="the related poll",
  )
  
  sites = models.ManyToManyField(Site, verbose_name="list of sites")
  
  places = models.OneToOneField(
  	Place,
      on_delete=models.CASCADE,
      verbose_name="related place",
  )
  ```

  - 첫 글자는 대문자로 지정하지 않음
  - 장고는 자동으로 첫 번째 글자를 대문자화함



### Relationships

관계형 데이터베이스의 강력함은 테이블간의 관계에 있음

데이터베이스의 관계 유형

- `many-to-one`
- `many-to-many`
- `one-to-one`



#### Many-to-one-relationships

`ForeignKey`

- many-to-one 관계를 정의
- 모델의 클래스 속성으로 정의
- 관계를 정의할 모델 클래스를 인수로 가져야 함
- 자기 자신이나 아직 선언되지 않은 모델에 대해서도 관계를 가질 수 있음



```python
from django.db import models

# 여러 개의 Car을 가질 수 있음
class Manufacturer(models.Model):
    pass

# Car 모델은 Manufacturer을 ForeignKey로 가짐
# 오직 하나의 Manufacturer만 가짐
class Car(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
```



#### Many-to-many relationships

`ManyToManyField`

- many-to-many 관계를 정의
- 관계를 정의할 모델 클래스를 인수로 가져야 함



```python
from django.db import models

# 여러 개의 Pizza에 올라갈 수 있음
class Topping(models.Model):
    pass

# 여러 개의 Topping 객체를 가질 수 있음
class Pizza(models.Model):
    toppings = models.ManyToManyField(Topping)
```

- 일반적으로 필드명은 관계된 모델 객체의 복수형 (권장)
- 어떤 모델이 `ManyToManyField`를 갖는지는 중요하지 않음
- 관계되는 둘 중 하나의 모델에만 존재해야 함
- `ManyToManyField` 인스턴스는 form에서 수정할 객체에 가까워야 함
  - `Pizza` form에서 `toppings`를 선택 (`topping` form에서 `pizzas`가 아니라)



##### Extra fields on many-to-many relationships

두 모델 사이의 관계와 데이터를 연결해야 할 경우, 장고에서는 many-to-many 관계를 관리하는 데 사용되는 모델을 지정할 수 있음

중간 모델에 추가 필드를 넣을 수 있음 (`ManyToManyField`의 `through` 인수에 중간 모델을 가리키도록 하여 연결)



```python
# 사람과 그룹으로 멤버를 이루는 관계에서, 음악가가 속한 그룹을 트래킹(추적)
from django.db import models

# 타겟 모델
class Person(models.Model):
    name = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name
  
# 원본 모델
class Group(models.Model):
    name = models.CharField(maX_length=128)
    # ManyToManyField의 through 인수에 중간 모델을 가리키도록 하여 연결
    members = models.ManyToManyField(Person, through='Membership')
    
    def __str__(self):
        return self.name
  
# 중간 모델
class Membership(models.Model):
    # 중간 모델을 설정할 때, 명시적으로 many-to-many 관계에 참여하는 모델들의 ForeignKey를 지정
    # 두 모델이 관련되는 법을 정의
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    # 어떤 사람이 그룹으로 가입할 때 추가로 존재하는 세부사항들
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)
```

- 중간 모델의 제한 사항
  - 중간 모델(과 타겟 모델)은 원본 모델에 대해 단 하나의 ForeignKey 필드를 가져야 함
    - 아니면 반드시 `ManyToMany` 필드에서 `through_fields` 옵션으로 관계에 사용될 필드 이름을 지정해 주어야 함
  - 자기 자신에게 many-to-many 관계를 가지는 모델의 경우
    - 중간 모델에 동일한 모델에 대한 `ForeignKey` 필드를 2개 선언할 수 있음
    - 3개 이상의 `ForeignKey` 필드를 선언할 경우, `through-fields` 옵션을 설정해 주어야 함
  - 자기 자신에게 many-to-many 관계를 갖고 중간 모델을 직접 선언하는 경우
    - `ManyToMany` 필드의 `symmetrical` 옵션을 `False`로 설정해 주어야 함



```shell
# ManyToManyField에서 중간 모델(Membership)을 사용
# 중간 모델 인스턴스 생성
>>> ringo = Person.objects.create(name="Ringo Starr")
>>> paul = Person.objects.create(name="Paul McCartney")
>>> beatles = Group.objects.create(name="The Beatles")
>>> m1 = Membership(
	person=ringo,
	group=beatles,
	date_joined=date(1962, 8, 16),
	invite_reason="Needed a new drummer."
)
>>> m1.save()
>>> beatles.members.all()
<QuerySet [<Person: Ringo Starr>]>
>>> ringo.group_set.all()
<QuerySet [<Group: The Beatles>]>
>>> m2 = Membership.objects.create(
	person=paul,
	group=beatles,
	date_joined=date(1960, 8, 1),
	invite_reason="Wanted to form a band."
)
>>> beatles.members.all()
<QuerySet [<Person: Ringo Starr>, <Person: Paul McCartney>]>
```

```shell
# 일반적인 many-to-many 필드와 달리, 직접 할당 명령어(add(), create(), set())를 사용할 수 없음
>>> beatles.members.add(john)
>>> beatles.members.create(name="George Harrison")
>>> beatles.members.set([john, paul, ringo, george])
```

- `Person`과 `Group` 관계를 설정할 때, 중간 모델의 필드값들을 명시해 주어야 함
- 중간 모델에서 person과 group 필드값은 알 수 있지만, date_joined와 invite_reason 필드값은 알 수 없기 때문



```shell
# 중간 모델을 직접 지정한 경우, 중간 모델을 직접 생성해야 함
>>> Membership.objects.create(person=ringo, group=beatles, date_joined=date(1968, 9, 4), invite_reason="You've been gone for a month and we miss you.")
>>> beatles.members.all()
<QuerySet [<Person: Ringo Starr>, <Person: Paul McCartney>, <Person: Ringo Starr>]>
>>> beatles.members.remove(ringo)

# clear() 함수는 사용 가능
>>> beatles.members.clear()
>>> Membership.objects.all()
<QuerySet []>

# 쿼리시에는 일반적인 many-to-many 관계와 동일하게 사용 가능
>>> Group.objects.filter(members__name__startswith='Paul')
<QuerySet [<Group: The Beatles>]>

# 중간 모델을 사용하고 있기 때문에 가능
# 비틀즈 멤버 중 1961년 1월 1일 이후에 합류한 멤버 찾기
>>> Person.objects.filter(group__name='The Beatles', membership__date_joined__gt=date(1961, 1, 1))

# Membership 모델에 직접 쿼리
>>> ringos_membership = Membership.objects.get(group=beeatles, person=ringo)
>>> ringos_membership.date_joined
datetime.date(1962, 8, 16)
>>> ringos_membership.invite_reason
'Needed a new drummer.'

# Person 객체로부터 many-to-many 역참조를 이용
>>> ringos_membership = ringo.membership_set.get(group=beatles)
>>> ringos_membership.date_joined
datetime.date(1962, 8, 16)
>>> ringos_membership.invite_reason
'Needed a new drummer.'
```



#### One-to-one relationships

`OneToOneField`

- one-to-one 관계를 정의
- 모델 클래스의 어트리뷰트로 선언
- 다른 모델을 확장하여 새로운 모델을 만드는 경우 유용
- 자기 자신이나 아직 선언되지 않은 모델에 대해서도 관계를 가질 수 있음
- `parent_link` 옵션을 제공
- 하나의 모델이 여러 개의 `OneToOneField`를 가질 수 있음



가게(Places) 정보가 담긴 데이터베이스를 구축한다고 가정

- 데이터베이스에 주소, 전화번호 등의 정보가 들어가야 함
- 맛집 데이터베이스를 추가적으로 구축할 경우, 새로 Restaurant 모델을 만드는 반복을 피하기 위해 Restaurant 모델에 Place 모델만 `OneToOneField`로 선언



> `OneToOneField`클래스가 자동적으로 모델의 primary key가 되었던 적이 있습니다. 지금은 더 이상 그렇게 사용하지 않습니다. 물론, 직접 `primary_key=True`를 지정하여 primary key로 만들 수는 있습니다.



### Models across files

다른 앱에 선언된 모델과 관계를 가질 수 있음

다른 앱의 모델을 import 해서 관계 필드를 선언



```python
from django.db import models
from geography.models import ZipCode

class Restaurant(models.Model):
    zip_code = models.ForeignKey(
    	ZipCode,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
```



### Field name restrictions

모델 필드명의 제약

1. 파이썬 예약어는 필드명으로 사용할 수 없음

   ```python
   class Example(models.Model):
       # 'pass'는 예약어
       pass = models.IntegerField()
   ```

2. 필드 이름에 밑줄 두 개를 연속으로 사용할 수 없음

   ```python
   class Example(models.Model):
       # 밑줄 두 개를 연속으로 사용하면, 장고에서 특별한 문법으로 사용됨
       foo__bar = models.IntegerField()
   ```

   - 데이터베이스에 컬럼명을 밑줄 두 개 넣어야 하는 경우, `db_column` 옵션을 사용하여 제약을 우회
   - SQL 예약어의 경우, (join, where, select)에는 필드 이름으로 허용됨
     - 장고에 쿼리문을 만들 때, 모든 컬럼명과 테이블명은 (실제 데이터베이스 엔진에 맞게 알아서) 이스케이프 처리함



### Custom field types

필드를 직접 만들어 사용할 수 있음

- 장고에서 제공하는 필드 타입 중 적절한 타입이 없는 경우
- 특정 데이터베이스에서만 제공하는 특별한 타입을 사용하고 싶은 경우



## Meta options

모델 클래스 내부에 Meta 라는 이름의 클래스를 선언

- 모델에 메타데이터를 추가



```python
from django.db import models

class Ox(models.Model):
    horn_length = models.IntegerField()
    
    # 모델 메타데이터
    class Meta:
        # 정렬 옵션
        ordering = ["horn_length"]
        # 복수 이름
        verbose_name_plural = "oxen"
```

- 모델 메타데이터
  - (필드의 옵션이 아니라) 모델 단위의 옵션
  - 옵션을 지정할 수 있음
    - ordering: 정렬 옵션
    - db_table: 데이터베이스 테이블 이름
    - verbose_name: 읽기 좋은 이름
    - verbose_name_plural: 복수 이름
  - 모델 클래스에 반드시 선언해야 하는 것은 아님
  - 모든 옵션을 설정해야 하는 것은 아님



## Model attributes

### objects

`Manager` 객체

- 모델 클래스에서 가장 중요한 속성
- 모델 클래스를 기반으로 데이터베이스에 대한 쿼리 인터페이스를 제공
- 데이터베이스 레코드를 모델 객체로 인스턴스화 함
- 할당하지 않으면 장고는 기본 Manager를 클래스 속성으로 자동 할당하는데, 이 때 속성의 이름이 <u>objects</u>



## Model methods

모델 클래스에 메소드를 구현해주어 모델 객체(row) 단위의 기능을 구현

테이블 단위의 기능은 Manager에 구현

```python
from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    
    def baby_boomer_status(self):
        "Returns the person's baby-boomer status."
        import datetime
        if self.birth_date < datetime.date(1945, 8, 1):
            return "Pre-boomer"
        elif self.birth_date < datetime.date(1965, 1, 1):
            return "Baby boomer"
        else:
            return "Post_boomer"
        
    def _get_full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)
    # property는 메소드를 속성처럼 접근할 수 있도록 해줌
    full_name = property(_get_full_name)
```



모델 클래스에 자동적으로 주어지는 메소드

- `__str__()` (Python 3)
  - 모델 객체가 문자열로 표현되어야 하는 경우에 호출
  - admin이나 console에서 많이 쓰임
  - 기본 구현은 아무 도움이 되지 않는 문자열을 리턴
  - 모든 모델에 대해 오버라이드 해서 알맞게 구현해주는게 좋음
- `get_absolute_url()`
  - 장고가 해당 모델 객체의 URL을 계산할 수 있도록 함
  - 장고는 모델 객체를 URL로 표현하는 경우에 사용
  - admin 사이트에서도 사용
  - 모델 객체가 유일한 URL을 가지는 경우 구현해주어야 함



### Overriding predefined model methods

커스터마이징 할 데이터베이스 동작을 캡슐화하는 모델 메소드 집합

`save()`나 `delete()`의 작업방식을 바꾸는 경우가 많음

동작을 바꾸기 위해 오버라이드 할 수 있음 



```python
from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()
    
    # 내장된 메소드를 재정의
    # 객체를 저장할 때마다 어떤 작업을 수행하기를 원할 때 사용
    def save(self, *args, **kwargs):
        do_something()
        super(Blog, self).save(*args, **kwargs)
        do_something_else()
```

```python
from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()
    
    # 저장을 막을 수도 있음
    def save(self, *args, **kwargs):
        if self.name == "Yoko Ono's blog":
            return
        else:
            # 슈퍼 클래스 메소드를 호출하는 것을 기억해야 함
            super(Blog, self).save(*args, **kwargs)
```

- `super(Blog, self).save(* args, **kwargs)`
  - 객체가 데이터베이스에 저장되도록 함
  - 슈퍼 클래스 메소드를 호출하는 것을 잊어버리면 기본 동작이 실행되지 않고, 데이터베이스에 저장하지 않음
  - `*args`, `**kwargs` 변수
    - 모델 메소드에 전달할 수 있는 인수를 전달
    - 장고는 수시로 내장 모델 메소드의 기능을 확장하여 새로운 인수를 추가함
    - 코드가 추가될 때 해당 인수를 자동으로 지원한다는 보장을 받음
- 오버라이드 된 모델 메소드는 `bulk operations`에서는 동작하지 않음
  - 쿼리셋을 사용하여 대량으로 객체를 삭체할 때 delete() 메소드가 반드시 호출되지 않을 수 있음
    - `pre_delete`와 `post_delete` 시그널을 사용하여 사용자 정의 삭제 논리를 실행
  - `bulk operaitons`에서는 `save()` 메소드, `pre_save` 및 `post_save` 시그널이 호출되지 않음
    - 객체를 대량으로 만들거나 업데이트 할 때 해결 방법이 없음



### Executing custom SQL

모델 메소드 및 모듈 수준 메소드에 사용자 지정 SQL 문을 작성



## Model inheritance

장고의 모델 상속

- 파이썬의 클래스 상속과 작동하는 방식이 거의 동일
- 반드시 따라야하는 기본 사항
  - 기본 클래스가 `django.db.models.Model`을 상속받아야 함
  - 부모 모델이 자체 데이터베이스 테이블을 가지는 모델이 될지, 부모가 자식 모델에게 전달할 정보만 갖고 있는지 여부만 결정하면 됨
- 상속을 제공하는 스타일
  1. 추상 기본 클래스(Abstract base classes)
     - 부모 클래스를 사용하여 각 하위 모델에 대해 일일이 입력하지 않으려는 정보를 제공하는 경우
     - 클래스를 따로 분리하여 사용하지 않음
     - 가장 일반적
  2. 다중 테이블 상속(Multi table inheritance)
     - 기존 모델을 하위 클래스화 하고, 각 모델이 자체 데이터베이스 테이블을 가지기를 원하는 경우
  3. `Proxy` 모델
     - 모델 필드를 변경하지 않고 모델의 파이썬 수준 동작만 수정하려는 경우



### Abstract base classes

추상 기본 클래스

- 몇 가지 공통된 정보를 여러 다른 모델에 넣으려 할 때 유용
- 기본 클래스를 작성하고 `Meta` class에 `abstract = True`를 넣음
- 데이터베이스 테이블을 만드는 데 사용되지 않는 대신, 다른 모델의 기본 클래스로 사용될 때 해당 필드는 자식 클래스의 필드에 추가됨
- 자식의 이름과 같은 이름(상속받은 클래스의 이름과 같은 이름의 필드)을 가진 추상 기본 클래스의 필드를 가질 수 없음
- 파이썬 레벨에서 공통 정보를 제외시키는 방법을 제공하면서, 데이터베이스 레벨에서 하위 모델 당 하나의 데이터베이스 테이블만 생성
- 기본 클래스가 자체적으로 존재하지 않음



```python
from django.db import models

# abstract base class
class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    
    class Meta:
        abstract = True
        
class Student(CommonInfo):
    hmoe_group = models.CharField(max_length=5)
```

- `Student` 모델에는 `name`, `age`, `home_group` 세 가지 필드가 있음
- `CommonInfo` 모델은 일반 `Django` 모델로 사용할 수 없음
  - 데이터베이스 테이블을 생성하지 않음
  - `Manager`를 가지지 않음
  - 직접 인스턴스화 하거나 저장할 수 없음



#### Meta inheritance

추상 기본 클래스가 생성되면 장고는 기본 클래스에서 선언한 `Meta` 내부 클래스를 속성으로 사용할 수 있게 함

자식 클래스가 자신의 `Meta` 클래스를 선언하지 않으면 부모 클래스의 메타를 상속받음



```python
from django.db import models

class CommonInfo(models.Model):
    class Meta:
        abstract = True
        ordering = ['name']
  
# 자식이 부모의 Meta 클래스를 확장하면 해당 클래스를 서브 클래스로 사용할 수 있음
class Student(CommonInfo):
    class Meta(CommonInfo.Meta):
        db_table = 'student_info'
```



장고는 추상 기본 클래스의 `Meta` 클래스를 조정함

`Meta` 속성을 적용하기 전에 `abstract` 속성 값을 `False`로 설정함 (추상 기본 클래스의 자식은 자동으로 추상 클래스가 되지 않음)

매번 `abstract = True`를 명시적으로 설정하면, 다른 추상 기본 클래스에서 상속받은 추상 기본 클래스를 만들 수 있음



#### Be careful with related_name and related_query_name

ForeignKey 또는 ManyToManyField에서 related_name 또는 related_query_name을 사용하는 경우

- 필드의 고유한 역 이름(reverse name)과 쿼리 이름(query name)을 항상 지정해야 함
- ForeignKey, ManyToManyField 필드를 가진 추상 기본 클래스를 상속받은 경우, 매번 해당 속성(related_name 또는 related_query_name)에 대해 정확히 동일한 값이 사용됨
- 이 문제를 해결하려면, 추상 기본 클래스에서 값의 일부에 '%(app_label)s' 및 '%(class)s'를 포함
  - '%(class)s': 필드가 사용되는 하위 클래스의 lower-cased 이름으로 대체
  - '%(app_label)s': 하위 클래스가 포함된 애플리케이션 이름의 lower-cased 이름으로 대체



```python
# common/models.py
from django.db import models

class Base(models.Model):
    m2m = models.ManyToManyField(
    	OtherModel,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)s",
    )
    
    class Meta:
        abstract = True
        
class ChildA(Base):
    pass

class ChildB(Base):
    pass
```

- common.ChildA.m2m 필드
  - reverse name은 'common_childa_related'
    - related_name 속성을 지정하지 않으면 'childa_set'
  - reverse query name은 'common_childas'
- common.ChildB.m2m 필드
  - reverse name은 'common_childb_related'
    - related_name 속성을 지정하지 않으면 'childb_set'
  - reverse query name은 'common_childbs'

```python
# rare/models.py
from common.models import Base

class ChildB(Base):
    pass
```

- rare.ChildB.m2m 필드
  - reverse name은 'rare_childb_related'
  - reverse query name은 'rare_childbs'



### Multi-table inheritance

계층 구조의 각 모델이 모두 각각 자신을 나타내는 모델인 경우

각 모델

- 자체 데이터베이스 테이블에 해당

- 개별적으로 쿼리하고 생성할 수 있음



```python
# 상속 관계는 자동으로 생성된 OneToOneFIeld를 통해 자식 모델과 부모 간 링크를 만듦
from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)
    
class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)
```

```shell
# Place의 모든 필드는 Restaurant에서 사용할 수 있지만, 데이터는 다른 데이터베이스 테이블에 있음
>>> Place.objects.filter(name="Bob's Cafe")
>>> Restaurant.objects.filter(name="Bob's Cafe")
```



```shell
# Restaurant 이면서 Place가 있는 경우, 모델 이름의 소문자 버전을 사용하여 Place 객체에서 Restaurant 객체를 가져올 수 있음
>>> p = Place.objects.get(id=12)
>>> p.restaurant
# <Restaurant: ...>
```

- p가 Restaurant이 아닌 경우(Place 객체로 직접 작성됐거나 다른 클래스의 부모인 경우), p.restaurant을 참조하면 Restaurant.DoesNotExist 예외 발생



```python
# Restaurant에 자동으로 생성된 OneToOneField
place_ptr = models.OneToOneField(
	Place,
    on_delete=models.CASCADE,
    parent_link=True,
)
```

- Restaurant에서 parent_link=True를 사용해 자신의 OneToOneField를 선언하여 해당 필드를 재정의 할 수 있음



#### Meta and multi-table inheritance

자식 모델은 부모의 메타 클래스에 액세스 할 수 없음

- 다중 테이블 상속 상황에서 자식 클래스가 부모의 Meta 클래스에서 상속받는 것은 의미가 없음

- 모든 메타 옵션은 이미 상위 클래스에 적용되었고 다시 적용하면 모순된 행동만 발생함



자식이 부모로부터 동작을 상속하는 제한된 경우

- 자식이 ordering 특성이나 get_latest_by 특성을 지정하지 않으면 해당 특성을 부모로부터 상속

  ```python
  class ChildModel(ParentModel):
      class Meta:
          ordering = []
  ```



#### Inheritance and reverse relations

다중 테이블 상속

- 암시적으로 OneToOneField를 사용하여 부모와 자식을 연결
- 자식 클래스를 임의의 추상이 아닌 부모 모델에 연결
- 상위에서 하위로 이동 가능
- 모델의 각 하위 클래스에 대해 새 데이터베이스 테이블이 만들어짐



```python
# Place 클래스에서 ManyToMAnyField를 사용하는 다른 하위 클래스를 만듦
class Supplier(Place):
    customers = models.ManyToManyField(Place)
    
# 결과 에러
# Reverse query name for 'Supplier.customers' clashes with reverse query
# name for 'Supplier.place_ptr'.

# HINT: Add or change a related_name argument to the definition for
# 'Supplier.customers' or 'Supplier.place_ptr'.
```

- customers_name 필드에 related_name을 추가
  - models.ManyToManyField(Place, related_name='provider')에서 발생한 오류 해결
- related_name 값으로 ForeignKey 및 ManyToManyField 관계에 대한 기본 값을 사용해야 함
  - 관계 유형들을 부모 모델의 하위 클래스에 배치하는 경우, 해당 필드 각각에 반드시 related_name 속성을 지정해야 함



#### Specifying the parent link field

부모에게 다시 연결되는 속성의 이름을 제어하려는 경우

- 고유한 OneToOneField를 만들고 parent_link=True로 설정

- 해당 필드가 부모 클래스에 대한 링크임을 나타내줌



### Proxy models

모델의 파이썬에서 동작만을 변경하고자 하는 경우

- 기본 관리자를 변경

- 새 메소드를 추가



프록시 모델 상속

- 원래 모델에 대한 proxy를 만듦
- 프록시 모델의 인스턴스를 생성, 삭제, 업데이트
- 원본(비 프록시) 모델을 사용하는 것처럼 모든 데이터가 저장됨
- 원본을 변경하지 않고 프록시의 기본 모델 순서(ordering)나 기본 관리자(default manager) 등을 변경할 수 있음



프록시 모델

- 일반 모델처럼 선언됨
- 장고에게 메타 클래스의 proxy 속성을 True로 설정하여 프록시 모델임을 알려야 함



```python
# Person 모델에 메소드를 추가
from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
   
# MyPerson 클래스는 상위 Person 클래스와 동일한 데이터베이스 테이블에서 작동
class MyPerson(Person):
    class Meta:
        proxy = True
        
    def do_something(self):
        pass
```

```shell
# Person의 새로운 인스턴스는 MyPerson을 통해 엑세스 할 수 있음 (그 반대도 가능)
>>> p = Person.objects.create(first_name="foobar")
>>> MyPerson.objects.get(first_name="foobar")
# <MyPerson: foobar>
```



```python
# Person 모델을 항상 ordering 하고 싶지는 않지만, 프록시를 사용할 때 last_name 속성으로 규칙적으로 ordering 하고자 할 경우
class OrderedPerson(Person):
    class Meta:
        ordering = ["last_name"]
        proxy = True
```

- 일반적인 Person 쿼리는 ordering 되지 않음
- OrderedPerson 쿼리는 last_name에 의해 ordering 됨



#### QuerySets still return the model that was requested

Person 객체를 쿼리 할 때마다 MyPerson 객체를 반환할 수는 없음

Person 객체에 대한 queryset은 해당 유형의 객체를 반환



> 프록시 객체의 요점은 원래 **Person**을 사용하는 코드는 그것을 사용하고, 사용자 코드는 포함시킨 확장기능을 사용할 수 있다는 것입니다 (다른 코드는 그다지 의존하지 않음). 그것은 **Person**(또는 다른 어떤 것이든)모델을 항상 당신이 만든 모델로 대체하는 방법이 아닙니다.



#### Base class restrictions

프록시 모델

- 정확히 하나의 비 추상적 모델 클래스를 상속해야 함
- 다른 데이터베이스 테이블의 행 사이에 연결을 제공하지 않음
  - 여러 개의 비 추상적 모델을 상속받을 수 없음
- 모델 필드가 정의되지 않은 임의의 수의 추상 모델 클래스를 상속받을 수 있음
- 공통의 비 추상 부모 클래스를 공유하는 임의의 수의 프록시 모델을 상속받을 수 있음



#### Proxy model managers

프록시 모델에 모델 관리자를 지정하지 않으면 모델 부모로부터 관리자를 상속받음

- 프록시 모델에서 관리자를 정의하면 그것이 기본값이 됨

- 부모 클래스에 정의된 관리자는 계속 사용할 수 있음



```python
# Person 모델을 쿼리할 때 사용되는 기본 관리자를 변경
from django.db import models

class NewManager(models.Manager):
    pass

class MyPerson(Person):
    objects = NewManager()
    
    class Meta:
        proxy = True
```

```python
# 기존 기본값을 바꾸지 않고 프록시에 새 관리자를 추가
# 새 관리자를 포함하는 기본 클래스를 작성하고 primary base class 다음으로 해당 관리자를 상속받음
class ExtraManagers(models.Model):
    secondary = NewManager()
    
    class Meta:
        abstract = True
        
class MyPerson(Person, ExtraManagers):
    class Meta:
        proxy = True
```



#### Differences between proxy inheritance and unmanaged models

프록시 모델 상속은 모델의 Meta 클래스에서 관리되는 특성을 사용하여 관리되지 않는 모델(unmanaged model)을 만드는 것처럼 비슷하게 보일 수 있음



unmanaged models

- Meta.db_table을 설정하면 관리되지 않는 모델을 만들어 기존 모델을 shadows 처리하고 Python 메소드를 추가할 수 있음
- 변경 작업을 수행할 경우, 반복적으로 구조가 일치하지 않는 오류 발생할 수 있음
  - 두 복사본을 동기화된 상태로 유지해야 함



proxy inheritance

- 프록싱 중인 모델과 정확히 동일하게 동작
- 부모 모델은 필드와 관리자를 직접 상속 (항상 부모 모델과 동기화됨)
- 일반적인 규칙
  1. Meta.managed = False
     - 기존 모델이나 데이터베이스 테이블을 미러링하고 원래 데이터베이스 테이블 열을 모두 원하는 않는 경우
     - 장고가 제어하지 않는 데이터베이스 뷰와 테이블을 모델링할 때 유용
  2. Meta.proxy = True
     - 모델의 파이썬 전용 동작을 변경하려고 하지만 원본과 동일한 필드를 모두 유지하려는 경우
     - 데이터를 저장할 때 프록시 모델이 원본 모델의 저장소 구조와 정확히 일치하도록 설정됨



### Multiple inheritance

장고 모델은 여러 부모 모델로부터 상속받을 수 있음

일반적인 파이썬 이름 해석 규칙(Name resolution rules)이 적용

특정 이름이 나타나는 첫 번째 클래스가 사용됨 (여러 부모가 메타 클래스를 포함)



"믹스 인(mix-in)" 클래스

- 여러 부모로부터 상속하기에 유용한 경우
- 믹스 인을 상속받은 모든 클래스에 특정 추가 필드나 메소드를 추가



```python
# 다중 상속
class Article(models.Model):
    # 명시적인 AutoField를 사용
    # 공통 id 기본 키 필드가 있는 여러 모델을 상속하는 것이 가능
    article_id = models.AutoField(primary_key=True)
    
class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    
class BookReview(Book, Article):
    pass
```

```python
# 공통 조상을 사용하여 AutoField를 유지
class Piece(models.Model):
    pass

class Article(Piece):
    # 각 상위 모델에서 공통 조상으로 명시적인 OneToOneField를 사용
    # 하위에서 상속되는 필드 사이의 충돌을 피함
    article_piece = models.OneToOneField(Piece, on_delete=models.CASCADE, parent_link=True)
    
class Book(Piece):
    book_piece = models.OneToOneField(Piece, on_delete=models.CASCADE, parent_link=True)
    
class BookReview(Book, Article):
    pass
```



### Field name "hiding" is not permitted

일반적인 Python 클래스 상속

- 자식 클래스가 부모 클래스의 모든 특성을 재정의 할 수 있음

장고 모델 상속

- 일반적으로 허용되지 않음
  - 비 추상적 모델에서 상속된 모델 필드
    - 기본 클래스에 author라는 필드가 있는 경우, 해당 기본 클래스에서 상속하는 클래스에서 다른 모델 필드를 만들거나 author라는 속성을 정의할 수 없음
  - 추상적 모델에서 상속된 모델 필드
    - 다른 필드나 값으로 재정의 하거나 field_name = None을 설정하여 제거할 수 있음

- 모델 관리자는 추상 기본 클래스에서 상속됨
  
  - 상속된 관리자가 참조하는 상속된 필드를 무시하면 버그가 발생할 수 있음
- 일부 필드는 모델의 추가 속성을 정의
  - ForeignKey: 필드 이름에 _id가 추가된 추가 속성과 외부 모델의 related_name 및 related_query_name을 정의
  - 추가 속성을 정의하는 필드가 변경되거나 제거된 경우, 추가 속성을 재정의 할 수 없음

- Field 인스턴스인 속성에만 적용 (파이썬이 인식하는 속성의 이름에만 적용)

  - 데이터베이스 열 이름을 수동으로 지정하는 경우, 다중 테이블 상속에서는 자식 및 조상 모델에 같은 열 이름을 표시할 수 있음

  - 두 개의 서로 다른 데이터베이스 테이블에 같은 이름의 열(column)들을 가짐

    ```python
    class Ancestor(models.Model):
        name = models.CharField(max_length=10, db_column='name')
        
    class Child(Ancestor):
        # 모델 클래스의 필드명(name)은 override 불가
        # DB 필드명(db_column)은 중복 가능
        # 모델 클래스의 필드명(속성명)은 중복 가능
        # 조상 테이블과 자식 테이블에 모두 'name' 필드가 있게 됨
        name2 = models.CharField(max_length=10, db_column='name')
    ```

- 조상 모델에서 존재하는 모델 필드를 재정의하면 FieldError 발생



> 상위 모델의 필드를 재정의하면 새 인스턴스의 초기화(**Model.__ init__**에서 초기화 할 필드 지정) 및 직렬화와 같은 영역에서 어려움이 발생합니다. 이것들은 일반적인 파이썬 클래스 상속에서 똑같은 방식으로 처리할 필요가 없는 기능이므로 Django모델 상속과 파이썬 클래스 상속에서의 이러한 차이는 Django에서 제멋대로 바꾼 것이 아닙니다.



## Organizing models in a package

manage.py startapp 명령

- `models.py` 파일을 포함하는 애플리케이션(app) 구조를 만듦

- 모델이 여러 개인 경우, models 패키지를 만들어 별도의 파일로 구성하여 사용

  ```python
  # models 디렉토리에 organic.py, synthetic.py가 있음
  from .organic import Person
  from .synthetic import Robot
  ```

  - `models.py`를 제거하고 myapp/models/ 디렉토리를 만들고 `__init__.py` 파일과 모델을 저장할 파일을 만듦
    - `__init__.py` 파일에서 모델을 가져옴
  - .models import *를 사용하지 않고 명시적으로 각 모델을 가져옴
    - 네임 스페이스가 복잡해지지 않아 코드를 읽기 쉽고 분석 도구를 유용하게 유지

