from bs4 import BeautifulSoup, NavigableString

def html_to_bbcode(html):
    soup = BeautifulSoup(html, 'html.parser')

    media_sites = ['youtube.com', 'reddit.com', 'spotify.com']  # Add more media sites if needed

    # Convert <code class="bbCodeInline"> tags to [ICODE] tags
    for code in soup.find_all('code', class_='bbCodeInline'):
        code.replace_with(f'[ICODE]{code.string}[/ICODE]')

    # Convert <code class="bbCodeBlock"> tags to [CODE] tags
    for code in soup.find_all('code', class_='bbCodeBlock'):
        code.replace_with(f'[CODE]{code.string}[/CODE]')

    # Convert <a> tags to [url] tags
    for a in soup.find_all('a'):
        if 'href' in a.attrs:  # Check if 'href' attribute exists
            if any(media_site in a['href'] for media_site in media_sites):
                media_site_id = a.find_parent(attrs={'data-media-site-id': True})
                if media_site_id:
                    a.replace_with(f'[MEDIA={media_site_id["data-media-site-id"]}]' + media_site_id["data-id"] + '[/MEDIA]')
                else:
                    a.replace_with(f'[MEDIA]{a["href"]}[/MEDIA]')
            else:
                a.replace_with(f'[URL unfurl="true"]' + str(a["href"]) + '[/URL]')

    # Convert <br> tags to newline characters
    for br in soup.find_all('br'):
        br.replace_with('')

    # Convert <img> tags to [IMG] tags
    for img in soup.find_all('img'):
        img.replace_with(f'[IMG]{img["src"]}[/IMG]')

    # Convert <blockquote> tags to [QUOTE] tags
    for blockquote in soup.find_all('blockquote'):
        # Remove the 'Genişletmek için tıkla...' div
        expand_link = blockquote.find('div', class_='bbCodeBlock-expandLink')
        if expand_link:
            expand_link.decompose()
        blockquote.replace_with(f'[QUOTE]{blockquote.get_text(strip=True)}[/QUOTE]\n')

    cookie_message = soup.find('div', class_='block-rowMessage')
    if cookie_message:
        cookie_message.decompose()

    # Get the text inside the <div> tag
    div_text = ''.join([item.get_text().strip() if not isinstance(item, NavigableString) else item.string for item in soup.div.contents])

    return div_text

html = "<div class=\"bbWrapper\">BIOS güncelleyin:<br>\n<div class=\"bbCodeBlock bbCodeBlock--unfurl is-pending is-recrawl  js-unfurl fauxBlockLink\" data-unfurl=\"true\" data-result-id=\"5094885\" data-url=\"https://www.asus.com/tr/motherboards-components/motherboards/prime/prime-a520m-k/helpdesk_bios?model2Name=PRIME-A520M-K\" data-host=\"www.asus.com\" data-pending=\"true\">\n<div class=\"contentRow\">\n<div class=\"contentRow-figure contentRow-figure--fixedSmall js-unfurl-figure\">\n<span class=\"fa-2x u-muted\">\n<i class=\"fa--xf far fa-spinner fa-pulse\" aria-hidden=\"true\"></i>\n</span>\n</div>\n<div class=\"contentRow-main\">\n<h3 class=\"contentRow-header js-unfurl-title\">\n<a href=\"https://www.asus.com/tr/motherboards-components/motherboards/prime/prime-a520m-k/helpdesk_bios?model2Name=PRIME-A520M-K\" class=\"link link--external fauxBlockLink-blockLink\" target=\"_blank\" rel=\"nofollow ugc noopener\" data-proxy-href>\nPRIME A520M-K｜Anakart｜ASUS Türkiye\n</a>\n</h3>\n<div class=\"contentRow-snippet js-unfurl-desc\">ASUS Prime serisi, AMD ve Intel iÅlemcilerin tÃ¼m potansiyelini ortaya Ã§Ä±karmak iÃ§in Ã¶zenle geliÅtirildi. SaÄlam gÃ¼Ã§ tasarÄ±mÄ±na, kapsamlÄ± soÄutma Ã§Ã¶zÃ¼mlerine ve akÄ±llÄ± ayar seÃ§eneklerine sahip olan Prime serisi anakartlar, kendi PCâlerini toplayan kiÅilere kullanÄ±ÅlÄ±...</div>\n<div class=\"contentRow-minor contentRow-minor--hideLinks\">\n<span class=\"js-unfurl-favicon\">\n<img src=\"https://www.asus.com/new_asus_ico_256x256.png\" alt=\"www.asus.com\" class=\"bbCodeBlockUnfurl-icon\" data-onerror=\"hide-parent\">\n</span>\nwww.asus.com\n</div>\n</div>\n</div>\n</div>\n<br>\nBir de aynı sayfadan Ethernet sürücüsünü güncelleyin. XMP niye açmıyorsunuz?</div>"
bbcode = html_to_bbcode(html)
print(bbcode)