import requests
import argparse
from bs4 import BeautifulSoup

def createParser():
  parser = argparse.ArgumentParser()
  parser.add_argument("--type", help="Choose search type (teacher/group)")
  return parser
  

def group_search():
  group_num = input("Введите номер группы: ")
  res = requests.get("https://ruz.spbstu.ru/search/groups?q="+group_num)

  soup = BeautifulSoup(res.text, 'html.parser')
  divs = soup.find_all('a', class_='groups-list__link')

  i = 1
  for div in divs:
    print(f"{i}. {div.text}")
    i += 1
  
  num = int(input("Выберите номер группы: "))

  res = requests.get("https://ruz.spbstu.ru" + divs[num - 1].get("href"))
  parse(res.text)


def parse(html):
  soup = BeautifulSoup(html, 'html.parser')

  lesson_teacher = soup.find_all('li', class_='breadcrumb-item')
  dates = soup.find_all('div', class_='schedule__date')
  lesson_names = soup.find_all('div', class_='lesson__subject')
  lesson_types = soup.find_all('div', class_='lesson__type')
  lesson_groups = soup.find_all('div', class_='lesson-groups__list')
  lesson_places = soup.find_all('a', class_='lesson__link', href=True) 
   
  for i in range(len(dates)):
    print(dates[i].text)
    print(lesson_names[i].text)
    print(lesson_types[i].text)
    string = lesson_groups[i].text
    splitted_string = [string[i:i+13] for i in range(8, len(string), 13)]
    result = ' '.join(splitted_string)
    print(result)
    print(lesson_teacher[1].text)
    last_lesson_place = lesson_places[-1].text
    print(last_lesson_place)

    print('')
  
  choice = int(input("Действие: 0 – предыдущая неделя, 1 – следующая неделя: "))
  if choice == 1:
    link = soup.find_all('a', class_='switcher__link')
    last_element = link[-1]
    res = requests.get("https://ruz.spbstu.ru" + last_element.get("href"))
    parse(res.text)
  elif choice == 0:
    link = soup.find_all('a', class_='switcher__link')
    last_element = link[0]
    res = requests.get("https://ruz.spbstu.ru" + last_element.get("href"))
    parse(res.text)


def teacher_search():
  teacher_name = input("Введите ФИО преподавателя: ")
  res = requests.get("https://ruz.spbstu.ru/search/teacher?q="+teacher_name);
  
  soup = BeautifulSoup(res.text, 'html.parser')
  divs = soup.find_all('a', class_='search-result__link')

  i = 1
  for div in divs:
    print(f"{i}. {div.text}")
    i += 1

  num = int(input("Выберите номер преподавателя: "))

  res = requests.get("https://ruz.spbstu.ru" + divs[num - 1].get("href"))


if __name__ == '__main__':
  print(""" 
          _              _       _                                       
 ___  ___| |__   ___  __| |_   _| | ___   _ __   __ _ _ __ ___  ___ _ __ 
/ __|/ __| '_ \ / _ \/ _` | | | | |/ _ \ | '_ \ / _` | '__/ __|/ _ \ '__|
\__ \ (__| | | |  __/ (_| | |_| | |  __/ | |_) | (_| | |  \__ \  __/ |   
|___/\___|_| |_|\___|\__,_|\__,_|_|\___| | .__/ \__,_|_|  |___/\___|_|   
                                         |_|                             
""")
  parser = createParser()
  namespace = parser.parse_args()

  if namespace.type == "group":
    group_search()

  elif namespace.type == "teacher":
    teacher_search()
  else:
    print("error")