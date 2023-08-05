from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()

setup(
    name="django-bonus",
    packages=["django_bonus"],
    package_dir={"django_bonus": "django_bonus"},
    package_data={
        "django_bonus": [
            "__init__.py",
            "templatetags/__init__.py",
            "templatetags/django_bonus.py",
        ]
    },
    version="0.1.0",
    description="Bonus Features for Django: More Template Filters like Replace",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Daniel J. Dufour",
    author_email="daniel.j.dufour@gmail.com",
    url="https://github.com/DanielJDufour/django-bonus",
    download_url="https://github.com/DanielJDufour/django-bonus/tarball/download",
    keywords=["django", "filter", "liquid", "template"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=["django"],
)
