from setuptools import setup, find_packages


with open("README.md", "r", encoding='UTF-8') as f:
    readme = f.read()


classifiers = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries",
]


setup(
      name='smsru_api',
      version='0.1.7',
      description='Python API для сервиса отправки сообщений sms.ru',
      url="https://github.com/XpycTee/smsru_api",
      long_description=readme,
      long_description_content_type="text/markdown",
      license='Apache License 2.0',
      packages=find_packages(),
      author="XpycTee",
      author_email='i@xpyctee.ru',
      classifiers=classifiers,
      keywords="sms.ru api sms ru",
      install_requires=['aiohttp'],
      python_requires='>=3.7',
)
