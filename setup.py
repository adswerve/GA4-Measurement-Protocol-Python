from setuptools import setup
import sys

try:
    long_description=open('DESCRIPTION.rst', 'rt').read()
except Exception:
    long_description="Google Analytics 4 Measurement Protocol in Python; an implementation of Google's Analytics 4 Measurement Protocol"

VERSION = '1.0.0'

setup(
    name = "ga4mp",
    description = "Google Analytics 4 Measurement Protocol Python Module",
    long_description = long_description,

    version = VERSION or 'NOTFOUND',

    author = 'Nate Bukowski',
    author_email = 'nate.bukowski@adswerve.com',

    url = 'https://github.com/adswerve/GA4-Measurement-Protocol-Python',
    download_url = "https://github.com/adswerve/GA4-Measurement-Protocol-Python" + VERSION,

    license = 'BSD',
    packages = ["ga4mp"],

    install_requires = [],

    zip_safe = True,
)
