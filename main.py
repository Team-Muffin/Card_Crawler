from selenium import webdriver
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import time

card_data_lst = []
card_data_lst.append(['CARD_NM', 'CARD_IMG', 'SMY_NOTI', 'SMY_ANNUAL_FEE', 'SMY_REWARDS', 'SMY_BASE_RECORD', 'SMY_BENEFIT1', 'SMY_BENEFIT2', 'TAGS', 'BENEFITS', 'TERMS'])

driver = webdriver.Chrome()

BASE_URL = 'https://card-search.naver.com'
LIST_URL = BASE_URL + '/list?sortMethod=qc'

driver.get(LIST_URL)
driver.implicitly_wait(3)

def parse_items():
    bs_obj = BeautifulSoup(driver.page_source, 'html.parser')

    table = bs_obj.select_one('ul.list')
    items = table.select('li.item')[-10:] # 하위 10개

    return items

total_parsed = 0
while total_parsed < 100:
    items = parse_items()

    for idx, item in enumerate(items):
        if total_parsed >= 100:
            break

        link = BASE_URL + item.find('a')['href']
        
        # 각 상품의 상세 페이지 파싱
        driver.get(link)
        bs_obj = BeautifulSoup(driver.page_source, 'html.parser')
        
        ## 기본 정보
        CARD_NM = bs_obj.select_one('div.cardname').text
        CARD_IMG = bs_obj.select_one('img.img')['src']

        ## 요약 정보
        CARD_INFO = bs_obj.select_one('div.cardinfo')
        try:    SMY_NOTI = CARD_INFO.select_one('b.noti').text
        except: SMY_NOTI = None
        SMY_ANNUAL_FEE = CARD_INFO.select_one('dd.desc.as_annualFee > span.txt').text
        try:    SMY_REWARDS = CARD_INFO.select_one('dd.desc.as_annualFee > b.rewards').text
        except: SMY_REWARDS = None
        SMY_BASE_RECORD = CARD_INFO.select_one('dd.desc.as_baseRecord > span').text
        try:
            dl_list = bs_obj.select_one('dl.list')
            last_dd = dl_list.find_all('dd')[-1]
            SMY_BENEFIT1 = last_dd.select_one('span:nth-of-type(1)').text
            SMY_BENEFIT2 = last_dd.select_one('span:nth-of-type(2)').text
        except: 
            SMY_BENEFIT1 = None
            SMY_BENEFIT2 = None

        ## 주요 혜택_태그
        TAGS = []
        benefit_tags = bs_obj.select('button.benefit')
        for benefit_tag in benefit_tags:
            tag = benefit_tag.select_one('span.name').text
            if tag:
                TAGS.append(tag)

        ## 상세 혜택
        BENEFITS = bs_obj.select_one('div.Benefits').text

        ## 카드 정보
        TERMS = []
        card_terms = bs_obj.select('div.cardItem > div.card_terms')
        for card_term in card_terms:
            term = card_term.select_one('div.inner').text
            if term:
                TERMS.append(term)

        card_data_lst.append([CARD_NM, CARD_IMG, SMY_NOTI, SMY_ANNUAL_FEE, SMY_REWARDS, SMY_BASE_RECORD, SMY_BENEFIT1, SMY_BENEFIT2, TAGS, BENEFITS, TERMS])
        total_parsed += 1

        # csv 저장
        with open('./card2.csv', 'w', encoding='utf-8', newline='') as f:
            csvWriter = csv.writer(f)
            for card_data in card_data_lst:
                csvWriter.writerow(card_data)

        driver.back()
        time.sleep(1)
        
    # '더보기' 버튼 클릭
    try:
        more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.more'))
        )
        more_button.click()
        time.sleep(3)
    except Exception as e:
        print('더보기 버튼 클릭 불가: ', e)
        break

driver.quit()