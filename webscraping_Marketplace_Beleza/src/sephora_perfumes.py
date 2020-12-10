from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime
from time import sleep
import logging

logging.basicConfig(level=logging.INFO)

count=1
tent=0
while tent < 3:
    try:
        driver = webdriver.Chrome("C:/Users/daniel.melo/projetos/studies/webscraping/src/chromedriver.exe")
        driver.get("https://www.sephora.com.br/perfumes/feminino")
        logging.info(f"Página '{driver.current_url}' acessada.")
        sleep(10)

        while count <=10:
            button_more_products = (driver.find_element_by_xpath('//*[@id="see_more_products"]'))
            button_more_products.click()
            sleep(5)
            logging.info(f'Mais produtos, página {count + 1}')
            count = count + 1
        break
    except:
        driver.close()
        tent += 1
        if tent == 3:
            logging.error('As páginas não foram carregadas corretamente')
        continue

content = driver.page_source
soup = bs(content, 'html.parser')

day = datetime.datetime.now().strftime('%x')
hour = datetime.datetime.now().strftime('%X')
date = datetime.datetime.now()

items = soup.find_all('li', class_ = 'item')

sku = []
descricao = []
gross_price = []
price = []
pgto = [] 

items_mapping = 0    
for i in items:

    count_out_of_stock = 0
    if i['class'] == ['item', 'out-of-stock']:
        count_out_of_stock += count_out_of_stock
        continue
        
    
    sku.append(
        i['data-productid'])
        
    descricao.append(
        i.find('a', class_ = "product-image")['title'])

    try:
        gross_price.append(i['data-product-price'])
    except:
        gross_price.append('')
    pass

    try:
        price.append(i['data-product-final-price'])
    except:
        price.append('')
    pass

    try:
        pgto.append(i.find('div', class_ = "installments").text)
    except:
        pgto.append('')
    pass

    items_mapping += 1

logging.info(f'Qtde de items mapeados: {items_mapping}')
logging.info(f'Qtde de out of stock: {count_out_of_stock}')

base = (pd.DataFrame({'sku':sku,
                      'descricao':descricao,
                      'gross_price':gross_price,
                      'price':price,
                      'pagamento': pgto,
                      'date':date,
                      'day':day,
                      'hour':hour})
        )

local_save = '../data/sephora.csv'
with open(local_save, 'a',  newline='') as f:
    base.to_csv(f, header=f.tell()==0, index=False, decimal='.', encoding='latin-1')
    logging.info(f'Salvo com susesso em {local_save}')
driver.close()
#Há algns casos em que o frete tem *