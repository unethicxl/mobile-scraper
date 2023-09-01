# mobile-scraper

This is code that i got inspired from oio from https://antibot.blog rewritten in python.

Use it wisely.

to intergrate proxies in the project go to function scrape_models() and add the following code:
proxies = {
            'http': 'http://ip:port or http://username:password@ip:port',
            'https': 'http://ip:port or http://username:password@ip:port',
        }
response = requests.get(url, headers=headers, proxies=proxies)

same for function fill_data()
