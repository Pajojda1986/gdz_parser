import requests
from time import sleep
from os import mkdir, chdir
from bs4 import BeautifulSoup


class Url:
    
    tasks = None

    def __init__(self, url):
        self.url = url
        self.header = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (compatible; MSIE 10.0; Windows; Windows NT 6.1; WOW64; en-US Trident/6.0)"
        }

        self.tasks = requests.get(self.url, headers=self.header).text


class Href(Url):

    def __int__(self):
        self.all_hrefs_and_title = []
        self.count_error = 0

    def get_all_hrefs(self) -> list:
        count_error = 0
        soup = BeautifulSoup(self.tasks, 'lxml')
        sections = soup.find('div', class_="task-list").find_all('section', class_="active section-task")

        all_hrefs = []

        for section_task in sections:
            for task in section_task.find_all("a"):
                try:
                    all_hrefs.append({
                        'title': f'{section_task.find("h2", class_="heading").text.strip()}',
                        'number': f' {task.get("title")}',
                        'href': f'https://gdz.ru{task.get("href")}'
                    })
                except AttributeError:
                    count_error += 1

        print(count_error)
        self.all_hrefs_and_title = all_hrefs
        return all_hrefs

    def show_all_hrefs(self):
        self.get_all_hrefs()
        for i in self.all_hrefs_and_title:
            print(i)


class ImageOnHref(Href):
    def get_jpg(self, directory):

        print("Image scraping start!")

        all_hrefs = self.get_all_hrefs()
        for img in all_hrefs:

            number = requests.get(img['href'], headers=self.header).text
            sleep(0.5)
            soup = BeautifulSoup(number, 'lxml')

            img_href = 'https:' + soup.find('div', class_="with-overtask").find('img').get('src')

            dir = directory + '/' + BeautifulSoup(self.tasks, 'lxml').find('title').next_element.text

            try:
                mkdir(dir)
                chdir(dir)

            except FileExistsError:
                chdir(dir)

            chdir(dir)
            p = requests.get(img_href)
            out = open(f"{img['number']}.jpg", "wb")
            out.write(p.content)
            out.close()
            chdir(directory)
            print(f"Successfully {img['number']}")


def start_parse() -> None:

    print("Привет, данный скрипт поможет тебе спарсить все картинки с гдз с сайта https://gdz.ru/")
    start_link = input("Пожалуйста, отправь мне ссылку на страницу, на который изображены все"
                       " номера заданий из выбранного учебника!\n")

    current_dir = input("Выберете директорию (папку) для фото!\n")

    ImageOnHref(start_link).get_jpg(current_dir)


if __name__ == '__main__':
    start_parse()
