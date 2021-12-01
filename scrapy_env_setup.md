# scrapy environment setup
This guide demonstrates how to setup the environment to run the scraper to get data from PoLyInfo.

### 1. install scrapy
#### If you are using Windows
Make sure you have miniconda or anaconda installed, then execute

	conda create --name scrapy
	conda activate scrapy
	conda install -c conda-forge scrapy

	
#### If you are using MacOS or Linux
If you have not installed virtualenv, you can install it with

	pip install virtualenv
	
Execute the following in the project folder to create, enter, and install scrapy in a virtual environment

	cd polyinfo_scraper
	virtualenv scrapy
	source scrapy/bin/activate
	pip install Scrapy
	

  ---
#### troubleshoot

	AttributeError: type object 'SettingsFrame' has no attribute 'ENABLE_CONNECT_PROTOCOL'

If you see the above error on Windows using conda, try to reinstall h2 with

	pip uninstall h2
	pip install h2==3.2.0

### 2. run spider
Assuming you are in polyinfo_scraper/ in the project folder, start scraping with

	cd polyinfo_scraper/spiders
	scrapy runspider polyinfo.py

When you are done scraping, exit the conda/virtual environment

	deactivate
