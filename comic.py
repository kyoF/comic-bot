import requests
from bs4 import BeautifulSoup
import json
import datetime
import slackweb


def main():
    today = get_today()

    target_url = get_url_from_json(
        'target_scraped_url').format(today.year, today.month)

    all_comics = get_comic_info_from_html(target_url).find_all('tr')

    for release_date, today_comic in enumerate(all_comics):
        if release_date == 0:
            continue

        if release_date == today.day:
            comics = get_today_release_comics(today_comic)

            break

    slack_text = create_slack_text(comics)

    slack_notify(slack_text)


def get_today():
    return datetime.date.today()


def get_url_from_json(key):
    with open('url_info.json') as f:
        json_data = json.load(f)
        return json_data[key]


def get_comic_info_from_html(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.find('div', id='content-inner')


def get_today_release_comics(comics):
    today_comics_list = []
    comics_of_day = comics.find(
        'td', class_='products-td').find_all('div', class_='div-wrap')

    for comic in comics_of_day:
        comic_info_dict = {
            'title': '',
            'image_url': '',
            'amazon_url': '',
            'company': '',
            'author': ''
        }

        comic_info_dict['title'] = get_title(comic).strip()
        comic_info_dict['image_url'] = get_image_url(comic).strip()
        comic_info_dict['amazon_url'] = get_amazon_url(comic).strip()
        comic_info_dict['company'] = get_company(comic).strip()
        comic_info_dict['author'] = get_author(comic).strip()

        today_comics_list.append(comic_info_dict)

    return today_comics_list


def get_title(comic):
    return comic.find('div', class_='product-description-right').find('a').get_text()


def get_image_url(comic):
    return comic.find('img')['src']


def get_amazon_url(comic):
    return comic.find('div', class_='product-description-right').find('a')['href']


def get_company(comic):
    try:
        return comic.find_all('p', class_='p-company')[0].get_text()
    except:
        return '不明'


def get_author(comic):
    try:
        return comic.find_all('p', class_='p-company')[1].get_text()
    except:
        return '不明'


def create_slack_text(comics):
    slack_text_list = []

    if comics == []:
        today = get_today()
        url = get_url_from_json('target_scraped_url').format(
            today.year, today.month)

        slack_text_list.append(
            {
                'blocks': [
                    {
                        'type': 'section',
                        'text': {
                            'type': 'mrkdwn',
                            'text': f'本日発売の新刊はありません \n 他の漫画情報は<{url}|こちら>を確認して下さい'
                        }
                    }
                ]
            }
        )

        return slack_text_list

    else:
        for comic in comics:
            slack_text_list.append(
                {
                    'blocks': [
                        {
                            'type': 'divider'
                        },
                        {
                            'type': 'section',
                            'text': {
                                'type': 'mrkdwn',
                                'text': f'<{comic["amazon_url"]}|{comic["title"]}> \n \n {comic["company"]}/{comic["author"]}'
                            },
                            'accessory': {
                                'type': 'image',
                                'image_url': comic['image_url'],
                                'alt_text': comic['title']
                            }
                        }
                    ]
                }
            )

        return slack_text_list


def slack_notify(slack_text):
    today = get_today()

    slack_url = slackweb.Slack(get_url_from_json('incoming_webhook_url'))
    slack_url.notify(
        text=f'今日 ( {str(today.month)}/{str(today.day)} {str(today.strftime("%a"))} ) のマンガ情報',
        attachments=slack_text
    )


if __name__ == '__main__':
    main()
