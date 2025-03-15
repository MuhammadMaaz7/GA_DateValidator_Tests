import re
import random
import calendar

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

def initialize_population(categories,totalTC, TCPerCat):
    population = []
    catTCCount = 0
    
    for category in categories:
        count = 0
        while count < TCPerCat:
            population.append(generate_test_case(category))
            count += 1
            catTCCount += 1
    
    totalTC -= catTCCount 
    while totalTC >0:
        population.append(generate_random())
        totalTC -= 1
    
    return population  

def generate_test_case(category):
    if category == "Leap Year":
        return generateLeapYear()
    elif category == "30-day month":
        return generate30DayMonth()
    elif category == "31-day month":
        return generate31DayMonth()
    elif category == "Day > 31":
        return generateDayGreater31()
    elif category == "Month > 12":
        return generateMonthGreater12()
    elif category == "Non-leap February 29":
        return generateNonLeapFebruary29()
    elif category == "Min/Max Year":
        return generateMinMaxYear()
    elif category == "day/month transitions":
        return generateDayMonthTransitions()
    
def generate_random():
    day = str(random.randint(1,31)).zfill(2)
    month = str(random.randint(1,12)).zfill(2)
    year = str(random.randint(0,9999)).zfill(4)
    
    return f"{day}/{month}/{year}"  

def generateLeapYear():
    day = str(random.randint(1,29)).zfill(2)
    month = str(random.randint(1,12)).zfill(2)
    year = random.randint(0,9999)
    
    while 1:
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) :
            break
        else:
            year = random.randint(0,9999)
    
    year = str(year).zfill(4)
    
    return f"{day}/{month}/{year}"
        
def generate30DayMonth():
    day = str(random.randint(1,30)).zfill(2)
    year = str(random.randint(0,9999)).zfill(4)
    month = str(random.choice([11,9,6,4])).zfill(2)
    
    return f"{day}/{month}/{year}"
     
def generate31DayMonth():
    day = str(random.randint(1,31)).zfill(2)
    year = str(random.randint(0,9999)).zfill(4)
    month = str(random.choice([12,10,8,7,5,3,1])).zfill(2)
    
    return f"{day}/{month}/{year}"

def generateDayGreater31():
    day = str(random.randint(31,99)).zfill(2)
    year = str(random.randint(0,9999)).zfill(4)
    month = str(random.randint(1,12)).zfill(2)
    
    return f"{day}/{month}/{year}"
    
def generateMonthGreater12():
    day = str(random.randint(1,31)).zfill(2)
    year = str(random.randint(0,9999)).zfill(4)
    month = str(random.randint(13,99)).zfill(2)
    
    return f"{day}/{month}/{year}"

def generateNonLeapFebruary29():
    day = "29"
    month = "02"
    year = random.randint(0,9999)
    
    while 1:
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) :
            year = random.randint(0,9999)
        else:
            break
    
    year = str(year).zfill(4)
    
    return f"{day}/{month}/{year}"

def generateMinMaxYear():
    day = str(random.randint(1,28)).zfill(2)
    year = str(random.choice([0000,9999])).zfill(4)
    month = str(random.randint(1,12)).zfill(2)
    
    return f"{day}/{month}/{year}"

def generateDayMonthTransitions():
    year = random.randint(0,9999)
    month = random.randint(1,12)
    day = calendar.monthrange(year,month)[1]
    day = str(day).zfill(2)
    month = str(month).zfill(2)
    year = str(year).zfill(4)
    
    return f"{day}/{month}/{year}"
            
def main():
    categories = ["Leap Year","30-day month","31-day month", "Day > 31", "Month > 12", "Non-leap February 29", "Min/Max Year", "day/month transitions"]
    selectedCategories = []
    totalTestCases = 0
    
    print("Please Select the Target Categories (1/0)") 
    for  category in categories:
        choice = input(f"{category}: ")
        
        if choice == "1":
            selectedCategories.append(category)
        else:
            continue
    
    testCasesPerCategory = 1
    totalTestCases = 25
    
    initialize_population(selectedCategories,totalTestCases,testCasesPerCategory)
    
main()