from bs4 import BeautifulSoup, NavigableString

class Helper:
    @classmethod
    def process_message(cls, html):
        soup = BeautifulSoup(html, 'html.parser')

        media_sites = ['youtube.com', 
                       'reddit.com', 
                       'spotify.com', 
                       'dailymotion', 
                       'apple.com', 
                       'facebook.com', 
                       'flickr.com', 
                       'giphy.com', 
                       'imgur.com', 
                       'instagram.com', 
                       'pinterest.com', 
                       'soundcloud.com',
                       'tiktok.com',
                       'tumblr.com',
                       'twitch.tv',
                       'x.com',
                       'vimeo.com'
                       ] 

        for code in soup.find_all('code', class_='bbCodeInline'):
            code.replace_with(f'[ICODE]{code.string}[/ICODE]')

        for code in soup.find_all('code', class_='bbCodeBlock'):
            code.replace_with(f'[CODE]{code.string}[/CODE]')

        for a in soup.find_all('a'):
            if 'href' in a.attrs:  
                if any(media_site in a['href'] for media_site in media_sites):
                    media_site_id = a.find_parent(attrs={'data-media-site-id': True})

                    if media_site_id:
                        a.replace_with(f'[MEDIA={media_site_id["data-media-site-id"]}]' + media_site_id["data-id"] + '[/MEDIA]')
                    else:
                        a.replace_with(f'[MEDIA]{a["href"]}[/MEDIA]')

                else:
                    parent_div = a.find_parent('div', class_='bbCodeBlock')

                    if parent_div:
                        parent_div.replace_with(f'[URL unfurl="true"]' + str(a["href"]) + '[/URL]')

        for br in soup.find_all('br'):
            br.replace_with('')

        for img in soup.find_all('img'):
            img.replace_with(f'[IMG]{img["src"]}[/IMG]')

        for blockquote in soup.find_all('blockquote'):
            expand_link = blockquote.find('div', class_='bbCodeBlock-expandLink')

            if expand_link:
                expand_link.decompose()

            if blockquote['data-quote'] != "":
                quote_owner = blockquote['data-quote']
                post_id = blockquote['data-source'].split(': ')[1]
                member_id = blockquote['data-attributes'].split(': ')[1]
                blockquote.replace_with(f'[QUOTE="{quote_owner}, post: {post_id}, member: {member_id}"]{blockquote.get_text(strip=True).split('dedi:')[1]}[/QUOTE]\n')
            else:
                blockquote.replace_with(f'[QUOTE]{blockquote.get_text(strip=True)}[/QUOTE]\n')


        cookie_message = soup.find('div', class_='block-rowMessage')
        
        if cookie_message:
            cookie_message.decompose()

        div_text = ''.join([item.get_text().strip() if not isinstance(item, NavigableString) else item.string for item in soup.div.contents])

        return div_text