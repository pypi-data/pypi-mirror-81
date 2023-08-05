# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='python-thaibulksms',
    version='0.0.2',
    author=u'Jon Combe',
    author_email='jon@salebox.io',
    packages=['pythonthaibulksms'],
    include_package_data=True,
    install_requires=[],
    url='https://github.com/joncombe/python-thaibulksms',
    license='BSD licence, see LICENCE file',
    description='Python functions to send SMSs via ThaiBulkSMS.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    zip_safe=False,
)
