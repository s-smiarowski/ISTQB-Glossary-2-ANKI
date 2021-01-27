### ISTQB Glossary to ANKI flashcards deck builder
### Simple script for building Anki deck from ISTQB glossary page
### It's scrapping page searching for terms in two langages, 
### then building python deictionary from this data.
### and Finaly creating  Anki deck for future easy memorizing the terms


import webbrowser, sys, pyperclip, os, pprint, logging
from selenium import webdriver
from selenium.webdriver.support.ui import Select
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.DEBUG)

clear = lambda: os.system('cls') # utowrzenie metody clear w consoli

browser = webdriver.Chrome()
browser.get('https://glossary.istqb.org/pl/search') # go to the ISTQB Glossary page
browser.find_element_by_css_selector('#menu-space > div > form > div.advance-search').click() # advance search options
browser.find_element_by_css_selector('#advance-search-area > div > div.col-md-6.syllabi > span:nth-child(4)').click() # deselect all
browser.find_element_by_css_selector('#advance-search-area > div > div.col-md-6.syllabi > label:nth-child(7) > input[type=checkbox]').click() # select ISTQB Foundation V3.1 2018
browser.find_element_by_css_selector('#advance-search-area > div > div.col-md-6.methods > input[type=checkbox]:nth-child(19)').click() #  Multi Language Display
language_select = Select(browser.find_element_by_css_selector('#advance-search-area > div > div.col-md-6.methods > div:nth-child(21) > select:nth-child(1)'))  # Documentation https://selenium-python.readthedocs.io/navigating.html
language_select.select_by_value("48") # Chose Polish as a secondary language
browser.find_element_by_css_selector('#advance-search-area > div > div.col-md-6.methods > span.advance-search-btn.pull-right').click()
browser.implicitly_wait(3) # seconds https://selenium-python.readthedocs.io/waits.html

glossary = []

for j in range(1,13):
    for i in range(3,23):
        try:
            glossary.append({ # stworzenie listy slownikow
                'term_eng': browser.find_element_by_css_selector(f"#app > div > div:nth-child(4) > div > div.search-results > div:nth-child({i}) > div.term-row > div > div.term-heading").text,
                'desc_eng': "".join(browser.find_element_by_css_selector(f"#app > div > div:nth-child(4) > div > div.search-results > div:nth-child({i}) > div.term-row > div > div.term-definition-preview").text),
                'term_pl': browser.find_element_by_css_selector(f"#app > div > div:nth-child(4) > div > div.search-results > div:nth-child({i}) > div:nth-child(2) > div > div > div.term-heading").text,
                'desc_pl': browser.find_element_by_css_selector(f"#app > div > div:nth-child(4) > div > div.search-results > div:nth-child({i}) > div:nth-child(2) > div > div > div.term-definition-preview").text.replace('\n\t',' ')
            })
        except: logging.info('element has not been found')
        logging.info("strona(j): " + str(j) + ", term(i): " + str(i))
    try:
        browser.find_element_by_css_selector(f"span[data-page='{j+1}']").click()
    except:
        logging.info("there are no more pages to click")
    # if j==1: browser.implicitly_wait(3)
    browser.implicitly_wait(3)

# line = line.replace('\n','')
browser.quit()
# clear() # czyszczenie consoli
# pprint.pprint(glossary)
print(str(len(glossary)) + 'results')


### Known issues:
### -script is finding only 237-238 terms from avaliable 239
### -there are unnecesery new line sighns in desc_eng/desc_pl
### -waits should be changed