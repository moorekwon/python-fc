# section 05-1
# beautifulsoup
# beautifulsoup 사용

from bs4 import BeautifulSoup

html = """
<html>
    <head>
        <title>The Dormouse's story</title>
    </head>
    <body>
        <h1>This is h1 area.</h1>
        <h2>This is h2 area.</h1>
        <p class="title"><b>The Dormouse's story</b></p>
        <p class="story">Once upon a time, there were three little sisters.
            <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>
            <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>
            <a data-io="link3" href="http://example.com/little" class="sister" id="link3">Little</a>
        </p>
        <p class="story">
            story ...
        </p>
    </body>
</html>
"""

# 예제 1 (BeautifulSoup 기초)
# bs4 초기화
soup = BeautifulSoup(html, 'html.parser')
# print(soup)

# 타입 확인
# print('soup', type(soup))
# print('prettify', soup.prettify())

# h1 태그 접근
h1 = soup.html.body.h1
# print('h1', h1)

# p 태그 접근
# p1 = soup.html.body.p
# print('p1', p1)

# 다음 태그
# p2 = p1.next_sibling.next_sibling
# print('p2', p2)

# 텍스트 출력 1
print('h2>>', h1.string)
# print('p1>>', p1.string)

# 함수 확인
# print(dir(h1))

# 다음 element 확인
print(list(h1.next_element))
print(h1.next_element)