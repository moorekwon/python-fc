# section 05-1
# beautifulsoup
# beautifulsoup 사용 스크랩핑(1)

from bs4 import BeautifulSoup

html = """
<html>
    <head>
        <title>The Dormouse's story</title>
    </head>
    <body>
        <h1>this is h1 area</h1>
        <h2>this is h2 area</h2>
        <p class="title"><b>The Dormouse's story</b></p>
        <p class="story">Once upon a time there were three little sisters
            <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>
            <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>
            <a data-io="link3" href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
        </p>
        <p class="story">story...</p>
    </body>
</html>
"""

# bs4 초기화
soup = BeautifulSoup(html, 'html.parser')
# print(soup)

# 타입 확인
# print('soup', type(soup))

# 코드 정리
# print('prettify', soup.prettify())

# h1 태그 접근
h1 = soup.html.body.h1
# print('h1', h1)

# p 태그 접근
p1 = soup.html.body.p
# print('p1', p1)

p2 = p1.next_sibling.next_sibling
# print('p2', p2)
# print()

# 텍스트 출력
# print('h1 >>', h1.string)
# print('p1 >>', p1.string)

# 함수 확인
# print(dir(p2))

# 다음 element 확인
# print(list(p2.next_elements))

# 반복 출력 확인
# for v in p2.next_elements:
#     print(v)
    
# Find, Find_all
# a 태그 모두 선택
links1 = soup.find_all('a', limit=2)
# print(links1)
# print()

# 타입 확인
# print('links', type(links1))

# dir 확인
# print(dir(links1))

# links2 = soup.find_all('a', class_="sister")
# links2 = soup.find_all('a', id="link2")
# links2 = soup.find_all('a', string="Tillie")
links2 = soup.find_all('a', string=["Elsie", "Tillie"])
# print(links2)

# for t in links1:
#     print('link1 >>', t.text)

# 처음 발견한 a 태그 선택
link1 = soup.find('a')
# print('links', type(link1), link1)

# dir 확인
# print(dir(link1))

# 태그 텍스트 출력
# print(link1.string)
# print(link1.text)

# 다중 조건
link2 = soup.find('a', {"class": "sister", "data-io": "link3"})
# print(link2)

# Select, Select_one
# CSS 선택자
# 태그 + 클래스 + 자식 선택자
b = soup.select_one("p.title > b")
# print(link1)
# print('b >>', b.string)
# print()

# 태그 + id 선택자
link1 = soup.select_one("a#link1")
# print(link1)
# print('link1 >>', link1.string)
# print()

# 태그 + 속성 선택자
link3 = soup.select_one('a[data-io="link3"]')
# print(link3)
# print('link3 >>', link3.string)

# 선택자에 맞는 전체 선택
# 태그 + 클래스 + 자식
storyA = soup.select('p.story > a')
# print('storyA', storyA)

# 태그 + 클래스 + 자식 + 태그 + 순서
secondA = soup.select('p.story > a:nth-of-type(2)')
# print('secondA', secondA)

# 태그 + 클래스
story = soup.select('p.story')
print('story2', story[1])