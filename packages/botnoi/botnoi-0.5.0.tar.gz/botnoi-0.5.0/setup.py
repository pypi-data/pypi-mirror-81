from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='botnoi',
    version='0.5.0',
    description='BOTNOI',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Winn Voravuthikunchai',
    author_email='vwinnv@gmail.com',
    keywords=['NLP'],
    include_package_data=True,
    url='https://github.com/winn/botnoi',
    download_url='https://pypi.org/project/botnoinlp/'
)

install_requires = [
'pandas',
'pillow',
'pythainlp',
'gensim',
'pymongo[tls,srv]',
'SpeechRecognition',
'wave',
'audioread'

]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
