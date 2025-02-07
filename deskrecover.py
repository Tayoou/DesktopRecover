import subprocess
import ctypes
import os
import sys
import time


# 检查是否以管理员身份运行
class RegEditor(object):
    def is_admin(self):
        try:
            return os.geteuid() == 0  # 在类 Unix 系统中检查管理员权限
        except AttributeError:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0  # Windows 下检查管理员权限

    def reg_restore(self):
        # 提升权限，重新运行脚本
        if not self.is_admin():
            script = sys.argv[0]
            subprocess.run(['runas', '/user:Administrator', 'python deskrecover.py'], shell=True)
            sys.exit(0)
        # 保存注册表
        current_directory = os.getcwd()
        reg_file_path = os.path.join(current_directory, 'DesktopBak.reg')
        subprocess.run(['regedit', '/e', reg_file_path, r'HKEY_CURRENT_USER\Software\Microsoft\Windows\Shell\Bags\1\Desktop'], check=True)
        print(f"注册表已成功导出到 {reg_file_path}")

    def reg_read(self):
        if not self.is_admin():
            script = sys.argv[0]
            subprocess.run(['runas', '/user:Administrator', 'python', script] + sys.argv[1:], shell=True)
            sys.exit(0)
        # 应用注册表
        current_directory = os.getcwd()
        reg_file_path = os.path.join(current_directory, 'DesktopBak.reg')
        subprocess.run(['cmd', '/c', 'start', '/w', reg_file_path], check=True)

    def explore_restart(self):
        if not self.is_admin():
            script = sys.argv[0]
            subprocess.run(['runas', '/user:Administrator', 'python', script] + sys.argv[1:], shell=True)
            sys.exit(0)
        subprocess.run(["taskkill", "/F", "/IM", "explorer.exe"])
        os.startfile("explorer.exe")

