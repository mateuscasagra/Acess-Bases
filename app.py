
from selenium import webdriver
from selenium.webdriver.common.by import By


user_cnpj = ""
user_email= ""
user_senha = ""



options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.get("https://mob.nox.com.br/Login")
driver.implicitly_wait(0.5)
login = driver.find_element(By.NAME, value="cnpj").send_keys(user_cnpj)
email = driver.find_element(By.NAME, value="user").send_keys(user_email)
senha = driver.find_element(By.NAME, value="password").send_keys(user_senha)
submit_button = driver.find_element(By.ID, value="btnLogin").click()
