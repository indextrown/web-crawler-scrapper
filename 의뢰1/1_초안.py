import requests
from bs4 import BeautifulSoup
import os

# 이미지 저장 디렉토리 설정
if not os.path.exists("images"):
    os.makedirs("images")

#reponse는 객체이다
response = requests.get("https://sound-messe.com/exhibitors")
soup = BeautifulSoup(response.text, 'html.parser')
li = soup.select(".exhibitorslistwrap > .exhibitors")


cnt = 0
for i in li:
    if cnt == 2: break
    num = "".join(i.select_one("a > div > div").text.split())
    coop = "".join(i.select_one("a > div > span").text.split())
    link = i.select_one("a>figure>img").get("src")
    new_link = link if link.startswith("https://") else "https://sound-messe.com" + link

    filename = (num).replace("/", "_") + ".jpg"
    print(filename)
    print(new_link)
    print()

    img_response = requests.get(new_link)
    with open(os.path.join("images", filename), "wb") as img_file:
        img_file.write(img_response.content)

    cnt +=1

print(f"총 {cnt}개 파일을 추출하였습니다. ")

