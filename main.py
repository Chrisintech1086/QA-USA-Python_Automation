import time

import data
import helpers
from selenium import webdriver

from pages import UrbanRoutesPage


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        # do not modify - we need additional logging enabled in order to retrieve phone confirmation code
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(5)
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            print("Cannot connect to Urban Routes. Check the server is on and still running")

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        urban_routes_page = UrbanRoutesPage(self.driver)
        urban_routes_page.set_route('East 2nd Street, 601', '1300 1st St')
        time.sleep(3)
        assert urban_routes_page.get_from() == data.ADDRESS_FROM
        assert urban_routes_page.get_to() == data.ADDRESS_TO

    def test_select_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        urban_routes_page = UrbanRoutesPage(self.driver)
        urban_routes_page.write_from(data.ADDRESS_FROM)
        urban_routes_page.write_to(data.ADDRESS_TO)
        urban_routes_page.click_call_taxi_button()
        urban_routes_page.click_supportive_button()
        time.sleep(3)
        assert urban_routes_page.get_supportive_plan_selected() == 'Supportive'


    def test_fill_phone_number(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        urban_routes_page = UrbanRoutesPage(self.driver)
        urban_routes_page.write_from(data.ADDRESS_FROM)
        urban_routes_page.write_to(data.ADDRESS_TO)
        urban_routes_page.click_call_taxi_button()
        urban_routes_page.click_phone_number_button()
        urban_routes_page.enter_phone_number(data.PHONE_NUMBER)
        code = helpers.retrieve_phone_code(self.driver)
        urban_routes_page.enter_phone_code(code)
        time.sleep(3)
        assert urban_routes_page.get_phone_number() == data.PHONE_NUMBER

    def test_fill_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        urban_routes_page = UrbanRoutesPage(self.driver)
        urban_routes_page.write_from(data.ADDRESS_FROM)
        urban_routes_page.write_to(data.ADDRESS_TO)
        urban_routes_page.click_call_taxi_button()
        urban_routes_page.click_payment_method_button()
        urban_routes_page.click_add_card_button()
        urban_routes_page.enter_card_number(data.CARD_NUMBER)
        time.sleep(3)
        urban_routes_page.enter_cvv_code(data.CARD_CODE)
        time.sleep(3)
        urban_routes_page.click_link_button()
        time.sleep(3)
        assert urban_routes_page.get_card_value() == data.CARD_NUMBER
        assert urban_routes_page.get_cvv_code() == data.CARD_CODE

    def test_comment_for_driver(self):
            self.driver.get(data.URBAN_ROUTES_URL)
            urban_routes_page = UrbanRoutesPage(self.driver)
            urban_routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
            urban_routes_page.enter_message_to_the_driver(data.MESSAGE_FOR_DRIVER)
            time.sleep(3)
            assert urban_routes_page.get_message_to_the_driver() == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        urban_routes_page = UrbanRoutesPage(self.driver)
        urban_routes_page.write_from(data.ADDRESS_FROM)
        urban_routes_page.write_to(data.ADDRESS_TO)
        urban_routes_page.click_call_taxi_button()
        urban_routes_page.click_supportive_button()
        urban_routes_page.click_blanket_slider()
        time.sleep(3)
        assert urban_routes_page.get_blanket_slider_switch_status()


    def test_order_2_ice_creams(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        urban_routes_page = UrbanRoutesPage(self.driver)
        urban_routes_page.write_from(data.ADDRESS_FROM)
        urban_routes_page.write_to(data.ADDRESS_TO)
        urban_routes_page.click_call_taxi_button()
        urban_routes_page.click_supportive_button()
        urban_routes_page.click_ice_cream_counter_plus()
        time.sleep(3)
        assert urban_routes_page.get_ice_cream_counter() == 2

    def test_car_search_model_appears(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        urban_routes_page = UrbanRoutesPage(self.driver)
        urban_routes_page.write_from(data.ADDRESS_FROM)
        urban_routes_page.write_to(data.ADDRESS_TO)
        urban_routes_page.click_call_taxi_button()
        urban_routes_page.click_supportive_button()
        urban_routes_page.enter_message_to_the_driver(data.MESSAGE_FOR_DRIVER)
        urban_routes_page.click_order_taxi_button()
        time.sleep(3)
        assert urban_routes_page.get_message_to_the_driver() == data.MESSAGE_FOR_DRIVER
        assert urban_routes_page.get_order_taxi_button() == True


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()