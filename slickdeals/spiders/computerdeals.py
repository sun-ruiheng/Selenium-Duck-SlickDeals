import scrapy
from scrapy_selenium import SeleniumRequest

class ComputerdealsSpider(scrapy.Spider):
    name = 'computerdeals'

    # Initial request, response passed into parse().
    def start_requests(self):
        yield SeleniumRequest(
            url='https://slickdeals.net/computer-deals/',
            wait_time=3,
            callback=self.parse
        )


    def parse(self, response):

        # Get all listed products on the page.
        products_list = response.xpath('//ul[@class="dealTiles categoryGridDeals blueprint"]/li')

        for product in products_list:

            # From every product, extract its name, URL, store and price. If its URL doesn't exist, skip the product. 

            product_name = product.xpath('.//a[@class="itemTitle bp-p-dealLink bp-c-link"]/text()').get()
            product_link = product.xpath('.//a[@class="itemTitle bp-p-dealLink bp-c-link"]/@href').get()
            if not product_link:
                continue
            product_store = product.xpath('.//span[@class="blueprint"]/button/text()').get()
            product_price = product.xpath('.//div[@class="itemPrice  wide "]/text()').get()


            yield {
                "Item": product_name,
                "Price": product_price,
                "Store": product_store,
                "URL": f"https://slickdeals.net{product_link}"
                # Because the link is not full but relative.
            }

        # Find the "Next" button in HTML.
        next_page = response.xpath('.//a[@data-role="next-page"]/@href').get()

        if next_page:
            # Traverse to next page if it exists.
            absolute_url = f"https://slickdeals.net{next_page}"

            yield SeleniumRequest(
                url=absolute_url,
                wait_time=3,
                callback=self.parse
            )