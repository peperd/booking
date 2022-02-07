# This file is going to include method that will parse
# The specific data that we need from one of deal boxes.

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class BookingReport:
    def __init__(self, boxes_section_element: WebElement):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements(By.CLASS_NAME, "fc21746a73")

    def pull_data(self):
        collection = []
        for deal_box in self.deal_boxes:
            # pulling the hotel name
            hotel_name = (
                deal_box.find_element(By.CLASS_NAME, "fde444d7ef")
                .get_attribute("innerHTML")
                .strip()
            )
            # pulling prices
            hotel_price = (
                deal_box.find_element(By.CLASS_NAME, "_e885fdc12")
                .get_attribute("innerHTML")
                .strip("€&nbsp;")
            )
            # pulling hotel scores
            hotel_score = (
                deal_box.find_element(
                    By.CSS_SELECTOR, 'div[class="_9c5f726ff bd528f9ea6"]'
                )
                .get_attribute("innerHTML")
                .strip()
            )
            collection.append([hotel_name, hotel_price, hotel_score])
        return collection
