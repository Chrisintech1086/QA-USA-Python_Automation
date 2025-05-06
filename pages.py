import time

from pyexpat.errors import messages
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import retrieve_phone_code

class UrbanRoutesPage:
    # Addresses
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    # Tariff and call button
    supportive_plan_button = (By.XPATH, '//div[contains(text(), "Supportive")]')
    supportive_plan_card_parent = (By.XPATH, '//div[contains(text(), "Supportive")]//..')
    active_plan_card = (By.XPATH, '//div[@class="tcard active"]//div[@class="tcard-title"]')
    call_taxi_button = (By.XPATH, '//button[contains(text(), "Call a taxi")]')
    phone_number_button = (By.CLASS_NAME, 'np-text')
    phone_number_entry = (By.ID, 'phone')
    phone_code_entry = (By.ID, 'code')
    payment_method_button = (By.CLASS_NAME, 'pp-text')
    add_card_button = (By.XPATH, '//div[contains(text(), "Add card")]')
    card_number_entry = (By.ID, 'number')
    cvv_code_entry = (By.XPATH, '//input[@class="card-input" and @id="code"]')
    link_button = (By.XPATH, '//button[text()="Link"]')
    message_to_the_driver_entry = (By.ID, 'comment')
    blanket_slider = (By.CLASS_NAME, 'switch')
    blanket_slider_switch_status = (By.CLASS_NAME, 'switch-input')
    ice_cream_counter = (By.CLASS_NAME, 'counter-value')
    ice_cream_plus_button = (By.CLASS_NAME, 'counter-plus')
    order_taxi_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[4]/button')

    def __init__(self, driver):
        self.driver = driver

    def write_from(self, from_address):
        from_field = self.driver.find_element(*self.from_field)
        from_field.send_keys(from_address)

    def write_to(self, to_address):
        to_field = self.driver.find_element(*self.to_field)
        to_field.send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def click_call_taxi_button(self):
        self.driver.find_element(*self.call_taxi_button).click()

    def set_route(self, from_address, to_address):
        self.write_from(from_address)
        self.write_to(to_address)
        self.click_call_taxi_button()

    def  click_supportive_button(self):
         self.driver.find_element(*self.supportive_plan_button).click()

    def get_supportive_status(self):
        if self.driver.find_element(*self.supportive_plan_card_parent).get_attribute('class')!= "tcard active":
            card = WebDriverWait(self.driver, 3).until(
                expected_conditions.visibility_of_element_located(self.supportive_plan_button))
            self.driver.execute_script("arguments[0].scrollIntoView();", card)
            card.click()

    def get_supportive_plan_selected(self):
        return self.driver.find_element(*self.active_plan_card).text

    def click_phone_number_button(self):
        self.driver.find_element(*self.phone_number_button).click()

    def enter_phone_number(self, phone_number):
        self.driver.find_element(*self.phone_number_entry).send_keys(phone_number)
        self.driver.find_element(*self.phone_number_entry).send_keys(Keys.RETURN)

    def enter_phone_code(self, phone_code):
        self.driver.find_element(*self.phone_code_entry).send_keys(phone_code)
        self.driver.find_element(*self.phone_code_entry).send_keys(Keys.RETURN)

    def get_phone_number(self):
        return self.driver.find_element(*self.phone_number_button).text

    def click_payment_method_button(self):
        self.driver.find_element(*self.payment_method_button).click()

    def click_add_card_button(self):
        self.driver.find_element(*self.add_card_button).click()

    def press_add_card_button(self):
        self.driver.find_element(*self.add_card_button).send_keys()
        self.driver.find_element(*self.add_card_button).send_keys(Keys.RETURN)

    def enter_card_number(self, card_number):
        self.driver.find_element(*self.card_number_entry).send_keys(card_number)
        self.driver.find_element(*self.card_number_entry).send_keys(Keys.RETURN)

    def click_cvv_code_field(self):
        self.driver.find_element(*self.cvv_code_entry).click()

    def enter_cvv_code(self, cvv_code):
        self.driver.find_element(*self.cvv_code_entry).send_keys(cvv_code)
        self.driver.find_element(*self.cvv_code_entry).send_keys(Keys.RETURN)

    def click_link_button(self):
        self.driver.find_element(*self.link_button).click()

    def get_card_value(self):
        return self.driver.find_element(*self.card_number_entry).get_property("value")

    def get_cvv_code(self):
        return self.driver.find_element(*self.cvv_code_entry).get_property("value")

    def enter_message_to_the_driver(self, message):
        self.driver.find_element(*self.message_to_the_driver_entry).send_keys(message)
        self.driver.find_element(*self.message_to_the_driver_entry).send_keys(Keys.RETURN)

    def get_message_to_the_driver(self):
        return self.driver.find_element(*self.message_to_the_driver_entry).get_property("value")

    def click_blanket_slider(self):
        self.driver.find_element(*self.blanket_slider).click()

    def get_blanket_slider_switch_status(self):
        element = self.driver.find_element(*self.blanket_slider_switch_status)
        print("Found blanket slider switch element")

        # Check if the element is selected or check its attribute
        status = element.is_selected()  # or use get_attribute('checked') if it's a checkbox
        print(f"Blanket slider switch status: {status}")

        return status

    def click_ice_cream_counter_plus(self):
        self.driver.find_element(*self.ice_cream_plus_button).click()
        self.driver.find_element(*self.ice_cream_plus_button).click()

    def get_ice_cream_counter(self):
        return int(self.driver.find_element(*self.ice_cream_counter).text)

    def click_order_taxi_button(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(self.order_taxi_button))
        self.driver.find_element(*self.order_taxi_button).click()

    def get_order_taxi_button(self):
        return self.driver.find_element(*self.order_taxi_button).is_displayed()