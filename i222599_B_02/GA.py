import re
import random
import calendar
import math
import csv
import matplotlib.pyplot as plt

# Provided date validation function
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

# function for initializing population
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
        
    popWithCat = numberOfCategoriesCovered(population)
    
    return popWithCat  

# Function fot generating test case based on the selected category
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

# Function for generating completely random test case
def generate_random():
    day = str(random.randint(1,31)).zfill(2)
    month = str(random.randint(1,12)).zfill(2)
    year = str(random.randint(0,9999)).zfill(4)
    
    return f"{day}/{month}/{year}"  

# Generating a leap year test case
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

# Generating a 30 day month test case
def generate30DayMonth():
    day = str(random.randint(1,30)).zfill(2)
    year = str(random.randint(0,9999)).zfill(4)
    month = str(random.choice([11,9,6,4])).zfill(2)
    
    return f"{day}/{month}/{year}"

# Generating a 31 day month test case
def generate31DayMonth():
    day = str(random.randint(1,31)).zfill(2)
    year = str(random.randint(0,9999)).zfill(4)
    month = str(random.choice([12,10,8,7,5,3,1])).zfill(2)
    
    return f"{day}/{month}/{year}"

# Generating a day greater than 31 test case
def generateDayGreater31():
    day = str(random.randint(31,40)).zfill(2)
    year = str(random.randint(0,9999)).zfill(4)
    month = str(random.randint(1,12)).zfill(2)
    
    return f"{day}/{month}/{year}"

# Generating a month greater than 12 test case
def generateMonthGreater12():
    day = str(random.randint(1,31)).zfill(2)
    year = str(random.randint(0,9999)).zfill(4)
    month = str(random.randint(13,16)).zfill(2)
    
    return f"{day}/{month}/{year}"

# Generating a invalid non leap year but feb 29 test case
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

# Generating a day containing min or max year i.e 0000 or 9999
def generateMinMaxYear():
    day = str(random.randint(1,28)).zfill(2)
    year = str(random.choice([0000,9999])).zfill(4)
    month = str(random.randint(1,12)).zfill(2)
    
    return f"{day}/{month}/{year}"

# Generating a test case which is day or month transition
def generateDayMonthTransitions():
    year = random.randint(0,9999)
    month = random.randint(1,12)
    day = calendar.monthrange(year,month)[1]
    day = str(day).zfill(2)
    month = str(month).zfill(2)
    year = str(year).zfill(4)
    
    return f"{day}/{month}/{year}"

# Function for finding categories covered by population
def numberOfCategoriesCovered(population):
    dates = []
    
    for date in population:
        cats = findCoveredCategories(date)
        dates.append((date,cats))
        
    return dates
    # return [(date, findCoveredCategories(date)) for date in population]

# Function for finding categories covered by a single date
def findCoveredCategories(date):
    categoriesCovered = []
    
    day,month,year = map(int,date.split('/'))
    
    if month <= 12:
        lastDayOfMonth = calendar.monthrange(year,month)[1]
    else:
        lastDayOfMonth = 30
    
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        categoriesCovered.append("Leap Year")
    
    if month in [4,6,9,11] and day <= 30:
        categoriesCovered.append("30-day month")
    
    if month in [12,10,8,7,5,3,1] and day <= 31:
        categoriesCovered.append("31-day month")
    
    if day > 31:
        categoriesCovered.append("Day > 31")
    
    if month > 12:
        categoriesCovered.append("Month > 12")
    
    if month == 2 and day == 29 and not isLeapYear(year):
        categoriesCovered.append("Non-leap February 29")
    
    if year == 9999 or year == 0:
        categoriesCovered.append("Min/Max Year")
    
    if day == 1 or day == lastDayOfMonth:
        categoriesCovered.append("day/month transitions")
        
    return categoriesCovered
       
