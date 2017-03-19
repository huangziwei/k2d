from setuptools import setup, find_packages

setup(name='k2d',
      version='0.1.2',
      author='Ziwei Huang',
      author_email='huang-ziwei@outlook.com',
      url='https://github.com/huangziwei/k2d',
      packages=['k2d'],
      scripts=['bin/k2d'],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'],
     )