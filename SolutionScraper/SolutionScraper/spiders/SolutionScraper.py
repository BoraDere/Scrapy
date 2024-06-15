import scrapy
from ..helper import Helper

class SolutionSpider(scrapy.Spider):
    name = 'solutionscraper'
    allowed_domains = [
        'www.technopat.net'
    ]
    start_urls = [
        'https://www.technopat.net/sosyal/uye/bora-dere.126747/solutions'
    ]


    def parse(self, response):
        prefix = 'https://www.technopat.net'
        solutions = response.css('h3.contentRow-title')

        for solution in solutions:
            link = prefix + solution.css('h3 a::attr(href)').get().split('post')[0]

            yield scrapy.Request(
                link,
                callback=self.parse_solution,
                meta = {
                    'link': link,
                }
            )


    def parse_solution(self, response):

        link = response.meta['link']
        title = response.css('div.p-title').xpath('//h1/text()').get()
        solution = response.css('article.message.message--post.message--solution.js-post.js-inlineModContainer')
        raw_message = solution.css('div.bbWrapper').get()
        processed_message = Helper.process_message(raw_message)
        datetime = solution.css('time.u-dt::attr(datetime)').get()
        datetime_str = solution.css('time.u-dt::attr(title)').get()

        yield {
            'link': link,
            'title': title,
            'processed_message': processed_message,
        }


    # def parse_reactions(self, response):
