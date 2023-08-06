from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

setup(
    name='unetpy',
    version='3.1.1',
    description='Unet Python Gateway',
    long_description=readme,
    author='Mandar Chitre, Prasad Anjangi',
    author_email='mandar@arl.nus.edu.sg, prasad@subnero.com',
    url='https://github.com/org-arl/unet-contrib/tree/master/unetsocket/python',
    license='BSD (3-clause)',
    python_requires='>=3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'numpy>=1.11',
        'fjagepy>=1.7.0'
    ]
)
