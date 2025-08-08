from setuptools import setup, find_packages

NAME = 'smsru_api'
VERSION = '1.2'

DESCRIPTION = '[A]sync Python API для сервиса отправки сообщений sms.ru'
URL = 'https://github.com/XpycTee/smsru_api'
LICENSE = 'Apache License 2.0'

AUTHOR = 'XpycTee'
AUTHOR_EMAIL = 'i@xpyctee.ru'

with open("pypidesc.md", "r", encoding='UTF-8') as f:
    readme = f.read()

keywords = [
    "async", "sync", "aio", 
    "sms.ru", "sms", "ru", "smsru", 
    "sms-verification", "verification", "sms-messages", "messages", 
    "api", "api-client", 
    "http"
]

classifiers = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: Implementation :: PyPy",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries",
]

with open("requirements.txt", "r", encoding='UTF-8') as f:
    requieres = [line.rstrip('\n') for line in f]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    url=URL,
    long_description=readme,
    long_description_content_type="text/markdown",
    license=LICENSE,
    packages=find_packages(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    classifiers=classifiers,
    keywords=keywords,
    install_requires=requieres,
    python_requires='>=3.8',
)
