from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


driver = webdriver.Chrome();

# driver.save_screenshot('sample_screenshot_1.png');

x = driver.get_window_size()

y = driver.execute_script("return document.documentElement.scrollHeight")

print (x)
print (y)
print(x['height'])
str1 = ""
str2 = ""
def takeRollingPic():
    count = 1
    for i in range(x['height'],y,x['height']):
        str1 = "window.scrollTo(0, " + str(i) +  ");"
        driver.execute_script(str1)
        str2 = "court_screenshot_" + str(count) + ".png"
        driver.save_screenshot(str2);
        count += 1
        time.sleep(3)
