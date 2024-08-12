import numpy as np 
import pandas as pd
from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import random
from find_info_all import *



def get_data_from_page(driver):
    td_elements = driver.find_elements(By.CSS_SELECTOR, 'td.a1')
    time.sleep(random.randint(2, 5))
    for td in td_elements:
        try:
            next_td = td.find_element(By.XPATH, 'following-sibling::td[1]')
            first_a = next_td.find_element(By.TAG_NAME, 'a')
        
            link = first_a.get_attribute('href')
            name = first_a.text
            
            all_names.append(name)
            all_links.append(link)
        except Exception as e:
            print(f"Không thể lấy dữ liệu từ thẻ <td>: {e}")
    print(len(all_names))
    print(len(all_links))



def first_info(driver, url):
    article_element = driver.find_element(By.TAG_NAME, 'article')
    profile_element = article_element.find_element(By.CLASS_NAME, 'profile.clearfix')
    sleep(random.randint(1, 3))
    full_text = profile_element.text

    texts = full_text
    lines = texts.split('\n')
    name = lines[0]
    position = lines[1]
    age_birth = re.search(r'(\d+y.o.) \(([^)]+)\)', lines[2])
    if age_birth:
        age = age_birth.group(1)  # "25y.o."
        birthdate = age_birth.group(2)  # "Feb 18, 1998"

    height_weight = re.search(r'(\d+cm) / (\d\'\d+\") (\d+kg) / (\d+lbs)', lines[2])
    if height_weight:
        height_cm = height_weight.group(1)  # "195cm"
        height_ft_in = height_weight.group(2)  # "6'5\""
        weight_kg = height_weight.group(3)  # "96kg"
        weight_lbs = height_weight.group(4)  # "212lbs"
    df_info_1 = pd.DataFrame({
        "Link": [url],
        'Full Name': [name],
        'Position': [position],
        'Age': [age],
        'Birthdate': [birthdate],
        'Height (cm)': [height_cm],
        'Height (ft/in)': [height_ft_in],
        'Weight (kg)': [weight_kg],
        'Weight (lbs)': [weight_lbs]
    })
    return df_info_1

def second_info(driver):
    article_elements = driver.find_elements(By.TAG_NAME, 'article')
    sleep(random.randint(1, 3))
    for article in article_elements:
        grid_divs = article.find_elements(By.CSS_SELECTOR, 'div.grid:not([class*=" "])')
        for grid_div in grid_divs:
            col_divs = grid_div.find_elements(By.CSS_SELECTOR, 'div.col')
            col_divs = [col.text for col in col_divs]
    over_rt, potential, value, wage = [], [], [], []
    for el in col_divs:
        els = el.split('\n')
        if els[1] == "Overall rating":
            over_rt.append(els[0])
        elif els[1] == "Potential":
            potential.append(els[0])
        elif els[1] == "Value":
            value.append(els[0])
        elif els[1] == "Wage":
            wage.append(els[0])
    col_divs_df = pd.DataFrame({
        "Overall rating": over_rt,
        "Potential": potential,
        "Value": value,
        "Wage" :wage
    })
    return col_divs_df

def third_info(driver):
    article_elements = driver.find_elements(By.TAG_NAME, 'article')
    sleep(random.randint(1, 3))
    ls = []
    for article in article_elements:
        grid_divs = article.find_elements(By.CSS_SELECTOR, 'div.grid.attribute')
        if grid_divs:
            for grid_div in grid_divs:
                col_divs = grid_div.find_elements(By.CSS_SELECTOR, 'div.col')
                if col_divs:
                    for col_div in col_divs:
                        ls.append(col_div.text)
    profile, player_specialities, national_team, club, playstyles = [], [], [], [], []
    attacking, skill, movement, power, mentality, defending, goalkeeping = [], [], [], [], [], [], []

    for item in ls:

        if item.startswith('Attacking'):
            attacking = item.split('\n')[1:]
        elif item.startswith('Skill'):
            skill = item.split('\n')[1:]
        elif item.startswith('Movement'):
            movement = item.split('\n')[1:]
        elif item.startswith('Power'):
            power = item.split('\n')[1:]
        elif item.startswith('Mentality'):
            mentality = item.split('\n')[1:]
        elif item.startswith('Defending'):
            defending = item.split('\n')[1:]
        elif item.startswith('Goalkeeping'):
            goalkeeping = item.split('\n')[1:]

            
    aside_elems = driver.find_elements(By.TAG_NAME, "aside")
    sleep(random.randint(1, 3))
    aside_info = []
    for aside in aside_elems:
        attribute_elems = aside.find_elements(By.CSS_SELECTOR, "div.attribute")
        sleep(random.randint(1, 3))
        for attribute in attribute_elems:
            aside_info.append(attribute.text)
        sleep(random.randint(1, 3))
    aside_info = aside_info[0].split("\n")

    aside_df = find_aside_info(aside_info)
    
    aside_df = find_info_attacking(attacking)
    skill_df = find_info_skill(skill)
    movement_df = find_info_movement(movement)
    power_df = find_info_power(power)
    mentality_df = find_info_mentality(mentality)
    defending_df = find_info_defending(defending)
    goalkeeping_df = find_info_goalkeeping(goalkeeping)

    combined_df = pd.concat([aside_df, aside_df, skill_df, movement_df, power_df, mentality_df, defending_df, goalkeeping_df], axis=1)
    return combined_df
def info_in_one_link(driver, link):
    url = f"{link}?attr=classic"
    driver.get(url)
    sleep(random.randint(7, 10))
    df1 = first_info(driver, link)
    df2 = second_info(driver)
    df3 = third_info(driver)
    result = pd.concat([df1, df2, df3], axis=1)

    return result

def main_all_link():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = 'https://sofifa.com/?r=240048&set=true&offset='
    offset = 0  # Bắt đầu từ offset 0
    max_offset = 12000  # Giá trị offset tối đa

    all_names = []
    all_links = []

    while offset <= max_offset:
        url = f"{base_url}{offset}"
        driver.get(url)
        time.sleep(random.randint(5, 13))
        get_data_from_page(driver)
        offset += 60
        time.sleep(random.randint(10, 20))
    driver.quit()
    df = pd.DataFrame({"Name":all_names, "Link":all_links})
    df.to_csv("All_Links_and_Names1.csv")
def main_craw_info():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    df = pd.read_csv("All_Links_and_Names.csv")
    data = pd.DataFrame()
    start = time.time()
    for i in range(120):
        print(i)
        links = df["Link"][i]
        print(links)
        res = info_in_one_link(driver, links)
        data = pd.concat([data, res], axis = 0, ignore_index=True)
    end = time.time()
    runtime = end - start
    print("Total run = " , runtime)

    df = df.merge(data, on = "Link", how = "left")
    df.to_csv("First_100.csv", index=False)
if __name__=="__main__":

    main_craw_info()

