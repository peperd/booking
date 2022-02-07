# This file will include a class  with instance methods
# That will be responsible to interact with website
# After we have results, to apply filtration: 
# Filter 4 and 5 star hotel and sort results by rating score of hotel

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import time


class BookingFiltration:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def apply_star_rating(self):
        four_star = self.driver.find_element(
            By.XPATH, '//*[@id="searchboxInc"]/div[1]/div/div/div[1]/div[7]/div[5]/label/div/div/div/div/div/div')
        for i in range(3):
            i = 0
            if four_star.is_displayed():
                four_star.click()
                break
            else:
                time.sleep(5)
                i += 1
        time.sleep(5)
        five_star = self.driver.find_element(
            By.XPATH, '//*[@id="searchboxInc"]/div[1]/div/div/div[1]/div[7]/div[6]/label/div/div/div/div/div/div')
        for j in range(3):
            j = 0
            if five_star.is_displayed():
                five_star.click()
            else:
                time.sleep(5)
                j += 1

    def lowest_price_best_score(self):
        time.sleep(5)
        elem = self.driver.find_element(By.CLASS_NAME, '_aa3362ea2')
        if elem.is_displayed():
            elem.click()
        else:
            time.sleep(5)
            self.driver.find_element(By.XPATH, '//*[@id="ajaxsrwrap"]/div[1]/div/div/div[2]/ul/li[10]/a').click()
            time.sleep(5)
            self.driver.find_element(By.CLASS_NAME, 'a5b679fa41').click()
