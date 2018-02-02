import scrapy
from scrapy.item import Item

class ImgData(Item):
    date=scrapy.Field()
    weatherData=scrapy.Field()
    dailyWeather=scrapy.Field()

class AccuWeatherSpider(scrapy.Spider):
    name = "accu_weather"

    def start_requests(self):
        urlStart = 'https://www.wunderground.com/history/airport/LDSH/'
        urlEnd = '/DailyHistory.html?req_city=Split&req_state=17&req_statename=Croatia&reqdb.zip=00000&reqdb.magic=1&reqdb.wmo=14445'

        urls = [
            urlStart + '2017/4/19' + urlEnd
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        dailyWeather = ImgData()
        dailyWeather['weatherData'] = []

        day = response.css('select.day option[selected="selected"]::text').extract_first()
        month = response.css('select.month option[selected="selected"]::attr(value)').extract_first()
        year = response.css('select.year option[selected="selected"]::text').extract_first()
        date = day + '-' + month + '-' + year
        dailyWeather['date'] = date

        for tableRow in response.css('table#historyTable tr'):
            title = tableRow.css('td.indent span::text').extract_first()
            value = tableRow.css('td span.wx-value::text').extract_first()

            if title:
                dailyWeather['weatherData'].append({title: value})

        yield dailyWeather

        next_page = response.css('div.next-link a::attr(href)').extract_first()
        if next_page is not None and '15-9-2017' not in date:
            yield response.follow(next_page, self.parse)
