import requests
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
                    if len(sections) == 1:
                        all_hrefs.append({
                            'title': f'Номер задания {task.get("title")}',
                            'href': f'https://gdz.ru/{task.get("href")}'
                        })
                    else:
                        all_hrefs.append({
                            'title': f'{section_task.find("h2", class_="heading").text.strip()} {task.get("title")}',
                            'href': f'https://gdz.ru/{task.get("href")}'
                        })
                except AttributeError:
                    count_error += 1

        print(count_error)
        return all_hrefs

    def show_all_hrefs(self):
        self.get_all_hrefs()
        for i in self.all_hrefs_and_title:
            print(i)


def start_parse() -> None:

    print("Привет, данный скрипт поможет тебе спарсить ВСЁ ГДЗ!))!))))!)00!))")
    start_link = input("Пожалуйста, отправь мне ссылку на сайт, в котором изображены номера заданий"
                       " из твоего учебнка!\n")

    Href(start_link).show_all_hrefs()


if __name__ == '__main__':
    start_parse()
