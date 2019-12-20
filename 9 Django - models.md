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



#### One-to-one relationships

### Models across files

### Field name restrictions

### Custom field types



## Meta options



## Model attributes



## Model methods

### Overriding predefined model methods

### Executing custom SQL



## Model inheritance

### Abstract base classes

#### Meta inheritance

#### Be careful with related_name and related_query_name

### Multi-table inheritance

#### Meta and multi-table inheritance

#### Inheritance and reverse relations

#### Specifying the parent link field

### Proxy models

#### QuerySets still return the model that was requested

#### Base class restrictions

#### Proxy model managers

#### Differences between proxy inheritance and unmanaged models

### Multiple inheritance

### Field name "hiding" is not permitted



## Organizing models in a package