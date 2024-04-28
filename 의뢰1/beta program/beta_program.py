import importlib
import platform
import subprocess

class PackageManager:
    def __init__(self):
        self.required_modules = [
            "requests",
            "bs4",
            # ... add more modules if needed
        ]
        self.max_module_length = max(len(module) for module in self.required_modules)

    def import_module(self, module):
        try:
            importlib.import_module(module)
            print(f"# {module} 모듈을 성공적으로 임포트했습니다.{' ' * (self.max_module_length - len(module))} #")
        except ImportError:
            self.install_module(module)

    def install_module(self, module):
        install_message = f"'{module}' 모듈이 설치되어 있지 않습니다. Installing now..."
        print(f"# {install_message}{' ' * (50 - len(install_message))} #")
        try:
            #subprocess.check_call(["pip", "install", module])
            subprocess.check_call(["pip", "install", module], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            success_message = f"'{module}' 모듈 설치에 성공했습니다."
            print(f"# {success_message}{' ' * (50 - len(success_message))} #")
            self.import_module(module)  # 설치 후에 import
        except Exception as e:
            error_message = f"'{module}' 모듈 설치 중 에러 발생: {e}"
            print(f"# {error_message}{' ' * (50 - len(error_message))} #")

    def check_and_install_modules(self):
        system = platform.system()
        if system == "Windows":
            print("현재 시스템은 Windows입니다.")
            self.check_modules()

        elif system == "Darwin":
            print("현재 시스템은 macOS입니다.")
            self.check_modules()

        else:
            print("지원되지 않는 운영체제입니다.")
            try:
                print("맥 os로 시도중")
                self.check_modules()
            except:
                print("지원 불가로 강제종료")

    def check_modules(self):
        print('#' * (self.max_module_length + 38))
        print("#                필요한 패키지 확인합니다. . .                 #")
        print("#                                                              #")
        for module in self.required_modules:
            self.import_module(module)
        print('#' * (self.max_module_length + 38))
        print()

package_manager = PackageManager()
package_manager.check_and_install_modules()


import os
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import time


# 이미지 저장 디렉토리 설정
def folder(folderpath):
    if not os.path.exists(folderpath):
        os.makedirs(folderpath)

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

def start(cnt = 5):
    # 페이지 요청
    url = "https://sound-messe.com/exhibitors"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    li = soup.select(".exhibitorslistwrap > .exhibitors")

    start_time = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_exhibitor, item) for item in li[:cnt]]
        filenames = [future.result() for future in futures]
    end_time = time.time()
    total_time = end_time - start_time

    print(f"총 {len(filenames)}개 파일을 추출하였습니다.")
    print(f"총 소요 시간: {total_time}초")

if __name__ == "__main__":
    # 이미지 폴더는 해당 코드가 실행된/저장된 위치에 생성됩니다. images대신 다른 이름 수정 가능합니다. 
    folderpath = "images"
    folder(folderpath)
    start()