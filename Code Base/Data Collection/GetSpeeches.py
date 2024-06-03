import csv
import requests
from bs4 import BeautifulSoup

# Datasource 
url = "https://www.ukpol.co.uk/last-100-speeches-added/"

response = requests.get(url)

#Using BeautifulSoup to fetch the speech data
soup = BeautifulSoup(response.text, 'html.parser')
speeches = soup.find_all('div', class_='tg_module_block')

speeches_data = []
test =0 
for speech in speeches:
    
    #link to the speech
    link_element = speech.find('a', href=True)
    speech_url = link_element['href']

    # fetching the speech data using the link
    speech_response = requests.get(speech_url)
    speech_soup = BeautifulSoup(speech_response.text, 'html.parser')
    
    # extract the speech text from div class cm-entry-summary
    speech_text_element = speech_soup.find('div', class_='cm-entry-summary')
    speech_text = speech_text_element.get_text(strip=True)

    # getting the politicians name and speech title from h1
    h1_element = speech_soup.find('h1')
    h1_text = h1_element.get_text()
    politician_name, speech_title = [part.strip() for part in h1_text.split('–', 1)]

    speeches_data.append([politician_name, speech_title, speech_url, speech_text])

    #For testing 
    print(test)
    test+=1
    

csv_file_path = 'Data Collection/SpeechData.csv'

# Write data into a CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Politician Name', 'Speech Title', 'Speech URL', 'Speech Text'])  
    for speech_data in speeches_data:
        writer.writerow(speech_data)

print("Done")
