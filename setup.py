import setuptools
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "readme.md").read_text()


setuptools.setup(
	name='supermail',
	version='1.2',
	author="Flavio Piccoli",
	author_email="dros1986@gmail.com",
	description="An email client for reading and sending emails.",
	long_description=long_description,
    long_description_content_type='text/markdown',
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
