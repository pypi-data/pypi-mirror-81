import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Sandipan Roy",
    author_email="me@sandipan.ml",
    name='sandipan',
    license="MIT",
    description='Take it Easy; Make it Easy;',
    version='v0.0.10',
    long_description=README,
    url='https://sandipan.ml',
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires=['requests'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)
