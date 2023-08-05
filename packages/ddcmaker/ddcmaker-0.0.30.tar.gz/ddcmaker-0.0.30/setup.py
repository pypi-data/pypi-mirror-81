import os
import sys
import pathlib
import setuptools
from setuptools.command.install import install

path = sys.argv[0]

path = pathlib.Path(path).parent.as_posix()


class InstallDepend(install):
    """Customized setuptools install command"""

    def install_paramiko(self):
        # 安装paramiko
        os.system('sudo apt install python3-paramiko -y')

    def config_nginx(self):
        # '配置nginx配置文件'
        os.popen('sudo pkill -9 nginx')
        os.popen('sudo apt install nginx -y')

        target_file = "/etc/nginx/nginx.conf"
        nginx_cmd = '/usr/sbin/nginx'
        with open(f'{path}/config_file/start_file/nginx.conf') as file:
            with open(target_file, 'w') as conf_file:
                for line in file.readlines():
                    conf_file.write(line)

        # 重启nginx
        os.system(f'sudo {nginx_cmd} -s stop')
        os.system(f'sudo {nginx_cmd}')

        # 清理登录信息
        os.system(f'sudo rm /etc/motd')
        os.system(f'sudo touch /etc/motd')

    def config_origin(self):
        """配置源"""
        with open(f'{path}/config_file/start_file/pip.conf') as file:
            with open('/etc/pip.conf', 'w') as pip_file:
                for line in file.readlines():
                    pip_file.write(line)

    def config_upgrade_check(self):
        with open(f'{path}/config_file/start_file/upgrade_check.sh') as file:
            with open('/etc/upgrade_check.sh', 'w') as pip_file:
                for line in file.readlines():
                    pip_file.write(line)

    def config_install_check(self):
        with open(f'{path}/config_file/start_file/install_check.sh') as file:
            with open('/etc/install_check.sh', 'w') as pip_file:
                for line in file.readlines():
                    pip_file.write(line)

    def run(self):
        self.install_paramiko()
        install.run(self)
        self.config_nginx()
        self.config_origin()
        self.config_upgrade_check()
        self.config_install_check()


with open("describe.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

PACKAGES = setuptools.find_packages()

setuptools.setup(
    name='ddcmaker',
    version='0.0.30',
    description='This is a package for Raspberry pie system of maker  ',
    long_description=long_description,
    author='fastbiubiu',
    author_email='fastbiubiu@163.com',
    url='https://github.com/NocoldBob/robot',
    # package_dir=PACKAGE_DIR,
    include_package_data=True,
    install_requires=["bottle", "marshmallow", "pyserial", "numpy", 'requests', 'tornado', 'pigpio'],
    packages=PACKAGES,
    platforms='Linux',
    classifiers=[
        "Topic :: System :: Operating System Kernels :: Linux",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",

    ],
    cmdclass={
        'install': InstallDepend,
    },
    python_requires='>=3',
)
os.system('nohup sh -c "sleep 180 && sudo sh /etc/install_check.sh" >> /dev/null 2>&1 &')
