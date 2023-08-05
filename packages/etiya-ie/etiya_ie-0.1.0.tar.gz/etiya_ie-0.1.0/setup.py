from setuptools import setup

setup(
    name='etiya_ie',
    version='0.1.0',
    author='İrem Ekser',
    author_email='iremekser@gmail.com',
    packages=['etiya_ie'],
    url='https://github.com/iremekser/etiya-calisma',
    description='Etiya Bilgi Teknolojisi ve Hizmetleri için Intern sürecinde yazılan fonksiyonları içerir.',
    long_description=open('README.md').read(),
    install_requires=[
         "pyspark",
         "findspark",
         "psycopg2",
         "pandas",
         "pandasql",
    ],
)
