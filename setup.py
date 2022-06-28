import setuptools

setuptools.setup(
	name='EmailClient',
	version='1.0',
	author="Flavio Piccoli",
	author_email="dros1986@gmail.com",
	description="An email client for reading and sending emails.",
	# long_description="An email client for reading and sending emails.",
	# long_description_content_type="text/markdown",
	url="https://github.com/dros1986/EmailClient",
	packages=setuptools.find_packages('.'),
	#packages=setuptools.find_packages(include=['src']),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	install_requires=[
          'imapclient'
    ],
	python_requires='>=3',
 )
