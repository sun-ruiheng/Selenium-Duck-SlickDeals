# This example.py tests functionality of scrapy-selenium using duckduckgo.
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys

class ExampleSpider(scrapy.Spider):
    name = 'example'

    # Override the start_requests method with a Selenium Request
    def start_requests(self):
        yield SeleniumRequest(
            url="https://duckduckgo.com",
            wait_time=3,
            screenshot=True,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta["driver"]
        # Search query box
        search_input = driver.find_element_by_xpath("//input[@id='search_form_input_homepage']")
        search_input.send_keys('World Cup 2022')
        search_input.send_keys(Keys.ENTER)

        # Using Selector, we turn the acquired results page's HTML into a response so as to retrieve info from it down below
        html = driver.page_source
        response_object = Selector(text=html)

        # We use xpath on the new response_object, not original response because response is limited to the very first response of the program, not later pages.
        links = response_object.xpath("//div[@class='result__extras__url']/a")
        for link in links:
            yield {
                'URL': link.xpath(".//@href").get()
            }
