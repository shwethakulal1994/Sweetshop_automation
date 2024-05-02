import random
from multiprocessing import context

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

count = 0
total_price_of_added_qty = 0
sweets_for_order = []




def add_to_cart_click(context,index, sweet_type, item_count):
    # intializing j
    j = 1
    # variable index carries location of the sweet item and while loop will run until the j==item_count
    while j <= item_count:
        price_xpath = f"(//div[@class='card-body']/child::p[2]/child::small){[index]}"
        price = driver.find_element(By.XPATH,price_xpath).text
        context.price = price.split("£")[1] #split the string and get only price to calculate

        add_to_cart_xpath = f"(//div[@class='card-body']/following-sibling::div/child::a){[index]}"
        driver.find_element(By.XPATH, add_to_cart_xpath).click()

        context.count += 1
        j += 1

    #     As there is diffrence in the text of sweets from main page and basket, assigning same value as it is there in main page
    if sweet_type == 'Bon Bons':
        sweet_type= "Strawberry Bon Bons"
    if sweet_type == "Sherbert Discs":
        sweet_type= "Sherbet Discs"

    sweets_for_order.append(sweet_type) #It will append all the added sweet to global list sweets_for_order

    context.price_on_qty = (float(context.price))*(int(item_count)) # to get each item price

    context.total_price_of_added_qty += context.price_on_qty  # to get overall price of basket
    # return context.count, context.total_price_of_added_qty


def add_to_cart(context):
    context.count = count
    context.total_price_of_added_qty = total_price_of_added_qty
    i = 1

    # get all the elements of sweet text
    total_items_sweet_text= driver.find_elements(By.XPATH,"//div[@class='card-body']/child::h4")

    # iterating over list of elements to get each element
    while i <= len(total_items_sweet_text):
        sweet_text_xpath = f"(//div[@class='card-body']/child::h4){[i]}"
        item_text = driver.find_element(By.XPATH,sweet_text_xpath).text

        # Based on the sweet name quantity will be assigned
        if item_text == "Bon Bons":
            quantity = 2

        if item_text == "Chocolate Cups":
            quantity = 3

        if item_text == "Sherbert Discs":
            quantity = 1

        if item_text == "Sherbert Straws":
            quantity = 4

        # Calling add_to_cart_click function
        add_to_cart_click(context,i,item_text, quantity)
        i += 1

def random_num_generator(from_size, to_size):
    return random.randint(from_size, to_size)




#-------------- Execution begins from here --------------------

# To launch the application on crome browser
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

# this line for waiting 20 second for each step
driver.implicitly_wait(20)

#launching the application
driver.get("https://sweetshop.netlify.app/")

#maximizing the window
driver.maximize_window()

# For explicit wait when objects will not load within fixed time
wait = WebDriverWait(driver,10)
add_cart_button = wait.until(EC.element_to_be_clickable(driver.find_element(By.XPATH,"(//a[@class='btn btn-success btn-block addItem']/parent::div/preceding-sibling::div/child::h4)[1]")))

# Invoke add_to_cart function to add required items to cart
add_to_cart(context)

basket = wait.until(EC.element_to_be_clickable(driver.find_element(By.XPATH,"//ul[@class='navbar-nav ml-auto']/descendant::a[4]")))
basket.click()
assert driver.title == "Sweet Shop"
total_item_in_the_basket = driver.find_element(By.XPATH,"//span[@class='badge badge-secondary badge-pill']").text

total_price = driver.find_element(By.XPATH,"//*[@id='basketItems']/li[5]/strong").text
total_price = total_price.split('£')[1] # to get total price of a basket


all_aded_items = driver.find_elements(By.XPATH,"//*[@id='basketItems']/descendant::h6")

#to check whether all the selected items are prsent in basket or not
for sweet in all_aded_items:
    assert sweet.text in sweets_for_order

# validating the initiated items against the total items in the basket
assert (int(context.count) == int(total_item_in_the_basket))

#validating price before adding and after adding to basket
assert (float(total_price) == float(context.total_price_of_added_qty))

#getting random numbers to pass to the input fields
random_num = random_num_generator(10000,10000000000)
zip = random_num_generator(100000,999999)
cc_num = random_num_generator(100000000000,999999999999)
cc_exp = random_num_generator(100000000000,999999999999)
cvv =  random_num_generator(100,999)
email_id = f'test.{str(random_num)}@gmail.com' #generating unique email id

#filling firstname, lastname, emailid, adress
driver.find_element(By.XPATH,"//label[contains(text(),'First name')]/following-sibling::input").send_keys("testfname")
driver.find_element(By.XPATH,"//label[contains(text(),'Last name')]/following-sibling::input").send_keys("testlname")

driver.find_element(By.XPATH,"//label[contains(text(),'Email')]/following-sibling::input").send_keys(email_id)
driver.find_element(By.XPATH,"//label[contains(text(),'Address')]/following-sibling::input").send_keys("test address 12345")

# Selecting country from dropdown
country_drp = driver.find_element(By.XPATH,"//*[@id='country']")
all_elemet = Select(country_drp)
all_elemet.select_by_index(1)

# Selecting city from dropdown
city_drp = driver.find_element(By.XPATH,"//*[@id='city']")
all_element = Select(city_drp)
all_element.select_by_index(1)

# Entering credit card details and cvv and zip and expiration
driver.find_element(By.XPATH,"//*[@id='zip']").send_keys(zip)
driver.find_element(By.XPATH,"//*[@id='cc-name']").send_keys("testfname")
driver.find_element(By.XPATH,"//*[@id='cc-number']").send_keys(cc_num)
driver.find_element(By.XPATH,"//*[@id='cc-expiration']").send_keys("202512")
driver.find_element(By.XPATH,"//*[@id='cc-cvv']").send_keys(cvv)


# Selecting the standard shipping if it is already not selected
status = driver.find_element(By.XPATH,"//label[contains(text(),'Standard Shipping')]").is_selected()
if status ==  False:
    driver.find_element(By.XPATH,"//label[contains(text(),'Standard Shipping')]").click()

# Clicking on checkout button
driver.find_element(By.XPATH,"//button[normalize-space()='Continue to checkout']").click()
print("executed_successfully")
