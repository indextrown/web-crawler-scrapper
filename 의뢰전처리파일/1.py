import importlib
import platform

# 크롬 드라이버 모둔 에러 경우의 수
# 의존성 패키지 전체 다운 모듈화
class PackageManager:
    def __init__(self):
        self.required_modules = [
            "requests",
            "bs4",
            "selenium",
            "webdriver_manager",
            "chromedriver_autoinstaller",
            "pyautogui",
            "openpyxl"
            # ... add more modules if needed
        ]

        self.max_module_length = max(len(module) for module in self.required_modules)

    def import_module(self, module):
        try:
            importlib.import_module(module)
            spaces_after_module = " " * (self.max_module_length - len(module))
            print("# {} 모듈을 성공적으로 임포트했습니다.{} #".format(module, spaces_after_module))
        except ImportError:
            self.install_module(module)

    def install_module(self, module):
        install_message = "'{}' 모듈이 설치되어 있지 않습니다. Installing now...".format(module)
        spaces_after_module = " " * (self.max_module_length - len(module))
        print("# {}{} #".format(install_message, " " * (50 - len(install_message)) + spaces_after_module))
        try:
            subprocess.check_call(["pip", "install", module])
            success_message = "'{}' 모듈 설치에 성공했습니다.".format(module)
            spaces_after_module = " " * (self.max_module_length - len(module))
            print("# {}{} #".format(success_message, " " * (50 - len(success_message)) + spaces_after_module))
        except Exception as e:
            error_message = "'{}' 모듈 설치 중 에러 발생: {}".format(module, e)
            spaces_after_module = " " * (self.max_module_length - len(module))
            print("# {}{} #".format(error_message, " " * (50 - len(error_message)) + spaces_after_module))

    def check_and_install_modules(self):
        system = platform.system()
        if system == "Windows":
            print("현재 시스템은 Windows입니다.")
            self.win_required_modules_installed()

        elif system == "Darwin":
            print("현재 시스템은 macOS입니다.")
            self.mac_required_modules_installed()

        else:
            print("지원되지 않는 운영체제입니다.")
            try:
                print("맥 os로 시도중")
                self.mac_required_modules_installed()
            except:
                print("지원 불가로 강제종료")
                

    def mac_required_modules_installed(self):
        print('#' * (self.max_module_length + 38))
        print("#                필요한 패키지 확인합니다. . .                 #")
        print("#                                                              #")
        for module in self.required_modules:
            self.import_module(module)
        print('#' * (self.max_module_length + 38))
        print()

    def win_required_modules_installed(self):
        print('#' * (self.max_module_length + 32))
        print("#                필요한 패키지 확인합니다. . .               #")
        print("#                                                        #")
        for module in self.required_modules:
            self.import_module(module)
        print('#' * (self.max_module_length + 33))
        print()
package_manager = PackageManager()
package_manager.check_and_install_modules()

