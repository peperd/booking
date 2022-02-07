from selenium import webdriver
from booking import constants as const
from booking.filtration import BookingFiltration
from booking_report import BookingReport
from selenium.webdriver.common.by import By
from prettytable import PrettyTable
import os

CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH", "./chromedriver")


class Booking(webdriver.Chrome):
    def __init__(self, executable_path=CHROME_DRIVER_PATH, teardown=False):
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitchers", ["enable-logging"])
        super(Booking, self).__init__(executable_path=executable_path)
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    # method that change currency to EUR
    def change_currency(self, currency=None):
        currency_element = self.find_element(
            By.XPATH, '/html/body/header/nav[1]/div[2]/div[1]/button'
        )
        currency_element.click()
        selected_currency_element = self.find_element(
            By.CSS_SELECTOR,
            f'a[data-modal-header-async-url-param*="selected_currency={currency}"]',
        )
        selected_currency_element.click()

    # method that put the destination point to search field
    def select_place_to_go(self, place_to_go):
        search_field = self.find_element(By.ID, "ss")
        search_field.clear()
        search_field.send_keys(place_to_go)
        first_result = self.find_element(By.CSS_SELECTOR, 'li[data-i="0"]')
        first_result.click()

    # method that put the check in and check out dates to calendar
    def select_dates(self, check_in_date, check_out_date):
        check_in_element = self.find_element(
            By.CSS_SELECTOR, f'td[data-date="{check_in_date}"]'
        )
        check_in_element.click()
        check_out_element = self.find_element(
            By.CSS_SELECTOR, f'td[data-date="{check_out_date}"]'
        )
        check_out_element.click()

    # method that change number of travelling adults
    def select_adults(self, adults):
        selection_element = self.find_element(By.ID, "xp__guests__toggle")
        selection_element.click()
        while True:
            decrease_adult_element = self.find_element(
                By.XPATH, '/html/body/div[1]/div/div/div[2]/form/div[1]/div[3]/div[2]/div/div/div[1]/div/div[2]/button[1]'
            )
            decrease_adult_element.click()
            adults_value_element = self.find_element(
                By.CSS_SELECTOR, 'span[data-bui-ref="input-stepper-value"]'
            )
            adults_value = adults_value_element.get_attribute("value")
            if adults_value == 1:
                break
            increase_button_element = self.find_element(
                By.XPATH,
                '//*[@id="xp__guests__inputs-container"]/div/div/div[1]/div/div[2]/button[2]',
            )
            for i in range(1, adults):
                if i < adults:
                    increase_button_element.click()
                if i == adults:
                    break
            break

    # method that perform search
    def search_button(self):
        search_button = self.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_button.click()

    # method that  filter results and show only 4 and 5 star hotels
    # and sorts results by best rating score
    def apply_filtration(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating()
        filtration.lowest_price_best_score()

    # method that  print results to table
    def report_results(self):
        hotel_boxes = self.find_element(By.ID, "search_results_table")
        report = BookingReport(hotel_boxes)
        table = PrettyTable(
            field_names=["Hotel Name", "Hotel Price (EUR)", "Hotel Score"]
        )
        table.add_rows(report.pull_data())
        with open("table.txt", 'w') as f:
            print(
                table.get_string(
                    sortby="Hotel Price (EUR)",
                    sort_key=lambda x: int(x[2].replace(" ", "")),
                ), file=f
            )
