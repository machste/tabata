from setuptools import setup, find_packages

setup(
	name="tabata",
	version="0.1",
	packages=find_packages(),
	entry_points={
		"console_scripts": [
			"tabata = tabata.scripts.creator:main"
		]
	}
)