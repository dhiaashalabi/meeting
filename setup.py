from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in meeting/__init__.py
from meeting import __version__ as version

setup(
	name="meeting",
	version=version,
	description="Prepare agenda, invite users and record minutes of meeting",
	author="Frappe",
	author_email="hello@frappe.io",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
