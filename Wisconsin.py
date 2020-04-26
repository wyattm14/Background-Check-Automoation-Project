from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# To store all the cases heppened to one perosn or people who have the same name
caseLinks = []

# headless browser
# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('window-size=1200x600')
# browser = webdriver.Chrome(chrome_options=options)
browser = webdriver.Chrome()
# browser.get("https://publicindex.sccourts.org/Chesterfield/PublicIndex/PISearch.aspx")
browser.get("https://wcca.wicourts.gov/case.html")
# PROBLEM!!!can load other pages
# python_button = browser.find_element_by_xpath('//*[@id="ContentPlaceHolder1_ButtonAccept"]')
# python_button.click()

def login(firstname, lastName):
    webElement = browser.find_elements_by_xpath('//*[@id="lastName"]')[0]
    webElement.send_keys(lastName)
    webElement = browser.find_elements_by_xpath('//*[@id="home-container"]/main/div/form/div[2]/div[3]/div/fieldset/div[1]/div[2]/div/label/input')[0]
    webElement.send_keys(firstname)
    webElement = browser.find_elements_by_xpath('//*[@id="home-container"]/main/div/form/div[4]/div/button[1]')[0]
    webElement.submit()

# Test to see if there are multiple results out
# True => Yes
# False => NO
def checkSearchResult():
    if(browser.current_url == 'https://wcca.wicourts.gov/caseSearchResults.html'):
        return True
        # get case number from the url maybe
    else:
        return False

def getTotalCaseAmount():
    total = []
    webElement = browser.find_element_by_xpath(
        '//*[@id="caseSearchResults_info"]').text
    str = webElement.split(" ")
    filter_number = checkInt(str)[1]-checkInt(str)[0]+1
    total_results_num = checkInt(str)[len(checkInt(str))-1]
    page_num = int(total_results_num/filter_number)+1
    total.append(filter_number)
    total.append(total_results_num)
    total.append(page_num)

    return total

def checkInt(arr):
    num = []
    for i in arr:
        if(i.isdigit()):
            num.append(int(i))
        else:
            pass
    return num

# Grab the case numbers from the webpage
def grabCaseNumber():
    arr1 = getTotalCaseAmount()
    f_num = arr1[0] # filter_number
    t_re_num = arr1[1] # total_result_num
    p_num = arr1[2] # page_num
    total_links = []

    for i in range(1, 1+p_num):
        xpath = '//*[@id="caseSearchResults_paginate"]/ul/li[' + str((i+1)) + ']/a'
        webElement = browser.find_element_by_xpath(xpath)
        webElement.click()

        caseLinks = []
        caseLinks = browser.find_elements_by_xpath('//*[@id="caseSearchResults"]/tbody/tr/td[1]/a') # an array of webdriver objects
        for links in caseLinks:
            total_links.append(links.get_attribute('href'))

    print("Total links got: ", len(total_links))
    print("Total link num(inspected): ", t_re_num)

    return total_links

# get Personal case document
def getDoc():
    # if there are multiple results, then grab those cases numbers
    if(checkSearchResult()):
        link_arr = grabCaseNumber()
        for i in link_arr:
            print(i)
            browser.get(i + "&mode=details")
            str1 = ""
            str2 = ""
            x = browser.get_window_size()
            y = browser.execute_script("return document.documentElement.scrollHeight")
            count = 1
            for i in range(x['height'], y, x['height']):
                str1 = "window.scrollTo(0, " + str(i) + ");"
                browser.execute_script(str1)
                str2 = "court_screenshot_" + str(count) + ".png"
                browser.save_screenshot(str2)
                count += 1
                time.sleep(3)
    else:
        # if there is only one case, go directly to the case file
        url = browser.current_url
        browser.get(url + "&mode=details")
        str1 = ""
        str2 = ""
        x = browser.get_window_size()
        y = browser.execute_script("return document.documentElement.scrollHeight")
        count = 1
        for i in range(x['height'], y, x['height']):
            str1 = "window.scrollTo(0, " + str(i) + ");"
            browser.execute_script(str1)
            str2 = "court_screenshot_" + str(count) + ".png"
            browser.save_screenshot(str2)
            count += 1
            time.sleep(3)

# def turnPage(curr_page):
#     webElement = browser.find_element_by_xpath('//*[@id="caseSearchResults_next"]/a')
#     webElement.click()


login('Emmanuell', 'Miller')
time.sleep(2)
getDoc()
