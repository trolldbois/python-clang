import csv
import logging
import os
import shutil
import subprocess

import requests


class PackageBuilder:
    code_folder = 'clang'
    temp_folder = 'tmp'
    temp_package_filename = 'tmp_llvm_clang.deb'
    python_version = 'python3'
    setup_file = 'setup.py'
    setup_file_tpl = 'setup.py.tpl'

    def __init__(self, version, pyversion, url):
        self.version = version.strip()
        self.pyversion = str(int(pyversion.strip()))
        self.url = url.strip()

    def do(self):
        logging.info(f'packaging version {self.version} from {self.url}')
        if self.pyversion == '2':
            self.python_version = 'python2.7'
        else:
            self.python_version = 'python3'
        self.clean()
        self.download()
        self.unpack()
        try:
            self.move()
        except FileNotFoundError as e:
            logging.error(f"error in package v:{self.version} pyv:{self.pyversion} url:{self.url}")
            raise RuntimeError(
                f"Package python-clang version {self.version} for python {self.pyversion} does "
                f"not contain clang python binding.") from e
        self.setup()
        self.build()
        self.upload()
        logging.info(f'packaged version {self.version} for python {self.pyversion}')

    def clean(self):
        for d in [self.code_folder, self.temp_folder]:
            if os.path.exists(d):
                shutil.rmtree(d)
        if os.path.exists(self.setup_file):
            os.remove(self.setup_file)
        logging.debug("Working folders removed")

    def download(self):
        response = requests.get(self.url)
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
        ret = subprocess.run(['dpkg-deb', '-xv', self.temp_package_filename, '.'], cwd=self.temp_folder,
                              capture_output=True)
        logging.debug(f"unpack ret {ret}")
        if ret.returncode != 0:
            logging.error(ret.stderr)
            raise RuntimeError("unpack failed: ")

    def move(self):
        src = os.path.join(self.temp_folder, 'usr', 'lib', self.python_version, 'dist-packages', 'clang')
        dst = '.'
        shutil.move(src, dst)
        logging.debug(f"python package moved {src} -> {dst}")

    def setup(self):
        with open(self.setup_file_tpl, 'r') as tpl:
            tpl_content = tpl.read()
        tpl_content = tpl_content.replace('%VERSION%', self.version)
        tpl_content = tpl_content.replace('%PYTHON_VERSION%', self.pyversion)
        with open(self.setup_file, 'w') as setup_file:
            setup_file.write(tpl_content)
        logging.debug(f"setup.py file writen for clang v:{self.version}, pyv:{self.pyversion}")

    def build(self):
        # https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html
        ret = subprocess.run(['python', '-m', 'build'], capture_output=True)
        logging.debug(f"build ret {ret}")
        if ret.returncode != 0:
            logging.error(ret.stderr)
            raise RuntimeError("build failed")

    def upload(self):
        # https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html
        ret = subprocess.run(['twine', 'upload', f'dist/clang-{self.version}*'], capture_output=True)
        logging.debug(f"upload ret {ret}")
        if ret.returncode != 0:
            logging.error(ret.stderr)
            raise RuntimeError("upload failed")


def main():
    logging.basicConfig(level=logging.INFO)

    with open('packages.lst', newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        for version, pyversion, url in reader:
            if version.startswith('#'):
                continue
            builder = PackageBuilder(version, pyversion, url)
            builder.do()


if __name__ == '__main__':
    main()
