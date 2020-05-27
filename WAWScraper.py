from selenium import webdriver
from bs4 import BeautifulSoup
from time import *
import pyautogui
import re
import csv

CONTACT = "Deadwoods"
WEBSITE = "https://web.whatsapp.com"
OUTPUT_FILE = "chat_data.csv"
MESSAGE_LIST = []

def load_driver():
	options = webdriver.ChromeOptions();
	options.add_argument('--user-data-dir=./User_Data')
	driver = webdriver.Chrome(options=options)
	driver.get(WEBSITE)
	print("Scan QR code quickly")
	sleep(20)
	return driver

def select_chat(driver):
	user = driver.find_element_by_xpath("//span[@title='{}']".format(CONTACT))
	user.click()
	return

def get_messages(driver, message_list):
	htmlpage = (driver.page_source).encode('utf-8')
	soup = BeautifulSoup(htmlpage, features="html.parser")
	#message_list = []

	for message in soup.find_all("div", class_=["Tkt2p"]):

		if message not in message_list:	
			message_list.append(message)
			#print(type(message))
			message_data = str(message.find("div", class_="copyable-text"))
			message_raw = message.find("div", class_="_3zb-j")

			if message_raw.find("img"):
				emoji = message_raw.find_all("img")
				message_text = ""
				for i in emoji:
					message_text += i.attrs.get('data-plain-text')
				message_text += message_raw.get_text()
			else:
				message_text = message_raw.get_text()

			with open(OUTPUT_FILE, 'a', newline='', encoding='utf-8') as x:
				writer = csv.writer(x)
				writer.writerow([re.search('\, (.*)\]', message_data).group(1),
					re.search('\[(.*)\, ', message_data).group(1),
					re.search('\] (.*)\: "', message_data).group(1),
					message_text])

	return

def scroll_up():
	pyautogui.press('pageup', presses=3)

def main():

	driver = load_driver()
	while True:		
		select_chat(driver)
		get_messages(driver, MESSAGE_LIST)
		scroll_up()
		#print('do we print?')

if __name__ == '__main__':
	main()
