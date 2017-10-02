from bs4 import BeautifulSoup
import requests


def open_url(url):
    url = requests.get(url)
    return url


def create_soup(url):
    soup = BeautifulSoup(url.text, "lxml")
    return soup


def find_elements(soup):
    info = soup.find('div', class_='search-results organic').find_all('div', class_='info')

    print(len(info), ' - Элементов на странице')

    for i in info:
        try:
            business_name = i.find('span', itemprop='name').text
            link = i.find('a', class_='track-visit-website')
            address = i.find('span', class_='street-address').text
            addressRegion = i.find('span', itemprop='addressRegion').text
            local_address = i.find('span', itemprop='addressLocality').text
            phone = i.find('div', itemprop='telephone').text
            categories = i.find('div', class_='categories').text
            full_address = []
            link = link.get('href')
            full_address.append(business_name)
            full_address.append(link)
            full_address.append(address)
            local_address = local_address.strip()
            full_address.append(local_address)
            full_address.append(addressRegion)
            full_address.append(phone)
            full_address.append(categories)

            with open('text.txt', 'a') as f:  # Файл для записи
                print(full_address, file=f)
        except:
            pass


def find_next_page(soup):
    try:
        next = soup.find('a', class_='next ajax-page')
        index = next['href'].split('=')[1]
        print('Паарсим страницу - {} '.format(index))
        return next['href']

    except:
        print('Не найдена кнопка NEXT')
        return False


def next_page(next):
    url = 'https://www.yellowpages.com{}'.format(next)
    url = open_url(url)
    soup = create_soup(url)
    find_elements(soup)
    next = find_next_page(soup)
    return next


def main():
    url = 'https://www.yellowpages.com/ny/auto-repair'  # Первая страница поиска
    url = open_url(url)
    soup = create_soup(url)
    find_elements(soup)
    next = find_next_page(soup)
    while next:
        next = next_page(next)


if __name__ == '__main__':
    main()
