import requests
import argparse
from bs4 import BeautifulSoup

def createParser():
  parser = argparse.ArgumentParser()
  parser.add_argument("--type", help="Choose search type (teacher/group)")
  return parser
  

def group_search():
  group_num = input("Введите номер группы: ")
  res = requests.get(f"https://ruz.spbstu.ru/search/groups?q={group_num}")

  soup = BeautifulSoup(res.text, 'html.parser')
  divs = soup.find_all('a', class_='groups-list__link')

  i = 1
  for div in divs:
    print(f"{i}. {div.text}")
    i += 1
  
  num = int(input("Выберите номер группы: "))

  res = requests.get(f"https://ruz.spbstu.ru{divs[num - 1].get("href")}")
  parse(res.text)


def parse(html):
  soup = BeautifulSoup(html, 'html.parser')

  dates = soup.find_all('div', class_='schedule__date')
  lessons = soup.find_all('li', class_='lesson')
  num_day = 0
  count = 0
  for i in lessons:
    if count == 0:
      print(f"\033[0;31m{dates[num_day].text}\033[0m")
      num_day += 1

    count += 1
    lesson_name = i.find('div', class_='lesson__subject')
    print(f"{lesson_name.text}")

    lesson_type = i.find('div', class_='lesson__type')
    print(lesson_type.text)

    lesson_groups = i.find('div', class_='lesson-groups__list')
    splitted_string = [lesson_groups.text[i:i+13] for i in range(8, len(lesson_groups.text), 13)]
    result = ' '.join(splitted_string)
    print(result)

    lesson_link = i.find('div', class_='lesson__teachers')
    if lesson_link:
      span_elements = lesson_link.find_all('span')
      print(span_elements[-1].text)

    lesson_places = i.find('div', class_='lesson__places')
    print(lesson_places.text)

    if count == len(i.parent):
      count = 0
      print(" ")
    print(" ")

  
  choice = int(input("Действие: 0 – предыдущая неделя, 1 – следующая неделя"))
  link = soup.find_all('a', class_='switcher__link')
  index = ""
  if choice == 1: index = link[-1]
  elif choice == 0: index = link[0]
  res = requests.get(f"https://ruz.spbstu.ru{index.get("href")}")
  parse(res.text)
  

def teacher_search():
  teacher_name = input("Введите ФИО преподавателя: ")
  res = requests.get(f"https://ruz.spbstu.ru/search/teacher?q={teacher_name}");
  
  soup = BeautifulSoup(res.text, 'html.parser')
  divs = soup.find_all('a', class_='search-result__link')

  i = 1
  for div in divs:
    print(f"{i}. {div.text}")
    i += 1

  num = int(input("Выберите номер преподавателя: "))

  res = requests.get(f"https://ruz.spbstu.ru{divs[num - 1].get("href")}")
  parse(res.text)


if __name__ == '__main__':
  print("""
          _              _       _                                       
 ___  ___| |__   ___  __| |_   _| | ___   _ __   __ _ _ __ ___  ___ _ __ 
/ __|/ __| '_ \\ / _ \\/ _` | | | | |/ _ \\ | '_ \\ / _` | '__/ __|/ _ \\ '__|
\\__ \\ (__| | | |  __/ (_| | |_| | |  __/ | |_) | (_| | |  \\__ \\  __/ |   
|___/\\___|_| |_|\\___|\\__,_|\\__,_|_|\\___| | .__/ \\__,_|_|  |___/\\___|_|   
                                         |_|                             
""")
  print("\033[0;31mby qookieFaitPipi\n \033[0m")
  parser = createParser()
  namespace = parser.parse_args()

  if namespace.type == "group":
    group_search()

  elif namespace.type == "teacher":
    teacher_search()
  else:
    print("error")