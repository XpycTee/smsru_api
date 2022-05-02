from setuptools import setup


with open("README.md", "r") as f:
    readme = f.read()


def requirements():
    with open("requirements.txt", "r") as req:
        return [r for r in req.read().split("\n") if r]


setup(name='smsru_api',
      version='0.1.0',
      description='Python API для сервиса отправки сообщений sms.ru',
      url="https://git.xpyctee.ru/XpycTee/SmsRU_API",
      long_description=readme,
      long_description_content_type="text/markdown",
      license='GNU General Public License v3.0',
      packages=['smsru_api'],
      author="XpycTee",
      author_email='i@xpyctee.ru',
      keywords="sms.ru api python sms ru",
      install_requires=requirements(),
      zip_safe=False
)
