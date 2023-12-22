import requests
from bs4 import BeautifulSoup


def get_html(url: str) -> str:

    header = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (compatible; MSIE 10.0; Windows; Windows NT 6.1; WOW64; en-US Trident/6.0)"
    }

    req = requests.get(url, headers=header)
    return req.text


def get_all_hrefs(task: str) -> list:
    all_hrefs_and_title = []

    soup = BeautifulSoup(task, 'lxml')

    sections = soup.find('div', class_="task-list").find_all('section', class_="active section-task")

    count_error = 0

    for section_task in sections:
        for task in section_task.find_all("a"):
            try:
                if len(sections) == 1:
                    all_hrefs_and_title.append({
                        'title': f'Номер задания {task.get("title")}',
                        'href': f'https://gdz.ru/{task.get("href")}'
                    })
                else:
                    all_hrefs_and_title.append({
                        'title': f'{section_task.find("h2", class_="heading").text.strip()} {task.get("title")}',
                        'href': f'https://gdz.ru/{task.get("href")}'
                    })
            except AttributeError:
                print("###################################")
                count_error += 1

    print(count_error)
    return all_hrefs_and_title


def start_parse() -> None:

    print("Привет, данный скрипт поможет тебе спарсить ВСЁ ГДЗ!))!))))!)00!))")
    start_link = input("Пожалуйста, отправь мне ссылку на сайт, в котором изображены номера заданий из твоего учебнка!\n")
    task = get_html(start_link)

    all_hrefs = get_all_hrefs(task)
    for i in all_hrefs:
        print(i)


if __name__ == '__main__':
    start_parse()
