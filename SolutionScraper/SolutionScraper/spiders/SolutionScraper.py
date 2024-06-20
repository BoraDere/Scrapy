import scrapy
from ..helper import Helper

prefix = 'https://www.technopat.net'

# TODO: fix the shit outta it...

# TODO: handle more than one pages in reactions (tricky)
# TODO: handle more than one pages in solutions (easy)
# TODO: add reaction senders (easy)
# TODO: separate function for map updating (easy)
# TODO: check all bb codes. spoiler... remove code title=...

def initialize_reactions(d):
    for i in d:
        d[i] = [0, []]


reactions = {
    'Beğen': [0, []],
    'Muhteşem': [0, []],
    'Hahaha': [0, []],
    'İnanılmaz': [0, []],
    'Üzgün': [0, []],
    'Kızgın': [0, []],
    'Düşündürücü': [0, []], 
    'Beğenmedim': [0, []],
}

r_map = {
    1: 'Beğen',
    2: 'Muhteşem',
    3: 'Hahaha',
    4: 'İnanılmaz',
    5: 'Üzgün',
    6: 'Kızgın',
    7: 'Düşündürücü',
    8: 'Beğenmedim',
}

class SolutionSpider(scrapy.Spider):
    name = 'solutionscraper'
    allowed_domains = [
        'www.technopat.net'
    ]
    start_urls = [
        'https://www.technopat.net/sosyal/uye/bora-dere.126747/solutions?page=36'
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
        solution = response.css('article.message.message--simple') # solution messages are on a different page
        raw_message = solution.css('div.bbWrapper').get()
        processed_message = Helper.process_message(raw_message)
        datetime = solution.css('time.u-dt::attr(datetime)').get()
        datetime_str = solution.css('time.u-dt::attr(title)').get()

        initialize_reactions(reactions) # get around of cumulative calculation
        solution_link = prefix + str(solution.css('a.u-concealed::attr(href)').get())

        yield scrapy.Request(
            solution_link,
            callback=self.parse_solution_page,
            meta={
                'link': link,
                'title': title,
                'processed_message': processed_message,
                'datetime': datetime,
                'datetime_str': datetime_str,
            }
        )


    def parse_solution_page(self, response):
        if response.css('a.reactionsBar-link::attr(href)').get():
                suffix = '?reaction_id=0&list_only=1&page=1'
                reaction_link = prefix + str(response.css('a.reactionsBar-link::attr(href)').get()) + suffix
                yield scrapy.Request(
                    reaction_link,
                    callback=self.parse_reactions,
                    meta=response.meta
                )
        else:
            yield {
                # 'link': response.meta['link'],
                # 'title': response.meta['title'],
                # 'processed_message': response.meta['processed_message'],
                # 'datetime': response.meta['datetime'],
                # 'datetime_str': response.meta['datetime_str'],
                # 'reactions': reactions,
                'reponse': 'parse_solution_page--else'
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
            reactions[r_map[int(reaction_id)]][0] += 1

        yield {
            # 'link': link,
            # 'title': title,
            # 'processed_message': processed_message,
            # 'datetime': datetime,
            # 'datetime_str': datetime_str,
            # 'reactions': reactions
            'response': response
        }

        # response = https://www.technopat.net/sosyal/mesaj/7516271/reactions?reaction_id=0&list_only=1&page=1
        # while next_page:
            # callback parse_reacions(next_page)

        # current_page = int(response.url.split('=')[-1])
        # next_page = response.url.split('?')[0] + 'reaction_id=0&list_only=1&page=' + str(current_page + 1)

        # yield scrapy.Request(next_page, callback=self.parse_reactions)
        