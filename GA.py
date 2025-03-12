import re
import random

def is_valid_date(date_str):
    
    if not re.match(r"\d{2}/\d{2}/\d{4}$",date_str):
        return False
    
    day_str, month_str, year_str = date_str.split("/")
    try:
        day = int(day_str)
        month = int(month_str)
        year = int(year_str)
    except ValueError:
        return False
    
    if year < 0 or year > 9999:
        return False
    
    if month < 1 or month > 12:
        return False
    
    if day < 1:
        return False
    
    if month in [4,6,9,11] and day > 30:
        return False
    elif month == 2:
        is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        max_day = 29 if is_leap else 28
        if day > max_day:
            return False
    elif day > 31:
        return False
    
    return True

def initialize_population(pop_size):
    population = []
    count = 0
    
    while count < pop_size:
        rand_day = str(random.randint(1,31)).zfill(2)
        rand_month = str(random.randint(1,12)).zfill(2)
        rand_year = str(random.randint(0000,9999)).zfill(4)
        
        date = rand_day + '/' + rand_month + '/' + rand_year 
        print(date)
        
        if is_valid_date(date):
            print("Valid date: ",date)
            date_tuple = (rand_day,rand_month,rand_year)
            population.append(date_tuple) 
            count += 1
        else:
            print("Invalid date: ",date)
            continue
        
    print(population)
        

initialize_population(100)