# Function to check a leap year or not
def isLeapYear(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

# Fitness function for finding fitness of every test case in population
def fitness_function(dates):
    countCategories = {}
    fitnessScores = []
    
    for date, categories in dates:
        for category in categories:
            if category in countCategories:
                countCategories[category] += 1
            else:
                countCategories[category] = 1
            
    for date, categories in dates:
        unique = set(categories)
        redundant = 0
        for cat in unique:
            redundant += countCategories[category]
        redundant -= len(unique)
        
        # redundant = sum(countCategories[category] for category in unique) - len(unique)
        fit = len(unique) / ( 1+ redundant)
        fitnessScores.append((date,fit))
         
    return fitnessScores

# Population selection by the criteria of rank based selection
def populationSelection(dates, selectionRatio):
    fitnessScores = fitness_function(dates)
    datesSorted = sorted(fitnessScores, key=lambda x: x[1], reverse=True)
    selectionCount = math.ceil(selectionRatio * len(datesSorted))
    selectedDates = datesSorted[:selectionCount]
    nextGenList = [date for date,_ in selectedDates]

    remainingCount = len(dates) - len(nextGenList) 

    repeatedDates = selectedDates * (remainingCount // len(selectedDates)) + selectedDates[:remainingCount % len(selectedDates)]
    random.shuffle(repeatedDates) 
    
    for date,_ in repeatedDates:
        if len(nextGenList) < len(dates):  
            nextGenList.append(date)
    
    nextGenWithCat = numberOfCategoriesCovered(nextGenList)
    
    return nextGenWithCat

# Function for crossover mutation of a generation for new generation
def crossoverMutation(populationWithCategories):
    dates = [date for date,_ in populationWithCategories]
    crossoverMutationPopulation = []
    
    random.shuffle(dates)
    flag = False
    if len(dates) % 2 != 0:
        dates.append(random.choice(dates))
        flag = True
    
    for i in range(0, len(dates),2):
        par1 = dates[i]
        par2 = dates[i+1]
        d1,m1,y1 = map(int, par1.split('/'))
        d2,m2,y2 = map(int, par2.split('/'))
        
        d1 = str(d1).zfill(2)
        m1 = str(m1).zfill(2)
        y1 = str(y1).zfill(4)
        d2 = str(d2).zfill(2)
        m2 = str(m2).zfill(2)
        y2 = str(y2).zfill(4)
        chld1 = f"{d1}/{m2}/{y2}"
        chld2 = f"{d2}/{m1}/{y1}"
        
        chld1 = mutation(chld1) if random.random() < 0.15 else chld1
        chld2 = mutation(chld1) if random.random() < 0.15 else chld2 
        
        crossoverMutationPopulation.extend([chld1,chld2])
        
    newPopWithCat = numberOfCategoriesCovered(crossoverMutationPopulation)
    
    if flag:
        return newPopWithCat[:len(dates)-1]
    else:
        return newPopWithCat

# mutation function
def mutation(date):
    d,m,y = map(int,date.split('/'))
    d = max(1,min(31,d+random.choice([-3,0,3])))
    d = max(1,min(12,m+random.choice([-1,0,1])))
    y = max(0,y + random.choice([-100,0,100]))
    
    d = str(d).zfill(2)
    m = str(m).zfill(2)
    y = str(y).zfill(4)
    
    return f"{d}/{m}/{y}"

# Function to find the coverage by a generation against the selected categories by user
def findAccuracy(populationWithCat,selectedCategories):
    categoriesCovered = set()
    count = 0
    
    for date, categories  in populationWithCat:
        categoriesCovered.update(categories)
    
    for cat in categoriesCovered:
        if cat in selectedCategories:
            count += 1        
    
    acc = (count / len(selectedCategories)) * 100
    return acc,categoriesCovered
    
# Function for displaying final Test cases
def displayCategory(testcasesWithCat,requiredCat):
    for date,categories in testcasesWithCat:
        for category in categories:
            if category in requiredCat:
                print(date,f" ({category})")
                
# Function for adding final test cased to a csv file
def addToCsv(testcasesWithCat):
    with open('test.csv', mode='w', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Test Case", "Categories"])

        for date, categories in testcasesWithCat:
            writer.writerow([date,", ".join(categories)])

# Function for generating a line graph for coverage visualization over generations
def makeLineGraph(coverage):
    plt.figure(figsize=(14,7))
    gen = list(range(len(coverage)))
    plt.plot(gen,coverage,marker='o',linestyle='-',color='g',label='GA Coverage (%)')
    
    plt.xlabel("Generation")
    plt.ylabel("COverage(%)")
    plt.title("Line Graph Visualization for GA Coverage over Generations")
    plt.grid(True,linestyle='--',alpha=0.9)
    plt.legend()
    
    plt.show()
  
def GA():
    valid = ["Leap Year","30-day month","31-day month"]
    Invalid = ["Day > 31", "Month > 12", "Non-leap February 29"]
    Boundaries = ["Min/Max Year", "day/month transitions"]
    categories = ["Leap Year","30-day month","31-day month", "Day > 31", "Month > 12", "Non-leap February 29", "Min/Max Year", "day/month transitions"]
    # selectedCategories = ["Leap Year","30-day month","31-day month", "Day > 31", "Month > 12", "Non-leap February 29", "Min/Max Year", "day/month transitions"]
    selectedCategories = []
    testCasesPerCategory = 5
    totalTestCases = 0
    iterations = 0
    accuracy = 0
    coveragePerGen = []
    
    print("Please Select the Target Categories (1/0)") 
    for  category in categories:
        choice = input(f"{category}: ")
        
        if choice == "1":
            selectedCategories.append(category)
        else:
            continue
    
    totalTestCases = input("Enter the number of Total Test Cases Needed: ")
    while int(totalTestCases) < len(selectedCategories):
        totalTestCases = input("Total Test Cases must be greater than selected target categories: ")
    
    totalTestCases = int(totalTestCases)
    
    population = initialize_population(selectedCategories,totalTestCases,testCasesPerCategory)
        
    while True:
        if accuracy >= 90 or iterations == 100:
            break
        nextGeneration = populationSelection(population,selectionRatio=0.7)
        afterCrossover = crossoverMutation(nextGeneration)
        accuracy,categoriesCovered = findAccuracy(afterCrossover,selectedCategories)
        iterations += 1
        coveragePerGen.append(accuracy)
    
    print("_________Best Test Cases_________")
    print()
    print("_________Valid_________")
    displayCategory(afterCrossover,valid)
    print("_________Invalid_________")
    displayCategory(afterCrossover,Invalid)
    print("_________Boundary_________")
    displayCategory(afterCrossover,Boundaries)
    print()
    print(f"Coverage Acheived: {accuracy}%")
    print(f"Generations Executed: {iterations}")
    addToCsv(afterCrossover)
    makeLineGraph(coveragePerGen)

GA()