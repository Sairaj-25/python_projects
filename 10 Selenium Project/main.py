from selenium import webdriver

from selenium.webdriver.common.by import By

# keep Chrome browser open after program finishes

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome()
driver.get("https://www.amazon.in/Puma-Polyester-Hooded-Sweatshirt-681892_Black/dp/B0CL9DM8GD/ref=sr_1_5?crid=22218VLQHJ45F&dib=eyJ2IjoiMSJ9.9ClG5IbzqZMXtGLC9usWYJkH9e1sq2aQNQG7riX03eTgZLfLiz43sOpDOa1Mn3xIpBW9_-tnx6DKkUaMn8tTAwVTqjYU7t_sAlyZNfyr_2_cKVwIh6teh0HHZfcYR8HLx1_bAegEYN6lyPDi24-ORWxsB2FMOBekm3omIhbMCUCuW4QNZzamtFLFUMT3NoY-JvLL6GhkqvH8w3EQptYz8UYNfb4YWCHZMHyaFZzoUNXh5JuOwG4eto9rZ8Q8a5pA7JMBkJH3ioAWds6wU73WA44Piv9tiGeClmPToFbhvKKLrRR6Gstk6UeKggETnEWgja7j9GmnTRG9hZWMJxnM0YPkGhKTbjB1K25sFBNB_VbjlYXCPSToymft1-JqWseMllcw70BfKVg3AXgXqPfh0M2d85pIwYo-vAsEHJDbEdzoBCE84ETSSEnnfBhbMLoF.eu4sTR63299eFSaaFwHU1UC16T7LpdWOiJFFPRQ9dWg&dib_tag=se&keywords=black+zip+hoodie+for+men+puma+nike&nsdOptOutParam=true&qid=1734710687&sprefix=black+zip+hoodie+for+men+puma+nike%2Caps%2C229&sr=8-5")

price = driver.find_element(By.CLASS_NAME, value="a-price-whole")

print(f"Price of hoodie is {price.text}")




# driver.close() # Closes the current browser window
driver.quit() # Close all browser windows and also ends the webdriver session