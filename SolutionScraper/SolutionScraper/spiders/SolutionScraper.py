import scrapy
from ..helper import Helper

prefix = 'https://www.technopat.net'

# TODO: decide what the format should be
reactions = {
    1: [0, 'Beğen'],
    2: [0, 'Muhteşem'],
    3: [0, 'Hahaha'],
    4: [0, 'İnanılmaz'],
    5: [0, 'Üzgün'],
    6: [0, 'Kızgın'],
    7: [0, 'Düşündürücü'],
    8: [0, 'Beğenmedim'],
}


class SolutionSpider(scrapy.Spider):
    name = 'solutionscraper'
    allowed_domains = [
        'www.technopat.net'
    ]
    start_urls = [
        'https://www.technopat.net/sosyal/uye/bora-dere.126747/solutions'
    ]


    def parse(self, response):
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

        if solution.css('a.reactionsBar-link::attr(href)').get():
            reaction_link = prefix + str(solution.css('a.reactionsBar-link::attr(href)').get())
            yield scrapy.Request(
                reaction_link,
                callback=self.parse_reactions,
                meta = {
                    'link': link,
                    'title': title,
                    'processed_message': processed_message,
                    'datetime': datetime,
                    'datetime_str': datetime_str,
                }
            )

        else:
            yield {
                'link': link,
                'title': title,
                'processed_message': processed_message,
                'datetime': datetime,
                'datetime_str': datetime_str,
                'reactions': reactions,
            }

    def parse_reactions(self, response):
        link = response.meta['link']
        title = response.meta['title']
        processed_message = response.meta['processed_message']
        datetime = response.meta['datetime']
        datetime_str = response.meta['datetime_str']
        
        for reaction in response.css('li.block-row.block-row--separated'):
            reaction_id = reaction.css('div.contentRow-extra span::attr(data-reaction-id)').get()
            # reaction_sender = response.css('h3.contentRow-header a::text').get()
            reactions[int(reaction_id)][0] += 1

        yield {
            'link': link,
            'title': title,
            'processed_message': processed_message,
            'datetime': datetime,
            'datetime_str': datetime_str,
            'reactions': reactions
        }