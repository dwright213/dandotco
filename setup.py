from setuptools import setup

setup(
	name='dandotco',
	packages=['dandotco'],
	include_package_data=True,
	install_requires=[
		'flask',
		'click==6.6',
		'Flask==0.11.1',
		'httplib2==0.9.2',
		'httpretty==0.8.14',
		'itsdangerous==0.24',
		'Jinja2==2.8',
		'MarkupSafe==0.23',
		'oauth2==1.9.0.post1',
		'uWSGI==2.0.13.1',
		'Werkzeug==0.11.11'

	],
)