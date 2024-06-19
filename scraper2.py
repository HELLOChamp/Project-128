from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
import csv

# NASA Exoplanet URL
START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"

# Webdriver
browser = webdriver.Chrome("chromedriver.exe")
browser.get(START_URL)

time.sleep(10)

brown_dwarfs_data = []

headers = ['Star_name', 'Distance', 'Mass', 'Radius']

def scrape():
    for i in range(1,5):
        while True:
            time.sleep(2)

            soup = BeautifulSoup(browser.page_source, "html.parser")

            

            for ul_tag in soup.find_all("ul", attrs={"class", "marker"}):
                li_tags = ul_tag.find_all("li")
                temp_list = []
                for index, li_tag in enumerate(li_tags):
                    if index == 0:
                        temp_list.append(li_tag.find_all("a")[0].contents[0])
                    else:
                        try:
                            temp_list.append(li_tag.contents[0])
                        except:
                            temp_list.append("")

                # Get Hyperlink Tag
                hyperlink_li_tag = li_tags[0]

                temp_list.append("wiki"+ hyperlink_li_tag.find_all("a", href=True)[0]["href"])
                
                brown_dwarfs_data.append(temp_list)

            print(f"Page {i} scraping completed")

    scrape()
    
# Define Header
    headers = ['Star_name', 'Distance', 'Mass', 'Radius', 'hyperlink']
    
    # Define pandas DataFrame
    brown_dwarfs_df_1 = pd.DataFrame(brown_dwarfs_data, columns=headers)
    
    #Convert to CSV 
    brown_dwarfs_df_1.to_csv('new_scraped_data.csv',index=True, index_label="id")

# Calling Method
scrape()

new_brown_dwarfs_data = []

def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
      
        soup = BeautifulSoup(page.content, "html.parser")

        temp_list = []

        for tr_tag in soup.find_all("tr", attrs={"class": "star_row"}):
            td_tags = tr_tag.find_all("td")
          
            for td_tag in td_tags:
                try: 
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")
                    
        new_brown_dwarfs_data.append(temp_list)

    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

#Calling method

for index, data in enumerate(new_brown_dwarfs_data):
    scrape_more_data(data[5])
    print(f"scraping at hyperlink {index+1} is completed.")

print(new_brown_dwarfs_data[0:10])

final_brown_dwarfs_data = []

for index, data in enumerate(brown_dwarfs_data):
    new_brown_dwarfs_data_element = new_brown_dwarfs_data[index]
    new_brown_dwarfs_data_element = [elem.replace("\n", "") for elem in new_brown_dwarfs_data_element]
    new_brown_dwarfs_data_element = new_brown_dwarfs_data_element[:7]
    final_brown_dwarfs_data.append(data + new_brown_dwarfs_data_element)

with open("final.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(final_brown_dwarfs_data)