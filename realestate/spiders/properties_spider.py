# import scrapy

# class PropertiesSpider(scrapy.Spider):
#     name = "properties"  # Name of the spider
#     start_urls = [
#         "https://www.radiancerealty.in/projects/chennai/radiance-solitaire/"
#     ]

#     def parse(self, response):
#         # Extract the last and second last parts of the URL for name and location
#         url_parts = [part for part in response.url.strip('/').split('/')]
#         location = url_parts[-2] if len(url_parts) >= 2 else None
#         name = url_parts[-1] if len(url_parts) >= 1 else None

#         # Extract table data safely with default values
#         price = response.css("td:nth-of-type(1)::text").get(default='N/A').strip()
#         area = response.css("td:nth-of-type(2)::text").get(default='N/A').strip()
#         bedrooms = response.css("td:nth-of-type(3)::text").get(default='N/A').strip()

#         yield {
#             "name": name,  # Extracted property name from the URL
#             "location": location,  # Extracted location from the URL
#             "price": price,  # Price data if available
#             "area": area,  # Area data if available
#             "bedrooms": bedrooms,  # Bedrooms data if available
#             "url": response.url,  # Full URL of the listing
#         }
# import scrapy

# class PropertiesSpider(scrapy.Spider):
#     name = "properties"  # Name of the spider
#     start_urls = [
#         "https://www.radiancerealty.in/projects/chennai/radiance-flourish/"
#     ]

#     def parse(self, response):
#         # Extract the last and second last parts of the URL for name and location
#         url_parts = [part for part in response.url.strip('/').split('/')]
#         location = url_parts[-2] if len(url_parts) >= 2 else None
#         name = url_parts[-1] if len(url_parts) >= 1 else None

#         # Extract all rows from the table
#         rows = response.css("table tr")  # Adjust the CSS selector for the table rows

#         for row in rows:
#             # Extract data from each row
#             type_ = row.css("td:nth-of-type(1)::text").get(default='N/A').strip()
#             built_up_area = row.css("td:nth-of-type(2)::text").get(default='N/A').strip()
#             rate_per_sqft = row.css("td:nth-of-type(3)::text").get(default='N/A').strip()
#             price = row.css("td:nth-of-type(4)::text").get(default='N/A').strip()

#             # Yield the data for each row
#             yield {
#                 "name": name,  # Extracted property name from the URL
#                 "location": location,  # Extracted location from the URL
#                 "type": type_,  # Type of property (e.g., 2BHK, 3BHK)
#                 "built_up_area": built_up_area,  # Built-up area
#                 "rate_per_sqft": rate_per_sqft,  # Rate per sq.ft.
#                 "price": price,  # Price of the property
#                 "url": response.url,  # Full URL of the listing
#             }


import scrapy

class PropertiesSpider(scrapy.Spider):
    name = "properties"  # Name of the spider
    start_urls = []  # We will dynamically pass the start URL from the Flask API
    print('hii')

    def __init__(self, *args, **kwargs):
        # When the spider is initialized, get the 'url' from the arguments
        url = kwargs.get('url')
        print('hii',url)
        if url:
            self.start_urls = [url]  # Set the start URL dynamically
        super(PropertiesSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        print('hiii13')
        # Extract the last and second last parts of the URL for name and location
        url_parts = [part for part in response.url.strip('/').split('/')]
        location = url_parts[-2] if len(url_parts) >= 2 else None
        name = url_parts[-1] if len(url_parts) >= 1 else None

        # Extract all rows from the table
        rows = response.css("table tr")  # Adjust the CSS selector for the table rows

        for row in rows:
            # Extract data from each row
            type_ = row.css("td:nth-of-type(1)::text").get(default='N/A').strip()
            built_up_area = row.css("td:nth-of-type(2)::text").get(default='N/A').strip()
            rate_per_sqft = row.css("td:nth-of-type(3)::text").get(default='N/A').strip()
            price = row.css("td:nth-of-type(4)::text").get(default='N/A').strip()

            # Yield the data for each row
            yield {
                "name": name,  # Extracted property name from the URL
                "location": location,  # Extracted location from the URL
                "type": type_,  # Type of property (e.g., 2BHK, 3BHK)
                "built_up_area": built_up_area,  # Built-up area
                "rate_per_sqft": rate_per_sqft,  # Rate per sq.ft.
                "price": price,  # Price of the property
                "url": response.url,  # Full URL of the listing
            }