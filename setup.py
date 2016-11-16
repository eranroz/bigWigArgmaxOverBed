try:
    from setuptools import setup
except:
    from distutils.core import setup
setup(
    name='bigWigArgmaxOverBed',
    version='0.1',
    scripts=['bigWigArgmaxOverBed.py'],
    url='https://github.com/eranroz/bigWigArgmaxOverBed',
    license='MIT',
    author='eranroz',
    author_email='eranroz@cs.huji.ac.il',
    description='Find argmax within bigWig for each bed',
    install_requires=['bx-python', 'pandas']

)
