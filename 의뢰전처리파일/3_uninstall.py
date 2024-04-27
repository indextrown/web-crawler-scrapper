import subprocess

def uninstall_packages(package_names):
    for package_name in package_names:
        try:
            subprocess.check_call(["pip", "uninstall", package_name.strip(), "-y"])
            print(f"{package_name.strip()} 라이브러리를 성공적으로 삭제했습니다.")
        except subprocess.CalledProcessError as e:
            print(f"{package_name.strip()} 라이브러리 삭제 중 에러가 발생했습니다: {e}")

if __name__ == "__main__":
    package_names = ["requests", "selenium", "pyautogui"]
    uninstall_packages(package_names)
