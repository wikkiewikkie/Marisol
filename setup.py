"""
Marisol
=======
Python library that can be used to add bates numbers to existing PDF files.

Links
=====
* `Source Code <https://github.com/wikkiewikkie/Marisol>`_
* `Issues <https://github.com/wikkiewikkie/Marisol/issues>`_
"""
import marisol

from setuptools import setup

install_requires = [
    'pypdf2==1.27.9',
    'reportlab==3.3.0'
]

setup(
    name='Marisol',
    version=marisol.__version__,
    url='http://github.com/wikkiewikkie/Marisol',
    license=marisol.__license__,
    author=marisol.__author__,
    author_email=marisol.__email__,
    description='Add bates numbers, text stamps, and redactions to existing PDF files',
    packages=['marisol'],
    zip_safe=True,
    platforms='any',
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Legal Industry',
        'License :: OSI Approved',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Office/Business',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
