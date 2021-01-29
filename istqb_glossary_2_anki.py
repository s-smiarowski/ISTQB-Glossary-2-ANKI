import webbrowser, sys, logging, genanki, os, pyperclip, pprint
from selenium import webdriver
from selenium.webdriver.support.ui import Select
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.DEBUG)

browser = webdriver.Chrome()
browser.get('https://glossary.istqb.org/pl/search') # go to the ISTQB Glossary page
browser.find_element_by_css_selector('#menu-space > div > form > div.advance-search').click() # advance search options
browser.find_element_by_css_selector('#advance-search-area > div > div.col-md-6.syllabi > span:nth-child(4)').click() # deselect all
browser.find_element_by_css_selector('#advance-search-area > div > div.col-md-6.syllabi > label:nth-child(7) > input[type=checkbox]').click() # select ISTQB Foundation V3.1 2018
browser.find_element_by_css_selector('#advance-search-area > div > div.col-md-6.methods > input[type=checkbox]:nth-child(19)').click() #  multi language display
language_select = Select(browser.find_element_by_css_selector('#advance-search-area > div > div.col-md-6.methods > div:nth-child(21) > select:nth-child(1)'))  # Documentation https://selenium-python.readthedocs.io/navigating.html
language_select.select_by_value("48") # Polish as a secondary language
browser.find_element_by_css_selector('#advance-search-area > div > div.col-md-6.methods > span.advance-search-btn.pull-right').click()
browser.implicitly_wait(3) # time in seconds https://selenium-python.readthedocs.io/waits.html

glossary = []

for j in range(1,13): # 13
    for i in range(3,23): # 23
        try:
            glossary.append({ # list of dictionaries creation 
                'term_eng': browser.find_element_by_css_selector(f"#app > div > div:nth-child(4) > div > div.search-results > div:nth-child({i}) > div.term-row > div > div.term-heading").text,
                'desc_eng': "".join(browser.find_element_by_css_selector(f"#app > div > div:nth-child(4) > div > div.search-results > div:nth-child({i}) > div.term-row > div > div.term-definition-preview").text),
                'term_pl': browser.find_element_by_css_selector(f"#app > div > div:nth-child(4) > div > div.search-results > div:nth-child({i}) > div:nth-child(2) > div > div > div.term-heading").text,
                'desc_pl': browser.find_element_by_css_selector(f"#app > div > div:nth-child(4) > div > div.search-results > div:nth-child({i}) > div:nth-child(2) > div > div > div.term-definition-preview").text.replace('\n\t',' ')
            })
        except: logging.info('element has not been found')
        logging.info("page(j): " + str(j) + ", term(i): " + str(i))
    try:
        browser.find_element_by_css_selector(f"span[data-page='{j+1}']").click()
    except:
        logging.info("there are no more pages to click"
    browser.implicitly_wait(3)


genanki_model_istqb = genanki.Model(
  4400040004,
  'ISTQB FL',
  fields=[
    {'name': 'Question'},
    {'name': 'Question_PL'},
    {'name': 'Answer'},
    {'name': 'Answer_PL'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}}<br>-<br>{{Question_PL}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}<br>-<br>{{Answer_PL}}',
    },
  ])

genanki_deck_istqb = genanki.Deck(
  4400040005,
  'ISTQB FL')


for i in glossary:
    field1 = i['term_eng']
    field2 = i['term_pl']
    field3 = i['desc_eng']
    field4 = i['desc_pl']
    my_note = genanki.Note(
    model=genanki_model_istqb,
    fields=[field1, field2, field3, field4])
    genanki_deck_istqb.add_note(my_note)


genanki.Package(genanki_deck_istqb).write_to_file('istqb_glossary.apkg')


browser.quit()
# pprint.pprint(glossary)