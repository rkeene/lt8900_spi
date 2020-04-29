import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="lt8900_spi", # Replace with your own username
	version="1.0",
	author="Roy Keene",
	author_email="pypi@rkeene.org",
	description="Python interface to an LT8900 connected via SPI",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://chiselapp.com/user/rkeene/repository/lt8900_spi/",
	packages=["lt8900_spi"],
	package_dir={"":"."},
	license="MIT License",
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
	install_requires=['spidev>=3.0.0']
)
