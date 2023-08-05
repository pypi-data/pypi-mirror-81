from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='chipp',
  version='0.2',
  description='A AI STORE',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  author='potatochip',
  author_email='potatochip.tech@gmail.com',
  url = 'https://github.com/potatochip-tech/chip',   
  download_url = 'https://github.com/potatochip-tech/chip/archive/v_01.tar.gz',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator', 
  packages=[''],
  install_requires=[''] 
)