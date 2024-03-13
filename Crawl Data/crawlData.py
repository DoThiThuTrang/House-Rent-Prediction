from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as ChromeOptions
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import numpy as np
from tqdm import tqdm
import time


def try_to_add_feature_data(new_product, feature, we_src, selector_find, value_if_success=None, value_if_fail=np.nan):
    try:
        element = we_src.find_element(By.CSS_SELECTOR, selector_find)

        if not value_if_success:
            new_product[feature] = element.text
        else:
            new_product[feature] = value_if_success
    except NoSuchElementException:
        new_product[feature] = value_if_fail


df = pd.DataFrame(
    columns=['post_id', 'post_title', 'post_verified', 'post_type', 'upload_date', 'building_type', 'squares', 'nums_bedroom', 'nums_wc', 'nums_floor', 'path_size', 'front_size', 'building_direction', 'window_direction', 'furniture', 'legal', 'others', 'location', 'owner_id', 'owner_name', 'nums_img', 'price'])

# df = pd.read_excel('crawler_house_full.xlsx')

file_link = 'link_building.xlsx'
link_df = pd.read_excel(file_link)
file_out = 'crawler_building_full.xlsx'
file_error_out = 'crawler_building_error.xlsx'

building_type = 'Căn hộ chung cư'

options = ChromeOptions()

options.add_experimental_option(
    'excludeSwitches', ['enable-logging', 'enable-automation'])
options.add_experimental_option("useAutomationExtension", False)

max_temp_post = link_df['link'].shape[0]
temp_count = 0
error = {'link': []}

last_pause = 0
for link in tqdm(link_df['link'], desc="Had crawled complete"):
    new_building = {}
    if temp_count == max_temp_post:
        break
    temp_count += 1

    if temp_count < last_pause:
        continue

    try:
        driver = webdriver.Chrome(options=options)

        driver.get(link)
        # time.sleep(1)
        wait = WebDriverWait(driver, 2)

        content_locator = driver.find_element(
            By.CSS_SELECTOR, "div.re__main div")

        content = content_locator.find_element(
            By.CSS_SELECTOR, "div.re__main-content div")
        sidebar = content_locator.find_element(
            By.CSS_SELECTOR, "div.re__main-sidebar")

        content_details = content.find_element(
            By.CSS_SELECTOR, "div[class^='re__pr-info']")

        building_special = content_details.find_elements(
            By.CSS_SELECTOR, "div[class$='js__li-specs'] div div div[class$='item']")

        try_to_add_feature_data(new_building, 'post_verified',
                                content_details, 'div.re__pr-stick-listing-verified', value_if_success=1, value_if_fail=0)

        new_building['post_type'] = content.get_attribute('class').split()[-1]

        new_building['nums_img'] = try_to_add_feature_data(
            new_building, 'nums_img', content, "div[class$='js__pr-media-slide'] div[class^='re__media-preview'] div[class^='swiper-pagination'] span:nth-of-type(2)", value_if_fail=1)

        new_building['post_id'] = content_details.get_attribute("prid")
        new_building['owner_id'] = content_details.get_attribute("uid")

        new_building['building_type'] = building_type

        new_building['owner_name'] = sidebar.find_element(
            By.CSS_SELECTOR, "div[class$='js__contact-box'] div[class$='js_contact-name']").get_attribute("title")

        new_building['post_title'] = content_details.find_element(
            By.CSS_SELECTOR, "h1[class$='title']").text

        new_building['location'] = content_details.find_element(
            By.CSS_SELECTOR, "span[class$='address']").text

        case_special = {'Diện tích': 'squares', 'Mức giá': 'price', 'Số phòng ngủ': 'nums_bedroom',
                        'Số toilet': 'nums_wc', 'Số tầng': 'nums_floor', 'Pháp lý': 'legal', 'Nội thất': 'furniture', 'Hướng nhà': 'building_direction', 'Hướng ban công': 'window_direction', 'Đường vào': 'path_size', 'Mặt tiền': 'front_size'}

        for special in building_special:
            title_special = special.find_element(
                By.CSS_SELECTOR, "span[class$='title']").text
            value_special = special.find_element(
                By.CSS_SELECTOR, "span[class$='value']").text

            if title_special in case_special:
                new_building[case_special[title_special]] = value_special
            else:
                new_building['others'] = new_building.get(
                    'others', "") + title_special + ":" + value_special + ";"

        new_building['upload_date'] = content_details.find_element(
            By.CSS_SELECTOR, "div[class$='js__pr-config'] div:nth-of-type(1) span.value").text

        new_building = pd.DataFrame(new_building, index=[0])
        df = pd.concat([df, new_building], ignore_index=True)

        df.to_excel(file_out, index=False)
    except:
        error['link'].append(link)
        df_er = pd.DataFrame(error)
        df_er.to_excel(file_error_out, index=False)

    driver.close()

