from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import datetime
from time import sleep
import logging

logging.basicConfig(level=logging.INFO)

driver = webdriver.Chrome("C:/Users/daniel.melo/projetos/studies/webscraping/src/chromedriver.exe")
driver.get("https://www.belezanaweb.com.br/perfumes/feminino/")
logging.info(f"Página '{driver.current_url}' acessada.")

count=1
while count <=10:
    button_more_products = (driver.find_element_by_xpath('/html/body/main/div/section/div/div/button'))
    button_more_products.click()
    sleep(5)
    logging.info(f'Mais produtos, página {count + 1}')
    count = count + 1

content = driver.page_source
soup = bs(content, 'html.parser')

day = datetime.datetime.now().strftime('%x')
hour = datetime.datetime.now().strftime('%X')
date = datetime.datetime.now()

items = soup.select('div.showcase-item.js-event-product-click')

dpto = []
categoria = []
sku = []
descricao = []
gross_price = []
price = []
pgto = []
frete = []
    
items_mapping = 0
for i in items:

    dpto.append(
        json.loads(i['data-event'])['templateDepartmentSlugName'])

    categoria.append(
        json.loads(i['data-event'])['templateCategorySlugName'])

    sku.append(
        json.loads(i['data-event'])['sku'])

    descricao.append(
        i.find('a', class_ = "showcase-item-image")['title'][:50])
    
    try:
        gross_price.append(i.find('div', class_ = "item-price-max").text.replace('R$','').replace('.','').strip())
    except:
        gross_price.append('')
    pass
    
    price.append(
        i.find('div', class_ = "item-price-value").text.replace('\n','').replace('Frete Grátis','').replace('R$','').replace('*','').replace('.',''))
    
    try:
        pgto.append(
            " ".join(i.find('div', class_ ="item-price-installments").text.split()))
    except:
        pgto.append('')
    pass

    frete.append('Frete Grátis' in i.find('div', class_ = "item-price-value").text.replace('\n','').replace('R$',''))

    items_mapping += 1

logging.info(f'Qtde de items mapeados: {items_mapping}')

base = (pd.DataFrame({'dpto':dpto,
                      'categoria':categoria,
                      'sku':sku,
                      'descricao':descricao,
                      'gross_price':gross_price,
                      'price':price,
                      'pagamento': pgto,
                      'frete':frete,
                      'date':date,
                      'day':day,
                      'hour':hour})
        )

local_save = '../data/beleza_na_web.csv'

with open(local_save, 'a', newline='') as f:
    base.to_csv(f, header=f.tell()==0, index=False, decimal=',', encoding='latin-1')
    logging.info(f'Salvo com susesso em {local_save}')

driver.close()
#Há algns casos em que o frete tem *