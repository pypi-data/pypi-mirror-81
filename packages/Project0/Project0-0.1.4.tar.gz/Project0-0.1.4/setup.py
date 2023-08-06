from setuptools import setup
from setuptools import find_packages

def readme():
  with open('README.rst') as f:
    return f.read()

setup(
  name='Project0',
  version='0.1.4',
  description='Offline vocal assistant and tts',
  long_description=readme(),
  classifiers=[
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Topic :: Multimedia :: Sound/Audio :: Capture/Recording',
    'Topic :: Multimedia :: Sound/Audio :: Speech',
    'Topic :: Text Processing',
    'Natural Language :: English',
    'Natural Language :: Italian',
  ],
  keywords='vocal assistant offline tts',
  url='http://github.com/fenrir77/project0',
  author='Fenrir77',
  author_email='fenrir7377@gmail.com',
  license='MIT',
  packages=find_packages(),
  install_requires=[
    'markdown',
    'PyAudio',
    'pyttsx3',
    'SpeechRecognition',
    'PocketSphinx'
  ],
  test_suite='nose.collectior',
  tests_require=['nose', 'nose-cover3'],
  entry_points={
    'console_scripts': ['main=project0.command_line:main'],
  },
  include_package_data=True,
  zip_safe=False
)