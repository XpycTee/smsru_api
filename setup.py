from setuptools import setup, find_packages


with open("README.md", "r", encoding='UTF-8') as f:
    readme = f.read()


requirements = ['aiohttp~=3.8.1']

setup(name='smsru_api',
      version='0.1.3',
      description='Python API для сервиса отправки сообщений sms.ru',
      url="https://git.xpyctee.ru/XpycTee/SmsRU_API",
      long_description=readme,
      long_description_content_type="text/markdown",
      license='GNU General Public License v3.0',
      packages=find_packages(),
      author="XpycTee",
      author_email='i@xpyctee.ru',
      keywords="sms.ru api sms ru",
      install_requires=requirements,
      python_requires='>=3.8',
      )
