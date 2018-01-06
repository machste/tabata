from setuptools import setup, find_packages

setup(
	name="tabata",
	version="0.1",
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
