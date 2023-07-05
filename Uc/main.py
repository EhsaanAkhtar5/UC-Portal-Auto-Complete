from cgitb import text
from multiprocessing import Value
from multiprocessing.managers import ValueProxy
import time
import pandas
import pandas as pd
import csv

from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class Browser:
    browser, service = None, None

    def __init__(self, driver: str):
        self.service = Service(driver)
        self.browser = webdriver.Chrome(service=self.service)

    def open_page(self, url: str):
        self.browser.get(url)

    def close_browser(self):
        self.browser.close()

    def add_input(self, by: By, value: str, text: str):
        field = self.browser.find_element(by=by, value=value)
        field.send_keys(text)
        time.sleep(1)

    def drop_down(self, by: By, value: str, text: str):
        dropdown = Select(self.browser.find_element(by=by, value=value))
        dropdown.select_by_visible_text(text)
        time.sleep(1)

    def click_button(self, by: By, value: str):
        button = self.browser.find_element(by=by, value=value)
        button.click()

    def text_field(self, by: By, value: str, text: str):
        text_field = self.browser.find_element(by=by, value=value)
        text_field.send_keys(text)

    def login_likedin(self, username: str, password: str):
        self.add_input(by=By.ID, value="id-userName", text=username)
        self.add_input(by=By.ID, value="id-password", text=password)
        self.click_button(by=By.ID, value="id-submit-button")

    def List_loop(self, by: By, value: str, i: int, j: int,links: str):
        Temp_List_For_Join = []
        Temp_List_For_Join_2 = []
        Panal_data = self.browser.find_elements(by=by, value=value)
        for e in Panal_data:
            a = e.text.replace('\n', ' ')
            Curr = a.split(' ')
            for x in range(len(Curr)):
                if '(' in Curr[x]:
                    point_1 = str(Temp_List_For_Join)
                    point_2 = (Curr[x].replace('(', '') + ' ' + Curr[x + 1] + ' ' + Curr[x + 2].replace(')', ''))
                    break
                Temp_List_For_Join.append(Curr[x])
            for x in range(len(Curr)):
                if 'Complete' in Curr[x]:
                    point_3 = (Curr[x - 2] + ' ' + Curr[x - 1])
                if x == (len(Curr) - 1):
                    point_4 = (Curr[x - 2] + ' ' + Curr[x - 1] + ' ' + Curr[x])
                    break
            try:
                Temp_List_For_Join_2.append(
                    [point_1.replace('[', '').replace(']', '').replace("'", '').replace(',', ' '), point_2, point_3,
                     point_4,str(links.replace('[', '').replace(']', '').replace("'", ''))])
            except:
                point_3 = (Curr[-2] + ' ' + Curr[-1])
                Temp_List_For_Join_2.append(
                    [point_1.replace('[', '').replace(']', '').replace("'", '').replace(',', ' '), point_2, point_3,str(links.replace('[', '').replace(']', '').replace("'", ''))])
        Pulled_Data.extend(Temp_List_For_Join_2)
        if i == j - 1:
            Data = pandas.DataFrame()
            Data = Data.append(Pulled_Data)
            Data.to_csv('DataPulled.csv')

    def List_click_loop(self, by: By, value: str):
        Clickable_list = []
        Links = []
        Get_length_List = self.browser.find_elements(by=by, value=value)
        for e in Get_length_List:
            if ("Provide tenancy details" in e.text and 'New claim' not in e.text) or ("Confirm tenant's housing costs" in e.text):
                Clickable_list.append(e)
        j = len(Clickable_list)
        for i in range(j):
            List = self.browser.find_elements(by=by, value=value)
            for e in List:
                if ("Provide tenancy details" in e.text and 'New claim' not in e.text) or ("Confirm tenant's housing costs" in e.text):
                    Clickable_list.append(e)
                    Links.append(e.get_attribute('href'))
            Clickable_list[i].click()
            browser.List_loop(by=By.CLASS_NAME, value='panel', i=i, j=j,links=Links[i])

            browser.click_button(by=By.ID, value="tenancy-details-requests")
            Clickable_list.clear()



    def Test(self, by: By, value: str):
        print((self.browser.find_element(by=By.CLASS_NAME, value="task-list__link")).get_attribute("href"))


    def Confirm_Tenent(self, row ):
        browser.click_button(by=By.ID, value='isATenant-clickable-true')
        browser.click_button(by=By.ID, value='id-submit-button')
        time.sleep(1)
        browser.drop_down(by=By.ID, value='id-rentPaymentFrequency', text=row[8])
        browser.text_field(by=By.ID, value='id-rentAmount', text=row[9])
        if row[12] == 'Yes':
            browser.click_button(by=By.ID, value='isServiceCharges-clickable-true')
            browser.drop_down(by=By.ID, value='id-serviceChargesPaymentFrequency', text=row[8])
            browser.text_field(by=By.ID, value='id-serviceChargesAmount', text=row[10])
        else:
            browser.click_button(by=By.ID, value='isServiceCharges-clickable-false')
        if row[8] == 'Weekly':
            browser.click_button(by=By.ID, value='effectiveDateRadio-clickable-weeklyRentEffectiveDate')
        else:
            browser.click_button(by=By.ID, value='effectiveDateRadio-clickable-monthlyRentEffectiveDate')
        browser.click_button(by=By.ID, value='id-submit-button')
        browser.click_button(by=By.ID, value="tenancy-details-requests")
        time.sleep(1)


    def Provide_Tenent(self, row):
        browser.click_button(by=By.ID, value='isATenant-clickable-true')
        time.sleep(1)
        browser.text_field(by=By.ID, value='id-rentReference', text=row[4])
        time.sleep(1)
        browser.click_button(by=By.ID, value='id-submit-button')
        if row[13] == 'yes':
            browser.click_button(by=By.ID, value='temporaryAccommodation-clickable-true')
        else:
            browser.click_button(by=By.ID, value='temporaryAccommodation-clickable-false')
        time.sleep(1)
        if int(row[5]) > 1:
            browser.click_button(by=By.ID, value='jointTenancy-clickable-true')
            browser.add_input(by=By.ID, value='id-tenants', text=row[5])
            try:
                browser.click_button(by=By.ID, value='bothNamedOnTenancy-clickable-true')
            except:
                print('ok')
        else:
            browser.click_button(by=By.ID, value='jointTenancy-clickable-false')
        browser.drop_down(by=By.ID, value='id-numberOfBedrooms', text=row[6])
        if row[7] != '0':
            browser.click_button(by=By.ID, value='rentFreeWeeks-clickable-true')
            browser.text_field(by=By.ID, value='id-numberOfRentFreeWeeks', text=row[7])
        else:
            browser.click_button(by=By.ID, value='rentFreeWeeks-clickable-false')
        browser.click_button(by=By.ID, value='id-submit-button')
        browser.text_field(by=By.ID, value='id-rentAmount', text=row[9])
        browser.drop_down(by=By.ID, value='id-rentPaymentFrequency', text=row[8])
        if row[12] == 'Yes':
            browser.click_button(by=By.ID, value='serviceChargesExists-clickable-true')
            browser.text_field(by=By.ID, value='id-eligibleServiceChargeAmount', text=row[10])
            browser.drop_down(by=By.ID, value='id-eligibleServiceChargeFrequency', text=row[8])
        else:
            browser.click_button(by=By.ID, value='serviceChargesExists-clickable-false')
        time.sleep(1)
        browser.click_button(by=By.ID, value='id-submit-button')
        browser.click_button(by=By.ID, value="tenancy-details-requests")

    def No_Match(self):
        browser.click_button(by=By.ID, value='isATenant-clickable-false')
        browser.text_field(by=By.ID, value='id-noDetails', text='Person does not have a tenancy under us')
        try:
            browser.click_button(by=By.ID, value='acceptingOtherCharges-clickable-false')
        except:
            print('Confirm')


    def Run2_1(self, by: By, value: str):
        Panal_data = []
        with open('UC_data_test5.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                browser.open_page(row[14])
                time.sleep(1)
                Data = self.browser.find_elements(by=By.CLASS_NAME, value='panel')
                Panal_data.clear()
                for h in Data:
                    Panal_data.append(h.text.replace('\n', ' ').split(' '))
                l = self.browser.find_element(by=By.ID, value='main-heading')
                if 'Welcome back' in l.text:
                    browser.click_button(by=By.ID, value="tenancy-details-requests")
                else:
                    Split_row = row[0].split(' ')
                    if Split_row[0] in Panal_data[0]:
                        if "Confirming your tenant's housing costs" in l.text:
                            browser.Confirm_Tenent(row=row)
                        else:
                            browser.Provide_Tenent(row=row)
                        Split_row.clear()
                    else:
                        browser.No_Match()

    def Two_factor(self):
        with open('R:\\_Shared Content\\Corporate Services\\Business Systems\\tmp\Auto_vari.txt', 'r') as f:
            for line in f:
                for word in line.split():
                    text1 = word
            self.add_input(by=By.ID, value="id-accessCode", text=text1)
            self.click_button(by=By.ID, value="id-submit-button")


if __name__ == "__main__":
    Run = 1
    username = "***************.org.uk"
    password = "*********"
    url = "https://portal.universal-credit.service.gov.uk/sign-in"
    Pulled_Data = []
    browser = Browser("C:\Program Files (x86)\chromedriver.exe")
    browser.open_page(url)
    time.sleep(6)
    browser.login_likedin(username, password)
    time.sleep(10)
    browser.Two_factor()
    time.sleep(1)
    browser.click_button(by=By.ID, value="tenancy-details-requests")
    time.sleep(2)
    if Run == 3:
        browser.Test(by=By.TAG_NAME, value="li")
    if Run == 1:
        browser.List_click_loop(by=By.CLASS_NAME, value="task-list__link")
    if Run == 2:
        browser.Run2_1(by=By.TAG_NAME, value="li")
    browser.close_browser()


