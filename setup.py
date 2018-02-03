from setuptools import setup, find_packages

setup(
	name="tabata",
	version="1.0",
	packages=find_packages(),
	install_requires=[
		"sox>=1.3.2",
	],
	entry_points={
		"console_scripts": [
			"tabata = tabata.scripts.creator:main"
		]
	}
)
