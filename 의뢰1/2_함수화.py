import requests
from bs4 import BeautifulSoup
import os
import time

# 이미지 저장 디렉토리 설정
if not os.path.exists("images"):
    os.makedirs("images")

# img download
def download_image(img_url, filename):
    with open(os.path.join("images", filename), "wb") as img_file:
        img_file.write(img_url.content)

#reponse는 객체이다
url = "https://sound-messe.com/exhibitors"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
li = soup.select(".exhibitorslistwrap > .exhibitors")

start_time = time.time()
cnt = 0
for i in li:
    num = "".join(i.select_one("a > div > div").text.split())
    coop = "".join(i.select_one("a > div > span").text.split())
    link = i.select_one("a>figure>img").get("src")
    new_link = link if link.startswith("https://") else "https://sound-messe.com" + link

    filename = (num).replace("/", "_") + ".jpg"
    img_response = requests.get(new_link)
    download_image(img_response, filename)
    
    # print(filename)
    # print(new_link)
    # print()

    cnt +=1
end_time = time.time()
total_time = end_time - start_time

print(f"총 {cnt}개 파일을 추출하였습니다. ")
print(f"총 소요 시간: {total_time}초")
