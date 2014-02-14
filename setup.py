from setuptools import setup, find_packages

version = '0.1'

setup(
	name='ckanext-s3archive',
	version=version,
	description='s3archive extension for customising CKAN',
	long_description='',
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='Seb Bacon',
	author_email='seb.bacon@gmail.com',
	url='',
	license='',
	packages=find_packages(exclude=['ez_setup', 's3archives', 'tests']),
	namespace_packages=['ckanext', 'ckanext.s3archive'],
	include_package_data=True,
	zip_safe=False,
	install_requires=['boto'],
	entry_points=\
	"""
        [ckan.plugins]
	    s3archive=ckanext.s3archive.plugin:s3archivePlugin

        [paste.paster_command]
        s3archive=ckanext.s3archive.commands:s3archiveCommand
	""",
)
