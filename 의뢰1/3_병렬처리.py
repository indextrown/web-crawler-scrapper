import os
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import time

# 이미지 저장 디렉토리 설정
if not os.path.exists("images"):
    os.makedirs("images")

def download_image(img_url, filename):
    with open(os.path.join("images", filename), "wb") as img_file:
        img_file.write(img_url.content)

def process_exhibitor(i):
    num = "".join(i.select_one("a > div > div").text.split())
    link = i.select_one("a>figure>img").get("src")
    new_link = link if link.startswith("https://") else "https://sound-messe.com" + link
    filename = (num).replace("/", "_") + ".jpg"
    img_response = requests.get(new_link)
    download_image(img_response, filename)
    return filename

# 페이지 요청
url = "https://sound-messe.com/exhibitors"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
li = soup.select(".exhibitorslistwrap > .exhibitors")

start_time = time.time()
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(process_exhibitor, item) for item in li]
    filenames = [future.result() for future in futures]
end_time = time.time()
total_time = end_time - start_time

print(f"총 {len(filenames)}개 파일을 추출하였습니다.")
print(f"총 소요 시간: {total_time}초")