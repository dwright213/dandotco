from setuptools import setup

setup(
	name='dandotco',
	packages=['dandotco'],
	version='1.0',
    author='Dan Wright',
    author_email='dan@danwright.co',
    description='A blogging software.',
    url='https://github.com/dwright213/dandotco',
    license='GPL-3.0-or-later',
	include_package_data=True,
	install_requires=[
		'flask>=0.12.3',
		'click>=7.1.2',
		'flask>=1.0.0',
		'httplib2>=0.19.0',
		'httpretty==0.8.14',
		'itsdangerous>=2.0',
		'jinja2>=2.11.3',
		'MarkupSafe>=2.0',
		'oauth2==1.9.0.post1',
		'uWSGI>=2.0.13.1',
		'werkzeug>=0.15.3'

	],
)