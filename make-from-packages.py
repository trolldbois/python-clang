import csv
import logging
import os
import shutil
import subprocess

import requests


class PackageBuilder():
    code_folder = 'clang'
    temp_folder = 'tmp'
    temp_package_filename = 'tmp_llvm_clang.deb'
    python_version = 'python3'
    setup_file = 'setup.py'
    setup_file_tpl = 'setup.py.tpl'

    def do(self, version, pyversion, url):
        version = str(version.strip())
        pyversion = str(int(pyversion.strip()))
        url = str(url.strip())
        logging.info(f'packaging version {version} from {url}')
        if pyversion == '2':
            self.python_version = 'python2.7'
        else:
            self.python_version = 'python3'
        self.clean()
        self.download(url)
        self.unpack()
        try:
            self.move()
        except FileNotFoundError as e:
            logging.error(f"error in package v:{version} pyv:{pyversion} url:{url}")
            raise RuntimeError(
                f"Package python-clang version {version} for python {pyversion} does "
                f"not contain clang python binding.") from e
        self.setup(version, pyversion)
        self.build_and_publish()
        logging.info(f'packaged version {version} for python {pyversion}')

    def clean(self):
        for d in [self.code_folder, self.temp_folder]:
            if os.path.exists(d):
                shutil.rmtree(d)
        if os.path.exists(self.setup_file):
            os.remove(self.setup_file)
        logging.debug("Working folders removed")

    def download(self, url):
        response = requests.get(url)
        logging.debug(f"download ret {response.status_code}")
        if response.status_code != 200:
            raise RuntimeError("download failed")
        if not os.path.exists(self.temp_folder):
            os.makedirs(self.temp_folder)
        filename = os.path.join(self.temp_folder, self.temp_package_filename)
        with open(filename, 'wb') as out:
            out.write(response.content)
        return filename

    def unpack(self):
        ret = subprocess.call(['dpkg-deb', '-xv', self.temp_package_filename, '.'], cwd=self.temp_folder,
                              stdout=subprocess.DEVNULL)
        logging.debug(f"unpack ret {ret}")
        if ret < 0:
            raise RuntimeError("unpack failed")

    def move(self):
        src = os.path.join(self.temp_folder, 'usr', 'lib', self.python_version, 'dist-packages', 'clang')
        dst = '.'
        shutil.move(src, dst)
        logging.debug(f"python package moved {src} -> {dst}")

    def setup(self, version, pyversion):
        with open(self.setup_file_tpl, 'r') as tpl:
            tpl_content = tpl.read()
        tpl_content = tpl_content.replace('%VERSION%', version)
        tpl_content = tpl_content.replace('%PYTHON_VERSION%', pyversion)
        with open(self.setup_file, 'w') as setup_file:
            setup_file.write(tpl_content)
        logging.debug(f"setup.py file writen for clang v:{version}, pyv:{pyversion}")

    def build_and_publish(self):
        ret = subprocess.call(['python', 'setup.py', 'sdist', 'bdist_wheel', 'upload'], stdout=subprocess.DEVNULL)
        logging.debug(f"build_and_publish ret {ret}")
        if ret < 0:
            raise RuntimeError("build_and_publish failed")


def main():
    logging.basicConfig(level=logging.INFO)

    builder = PackageBuilder()
    with open('packages.lst', newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        for version, pyversion, url in reader:
            if version.startswith('#'):
                continue
            builder.do(version, pyversion, url)


if __name__ == '__main__':
    main()