df.to_excel(file_out, index=False)

# for page_number in range(1, 11):
#     driver = webdriver.Edge(options=options)
#     page_url = root_url + f"/p{page_number}"
#     driver.get(page_url)
#     # driver.implicitly_wait(10)

#     # Wait 3.5 on the webpage before trying anything
#     time.sleep(3.5)

#     # Wait for 3 seconds until finding the element
#     wait = WebDriverWait(driver, 3)

#     product_list = driver.find_elements(
#         By.CSS_SELECTOR, "div.re__main div div.re__main-content div[id='product-lists-web'] div[class^='js__card']")

#     for product in product_list:
#         new_product = {}
#         product_info = product.find_element(
#             By.CSS_SELECTOR, "a div.re__card-info")

#         product_detail_infos = product_info.find_element(
#             By.CSS_SELECTOR, "div.re__card-info-content div:nth-of-type(1)")
#         product_contact = product_info.find_element(
#             By.CSS_SELECTOR, "div.re__card-contact")

#         product_config = product_detail_infos.find_element(
#             By.CSS_SELECTOR, "div:nth-of-type(1)")
#         product_location = product_detail_infos.find_element(
#             By.CSS_SELECTOR, "div:nth-of-type(2)")

#         product_user_contact = product_contact.find_element(
#             By.CSS_SELECTOR, "div.re__card-published-info div")

#         # product_phone_contact = product_contact.find_element(
#         #     By.CSS_SELECTOR, "div.re__card-contact-button span:nth-of-type(1)")

#         new_product['id'] = product.get_attribute('prid')
#         new_product['owner_id'] = product.get_attribute('uid')
#         new_product['post_type'] = product.get_attribute('vtp')
#         new_product['post_verified'] = 0 if product.get_attribute(
#             'tracking-label').find('verified=0') != -1 else 1
#         new_product['nums_img'] = product.find_element(
#             By.CSS_SELECTOR, "a div.re__card-image div.re__card-image-feature span").text

#         new_product['title'] = product_info.get_attribute('title')

#         new_product['type'] = typeProduct

#         new_product['price'] = product_config.find_element(
#             By.CSS_SELECTOR, "span:nth-of-type(1)").text.replace('/tháng', '')

#         add_feature_data(new_product, 'squares',
#                          product_config, "span:nth-of-type(3)")
#         add_feature_data(new_product, 'nums_bedroom',
#                          product_config, "span[class^='re__card-config-bedroom'] span")
#         add_feature_data(new_product, 'nums_wc',
#                          product_config, "span[class^='re__card-config-toilet'] span")
#         if new_product['post_type'] == 'vip-diamond':
#             add_feature_data(new_product, 'district',
#                              product_location, "span:nth-of-type(2)")
#         else:
#             add_feature_data(new_product, 'district',
#                              product_location, "span")
#         add_feature_data(new_product, 'owner_name',
#                          product_user_contact, "div:nth-of-type(2)")

#         if new_product['post_type'] != 'vip-silver' and new_product['post_type'] != 'vip-normal':
#             new_product['upload_date'] = product_user_contact.find_element(
#                 By.CSS_SELECTOR, "div:nth-of-type(3) span").get_attribute("aria-label")
#         else:
#             new_product['upload_date'] = product_user_contact.find_element(
#                 By.CSS_SELECTOR, "div.re__card-published-info-published-at span.re__card-published-info-published-at").get_attribute("aria-label")

#         # product_phone_contact.click()
#         # WebDriverWait(product_phone_contact, 20).until(
#         #     EC.element_attribute_to_include(By.CSS_SELECTOR, "mobile"))
#         # print(product_phone_contact.get_attribute('mobile'))

#         df2 = pd.DataFrame(new_product, index=[0])
#         df = pd.concat([df, df2], ignore_index=True)

#     driver.close()
