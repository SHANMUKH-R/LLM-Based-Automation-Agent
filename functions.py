import re
import requests
from fuzzywuzzy import fuzz
from datetime import datetime
from openai import OpenAI

def get_task_output(AIPROXY_TOKEN, task):
    client = OpenAI(api_key = AIPROXY_TOKEN)
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
        {"role": "user", "content": task}
    ]
    )
    return response.choices[0].message.content.strip()

def count_days(dayname:str):
    days = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6}
    dayvalue = -1
    day = None
    for d in days:
        if d in dayname.lower():
            dayvalue = days[d]
            day = d
            break
    try:
        print("This will not cause any error")
        with open("/data/dates.txt","r") as file:
            print("My line")
            data = file.readlines()
            count  = sum([1 for line in data if datetime.strptime( line.strip(),"%Y-%m-%d").weekday()==dayvalue])
            f = open("/data/{}-count".format(day), "w")
            f.write(str(count))
            f.close()
    except:
        print("There is no File in data directory try making one")
def extract_dayname(task:str):
    match = re.search(r'count\s+(\w+)',task)  #re.search(r'count\s+([A-Za-z]+)', task)
    if match:
        return match.group(1)
    return ""
def extract_package(task: str):
    match = re.search(r'install\s+(\w+)',task)
    if match:
        return match.group(1)
    return ""
def get_valid_package_name(package_name:str):
    with open("packages.txt","r",encoding="utf-8") as file:
        data = file.read().strip()
        packages = [pkg.strip() for line in data.splitlines() for pkg in line.split()]
        
    best_match = max(packages, key=lambda pkg: fuzz.ratio(package_name, pkg), default="")
    
    return best_match if fuzz.ratio(package_name, best_match) >= 90 else ""
