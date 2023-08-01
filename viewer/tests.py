import time

from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from selenium.common import NoAlertPresentException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By


# Create your tests here.
class GenreFromTest(LiveServerTestCase):

	def test_book_select(self):
		driver = webdriver.Chrome()

		driver.get("http://127.0.0.1:8000/")
		time.sleep(2)
		book = driver.find_element(By.ID, 'new-book')
		book.click()
		time.sleep(3)

	#
# 	def test_sign_up(self):
# 		driver = webdriver.Chrome()
#
# 		driver.get("http://127.0.0.1:8000/")
# 		# time.sleep(2)
# 		login = driver.find_element(By.ID, 'sign-up-btn')
# 		login.click()
# 		# time.sleep(2)
# 		form_username = driver.find_element(By.ID, 'id_username')
# 		form_first_name = driver.find_element(By.ID, 'id_first_name')
# 		form_last_name = driver.find_element(By.ID, 'id_last_name')
# 		form_email = driver.find_element(By.ID, 'id_email')
# 		form_password1 = driver.find_element(By.ID, 'id_password1')
# 		form_password2 = driver.find_element(By.ID, 'id_password2')
# 		form_username.send_keys('tmalinky')
# 		form_first_name.send_keys('Tomáš')
# 		form_last_name.send_keys('Malý')
# 		form_email.send_keys('malinkyt@gmail.com')
# 		form_password1.send_keys('pass123456')
# 		form_password2.send_keys('pass123456')
# 		# time.sleep(2)
# 		form_submit = driver.find_element(By.ID, 'btn-submit')
# 		form_submit.click()
# 		# time.sleep(2)
# #
# 		login = driver.find_element(By.ID, 'login-id')
# 		login.click()
# 		# time.sleep(2)
# 		form_username = driver.find_element(By.ID, 'id_username')
# 		form_password = driver.find_element(By.ID, 'id_password')
# 		form_username.send_keys('tmalinky')
# 		form_password.send_keys('pass123456')
# 		# time.sleep(2)
# 		form_submit = driver.find_element(By.ID, 'btn-submit')
# 		form_submit.click()
# 		# time.sleep(2)
#
# 		book = driver.find_element(By.ID, 'new-book')
# 		book.click()
# 		# time.sleep(3)
#
# 		logout = driver.find_element(By.ID, 'logout-btn')
# 		logout.click()
# 		# time.sleep(2)

	# def test_login(self):
	# 	driver = webdriver.Chrome()
	#
	# 	driver.get("http://127.0.0.1:8000/")
	# 	# time.sleep(2)
	# 	login = driver.find_element(By.ID, 'login-id')
	# 	login.click()
	# 	# time.sleep(2)
	# 	form_username = driver.find_element(By.ID, 'id_username')
	# 	form_password = driver.find_element(By.ID, 'id_password')
	# 	form_username.send_keys('rkachyna')
	# 	form_password.send_keys('123456')
	# 	# time.sleep(2)
	# 	form_submit = driver.find_element(By.ID, 'btn-submit')
	# 	form_submit.click()
	# 	# time.sleep(2)
	#
	# 	users = driver.find_element(By.ID, 'users-page')
	# 	users.click()
	# 	# time.sleep(2)
	# 	user = driver.find_element(By.ID, 'user-page')
	# 	user.click()
	# 	time.sleep(2)
	# 	user = driver.find_element(By.ID, 'extend-btn')
	# 	user.click()
	# 	time.sleep(4)
	# 	try:
	# 		driver.switchTo.alert().accept()
	# 		# print(f"alert: {alert}")
	# 		# alert.accept()
	# 	except:
	# 		pass
	# 	logout = driver.find_element(By.ID, 'logout-btn')
	# 	logout.click()
	# 	time.sleep(2)

	# def test_order_book(self):
	# 	driver = webdriver.Chrome()
	#
	# 	driver.get("http://127.0.0.1:8000/")
	# 	time.sleep(2)
	# 	login = driver.find_element(By.ID, 'login-id')
	# 	login.click()
	# 	time.sleep(2)
	# 	form_username = driver.find_element(By.ID, 'id_username')
	# 	form_password = driver.find_element(By.ID, 'id_password')
	# 	form_username.send_keys('tmalinky')
	# 	form_password.send_keys('pass123456')
	# 	time.sleep(2)
	# 	form_submit = driver.find_element(By.ID, 'btn-submit')
	# 	form_submit.click()
	# 	time.sleep(2)
	#
	# 	book = driver.find_element(By.ID, 'new-book')
	# 	book.click()
	# 	time.sleep(2)
	#
	# 	borrow = driver.find_element(By.ID, 'borrow-book')
	# 	borrow.click()
	# 	time.sleep(2)
	#
	# 	cart = driver.find_element(By.ID, 'cart')
	# 	cart.click()
	# 	time.sleep(2)
	#
	# 	order = driver.find_element(By.ID, 'finish-button')
	# 	order.click()
	# 	time.sleep(2)
	#
	# 	orders = driver.find_element(By.ID, 'orders')
	# 	orders.click()
	# 	time.sleep(2)
	#
	# 	logout = driver.find_element(By.ID, 'logout-btn')
	# 	logout.click()
	# 	time.sleep(2)
