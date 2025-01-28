import json
import difflib  # for checking similar lines
import requests

# reading DB-datas from json-file
with open("countries.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# checking if a country has wine regions and how many
country = input("Which country do you plan to travel to? ").strip()
def check_country():   
    if country in data:
        regions = data[country]
        print(f"{country} has {len(regions)} wine regions.")
        info_check = input("Do you want a summary about these regions? (yes/no) ")
        if info_check.lower() == "yes":
            region_info(country)
    # checking if user typed country name wrong
    else:
        suggestions = difflib.get_close_matches(country, data.keys(), n=3)

        if suggestions:
            print(f"There is no such country as {country}. Did you mean ", end="")
            for suggestion in suggestions:
                print(f"{suggestion}? (yes/no) ", end="")
                answer = input("")
                if answer.lower() == "yes":
                    regions = data[suggestion]
                    print(f"{suggestion} has {len(regions)} wine regions.")
                    info_check = input("Do you want a summary about these regions? (yes/no) ")
                    if info_check.lower() == "yes":
                        region_info(suggestion)
                    break
                elif answer.lower() == "no":
                    continue        # checking next suggestion if user says no
                else:
                    print("Invalid answer. Please type 'yes' or 'no'.")
            else:
                print(f"There are no wine regions in {country}.")
        else:
            print(f"There are no wine regions in {country}.")

# shows info about wine regions of a specific country
def region_info(country):
    print(f"Here are the most famous wine regions in {country}:")
    regions = data[country]
    for index, region in enumerate(regions, start=1):
        print(f"{index}. {region["name"]}. {region["features"]}.")


    

check_country()
# load_main_cities()

