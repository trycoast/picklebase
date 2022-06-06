from setuptools import setup


def readme():
    '''Read README file'''
    with open('README.rst') as infile:
        return infile.read()


setup(
    name='picklebase',
    version='0.1',
    description='A simple pickle-based database',
    long_description=readme().strip(),
    author='',
    author_email='',
    url='https://github.com/trycoast/picklebase',
    packages=['picklebase'],
    install_requires=['pydantic'],
    keywords=[
        'picklebase',
        'pickle',
        'database'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Software Development'
    ],
    include_package_data=True,
    zip_safe=False
)
