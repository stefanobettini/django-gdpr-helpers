from setuptools import setup

setup(
    name="GDPR helpers",
    version="v0.1-alpha",
    description="A Django app for managing GDPR compliancy",
    url="https://github.com/Arussil/django-gdpr-helpers",
    author="Piras Fabio",
    author_email="fabio@godsofweb.com",
    packages=["gdpr_helpers"],
    install_requires=["django>2.2,<3.0"],
    license = "BSD-3-Clause",
)
