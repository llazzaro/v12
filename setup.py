import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'twisted',
    'pyopenssl',
]

setup(name='v12',
      version='0.1',
      description='v12: Asyc WWW',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Leonardo Lazzaro',
      author_email='lazzaroleonardo@gmail.com',
      url='www.lazzaroleonardo.com.ar',
      keywords='www asynchronic',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="v12",
      )
