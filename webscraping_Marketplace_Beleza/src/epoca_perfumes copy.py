from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import datetime
from time import sleep
import logging

logging.basicConfig(level=logging.INFO)

driver = webdriver.Chrome("C:/Users/daniel.melo/projetos/studies/webscraping/src/chromedriver.exe")
driver.get("https://www.epocacosmeticos.com.br/perfumes/perfume-feminino")
logging.info(f'Página {driver.current_url} acessada.')

content = driver.page_source
soup = bs(content, 'html.parser')

day = datetime.datetime.now().strftime('%x')
hour = datetime.datetime.now().strftime('%X')
date = datetime.datetime.now()

categoria = []
sku = []
descricao = []
gross_price = []
price = []
pgto = []

items_mapping = 0
count = 0
while count < 10:
    
    sleep(10)
    items = soup.find_all('li', class_ = 'perfumes-importados-em-promocao-|-frete-gratis-|-epoca-cosmeticos')
    pagerbottom = soup.find_all('div', class_ = "pager bottom")[0]['id']
    button_more_products = driver.find_element_by_xpath(f"//*[@id='{pagerbottom}']/ul/li[8]")
   
    for i in items: 
 
        categoria.append(i.find('div', class_ = "shelf-default__item")['data-category'])

        sku.append(i.find('div', class_ = "shelf-default__item")['data-id'])

        descricao.append(i.find('div', class_ = "shelf-default__item")['title'])

        try:
            price.append(i.find('div', class_ = "shelf-default__item")['data-price'].replace('R$','').replace('.','').strip())
        except:
            price.append('')
        pass

        try:
            gross_price.append(i.find('span', class_ = "listprice").text.replace('R$','').replace('.','').strip())
        except:
            gross_price.append('')
        pass

        try:
            pgto.append(i.find('span', class_ = "shelf-default__number-installment").text.replace('\n','').strip())
        except:
            pgto.append('')
        pass

        items_mapping += 1
    
    button_more_products.click()
    logging.info(f'Mais produtos, página {count + 1}')
    count += 1
    
logging.info(f'Qtde de items mapeados: {items_mapping}')


base = (pd.DataFrame({'sku':sku,
                      'descricao':descricao,
                      'gross_price':gross_price,
                      'price':price,
                      'pagamento': pgto,
                      'date':date,
                      'day':day,
                      'hour':hour})
        )

local_save = '../teste/epoca.csv'
with open(local_save, 'a',  newline='') as f:
    base.to_csv(f, header=f.tell()==0, index=False, decimal=',', encoding='latin-1')
    logging.info(f'Salvo com susesso em {local_save}')
driver.close()