import requests
from bs4 import BeautifulSoup
import json
import datetime


def main():
    # 明日の日付と曜日を取得する
    today = get_today()

    comics = []

    target_url = get_url_from_json(
        'target_scraped_url').format(today.year, today.month)

    all_comics = get_comic_info_from_html(target_url).find_all('tr')

    for release_date, today_comic in enumerate(all_comics):
        if release_date == 0:
            continue

        if release_date == today.day:
            comics_of_day = today_comic.find(
                'td', class_='products-td').find_all('div', class_='div-wrap')

            for comic in comics_of_day:
                comic_info_dict = {
                    'title': '',
                    'image_url': '',
                    'amazon_url': '',
                    'company': '',
                    'author': ''
                }

                comic_info_dict['title'] = get_title(comic)
                comic_info_dict['image_url'] = get_image_url(comic)
                comic_info_dict['amazon_url'] = get_amazon_url(comic)
                comic_info_dict['company'] = get_company(comic)
                comic_info_dict['author'] = get_author(comic)

                comics.append(comic_info_dict)

            break

    slack_text = create_slack_text(comics)


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
    return ''


def slack_notify(text, month, day, day_of_week):
    slack_url = get_url_from_json('incoming_webhook_url')
    slack_url.notify(
        f'今日 ( {str(month)}/{str(day)} {str(day_of_week)} ) のマンガ情報', attachments=text)


if __name__ == '__main__':
    main()
