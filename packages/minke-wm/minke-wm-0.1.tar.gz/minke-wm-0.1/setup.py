from setuptools import setup

def readme():
  with open('README.md') as f:
    return f.read()

setup(name='minke-wm',
    version='0.1',
    description='A minimal, keyboard-centric window manager',
    long_description=readme(),
    keywords='',
    url='http://gitlab.com/OldIronHorse/minkie',
    author='Simon Redding',
    author_email='s1m0n.r3dd1ng@gmail.com',
    license='GPL3',
    packages=[
            'minke'
        ],
    install_requires=[
            'xlib'
        ],
    scripts=[
            'bin/minke_wm'
        ],
    python_requires='>=3.6',
    test_suite='nose.collector',
    tests_require=['nose', 'nosy'],
    include_package_data=True,
    zip_safe=False)
