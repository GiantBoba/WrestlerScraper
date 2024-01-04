import requests
import re
from datetime import *

def insert_slash(input_string):
    pattern = re.compile(r'(?<=[^ ])([A-Z])')
    output_string = re.sub(pattern, r'/\1', input_string)
    return output_string  

def getSource(wrestler_name):
    val = wrestler_name
    val = val.replace(" ","-")
    url = 'https://www.thesmackdownhotel.com/wrestlers/' + val    
    response = requests.get(url)
    if response.status_code == 200:
        print("Using Smackdown Hotel as datasource")
    else:
        print("No datasource found")
    return response

def getNickname(payload):
    nickname = payload.find('li', class_='field-entry nicknames')
    if nickname:
        nickname = nickname.text.strip()
        nickname = nickname.replace("Nicknames","")
        nickname = nickname.strip()
        if(";" in nickname):
            nickname = nickname.split(';')[1]
            nickname = nickname.strip()
    else:
        nickname = "None"
    return nickname

def getGender(payload):
    gender = payload.find('li', class_='field-entry gender gender')
    if gender:
        gender = gender.text.strip()
        gender = gender.replace("Gender","")
        if(gender.strip() == "Male"):
            gender = "M"
        elif(gender.strip() == "Female"):
            gender = "F"
        else:
            gender = "?"
    else:
        gender = "?"
    return gender

def getIsActive(payload):
    active = payload.find('li', class_='field-entry roles full-width subfields-inline-text roles')
    if active:
        active = active.text.strip()
        if("Wrestler" in active):
            active = active.split("Wrestler")[1]
            if("\tPresent" in active):
                active = "Yes"
            else:
                active = "No"
        elif("Manager" in active):
            active = active.split("Manager")[1]
            if("\tPresent" in active):
                active = "Yes"
            else:
                active = "No"
        elif("\tPresent" in active):
            active = "Yes"
        else:
            active = "No"
    else:
        active = "?"
    return active

def getActivePromotion(payload):
    promotion = payload.find('span', class_='field-entry promotion')
    if(promotion):
        promotion_name = promotion.text.strip()
        promotion_name = promotion_name.replace("Promotion","")
        currPromotion = promotion_name.strip()
    else:
        currPromotion = "None"
    return currPromotion

def getPromotion(payload):
    companies_section = payload.find('li', class_='field-entry companies field-entry full-width subfields subfields-inline-text')
    if(companies_section):
        promotion_rows = companies_section.find_all('tr')
        promotion_time_dict = {}
        for row in promotion_rows:
            columns = row.find_all('td')
                        
            if len(columns) == 3:
                promotion_name = columns[0].find('span', class_='field-value').text.strip()
                start_date = columns[1].find('span', class_='field-value').text.strip()
                end_date = columns[2].find('span', class_='field-value').text.strip()
                if("Present" in end_date):
                    today_date = datetime.now()
                    end_date = today_date.strftime("%B %d, %Y")
                time_spent = len(range(int(start_date[-4:]), int(end_date[-4:]) + 1))

                if promotion_name in promotion_time_dict:
                    promotion_time_dict[promotion_name] += time_spent
                else:
                    promotion_time_dict[promotion_name] = time_spent

                most_time_spent_promotion = max(promotion_time_dict, key=promotion_time_dict.get)
                if(most_time_spent_promotion == "WWF"):
                    most_time_spent_promotion = "WWE"
                currPromotion = most_time_spent_promotion
    else:
        currPromotion = "None"
    return currPromotion

def getStable(payload):
    stable = payload.find('li', class_='field-entry teams full-width subfields-inline-text')
    brand = payload.find('span', class_='field-entry brands')
    alignment = payload.find('li', class_='field-entry alignments full-width alignments')
    if stable:
        stable = stable.text.strip()
        stable = stable.replace("Tag Teams & Stables","")
        if("Present" in stable):
            stable = stable.split("Present")[0]
            stable = stable.split(" -")[0]
            stable = stable.strip()        
    else:
        if brand:
            brand = brand.text.strip()
            brand = brand.replace("Brand","")
            stable = brand.strip()
        else:
            if alignment:
                alignment = alignment.text.strip()
                alignment = alignment.replace("Face / Heel Turns","")
                alignment = alignment.replace("Alignmentfromto","")
                alignment = alignment.strip()
                alignment = alignment[0:7]
                stable = alignment.strip()
            else:
                stable = "Main"
    return stable

def getWeight(payload):
    weight = payload.find('li', class_='field-entry weights unstyled subfields-inline-text weight')
    if weight:
        weight = weight.text.strip()
        weight = weight.replace("Weight","")
        weight = weight.strip()
        lbs = weight[:3]
        lbs = int(lbs)
    else:
        lbs = 0
    return(lbs)

def getHeight(payload):
    height = payload.find('li', class_='field-entry height height')
    if(height):
        height = str(height)
        height = height[107:114]
    else:
        height = "0 ft 0"
    return height

def getSize(height):
    feet = height.split("ft")[0]
    feet = int(feet[-2:-1])
    inches = height.split("ft")[1]
    inches = inches.split(" ")
    inches = int(inches[1])
    inches = (inches + (feet*12))
    inches = int(inches)
    return inches

def getCountry(payload):
    country = payload.find('li', class_='field-entry nationality country')
    if country:
        country = country.text.strip()
        country = country.replace("Nationality","")
        country = insert_slash(country.strip())
        country = country.strip()
    else:
        country = "Unknown"
    return country

def getDOB(payload):
    dob = payload.find('li', class_='field-entry born')
    if dob:
        dob = dob.text.strip()
        dob = dob.replace("Born","")
        dob = dob.split(" (")[0]
        dob = datetime.strptime(dob.strip(), "%B %d, %Y")
        dob = dob.date()
    else:
        dob = "Unknown"
    return dob

def getFinisher(payload):
    finisher = payload.find('li', class_='field-entry finishers full-width subfields-inline-text finishers')
    if(finisher):
        finisher = finisher.text.strip()
        finisher = finisher.replace("Finishers","")
        finisher = finisher.split(" (")[0]
        finisher = finisher.strip()
        finisherName = finisher.split("\n")[0]
        if(" - " in finisher):
            finisherDesc = finisher.split("\n")[1]
        else:
            finisherDesc = finisher.split("\n")[0]
        finsiherDesc = finisherDesc.strip()
        finisherName = finisherName.strip()
        finisherName = finisherName[:-2]
    else:
        finisherName = "None"
        finisherDesc = "None"
    return finisherName, finisherDesc