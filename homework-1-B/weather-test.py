import time, codecs, os
from bs4 import BeauifulSoup




class weather:

	def __init__(self):

		self.url = "https://weather.com/weather/today/l/44091e3d4d7855d2183e907740d821fc43098928e45ef972d409ec01965b6363"


	def parse_html(self, url):
        """
        extracts raw html from input url
        :param str url: the url of the web page to be parsed
        :return: object containing html code of url
        """
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        #executable_path must be set to the
        driver = webdriver.Chrome(executable_path=self.chrome_driver, chrome_options=options)
        driver.get(url)
        time.sleep(3)
        page_html = driver.page_source
        page_soup = soup(page_html, 'html.parser')

        return page_soup

    def main(self):
    	"""
    	extract current weather info
    	"""

    	soup_html = self.parse_html(self.url)
    	print(soup_html)


if __name__ == "__main__":
	print('[+] Initializing Scrape...')
	weather().main()