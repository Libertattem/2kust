import random

global city
global towns_start
global towns_world_start
global cities
global last_verb



cities = list()
list_city = open("words/towns_world.txt", "r", encoding="UTF-8").readlines()
city = list_city[random.randint(0, len(list_city) - 1)]
city = city.strip("\n")
cities.append(city.strip().lower())
print(city)

while city[-1] == "ь" or city[-1] == "ы" or city[-1] == "й" or city[-1] == " ":
    city = city[:-1]
    print(city)

last_verb = city[-1]
print(last_verb)

towns_start = True