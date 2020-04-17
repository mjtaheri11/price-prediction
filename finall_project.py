from bs4 import BeautifulSoup
import requests
import re
import mysql.connector
from selenium import webdriver
from time import sleep

""" in this code I just scrap data from ihome.ir and insert them into special database. this could be expand for more
 than 30 pages and use lambda function to stay until page completely loaded but this option is ignored"""

cnx = mysql.connector.connect(
    host='127.0.0.1',
    user="root",
    passwd="1375Javad", database='learn'
)

a = []
b = []
c = []
d = []
i = 0
driver = webdriver.Firefox()
driver.get('https://ihome.ir/sell-residential-apartment/th-tehran')
mycursor = cnx.cursor()
query1 = ("CREATE TABLE user(Area int(4), year int(2), bedroom int(4), neighbour varchar(30), price float(5, 2))")
mycursor.execute(query1)

while i < 30:
    button = driver.find_element_by_xpath("/html/body/div/div/div/div[1]/div[3]/div[2]/div[4]/div/ul/li[8]/a")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    val = soup.find_all('span', attrs={'class': 'title'})
    val2 = soup.find_all('span', attrs={'class': 'property-detail__icons-item__value'})
    val3 = soup.find_all('div', attrs={'class': 'sell-value'})

    for j in val:
        res1 = re.sub('\s+', ' ', j.text)
        x1 = re.findall(r'\b(\w+)\W*$', res1)
        a.append(x1[0])

    for j in val2:
        res2 = re.sub('\s+', ' ', j.text)
        b.append(res2)

    for j in val3:
        res3 = re.sub('\s+', ' ', j.text).strip()
        if re.findall(r'^\d+', res3):
            x21 = re.findall(r'میلیارد و (\d+) میلیون تومان', res3)
            x22 = re.findall(r'(\d+)', res3)
            if re.findall(r'\میلیارد', res3):
                if x21 != [] and x22 != []:
                    x2 = int(x22[0]) + int(x21[0]) / 1000
                    d.append(x2)
                else:
                    x2 = x22[0]
                    d.append(x2)
            else:
                print(x22, x22[0])
                x2 = int(x22[0]) / 1000
                d.append(x2)
    driver.execute_script("arguments[0].click();", button)
    driver.implicitly_wait(1000)
    sleep(30)
    i += 1

for i in range(len(a)):
    if b[3 * i + 1] != r' نوساز ':
        c.append([int(b[3 * i]), int(b[3 * i + 1]), int(b[3 * i + 2]), a[i], d[i]])
    else:
        c.append([int(b[3 * i]), 0, int(b[3 * i + 2]), a[i], d[i]])

query = "INSERT INTO user (Area, year, bedroom, neighbour, price) VALUES (%s, %s, %s, %s, %s)"
for i in range(0, len(c)):
    val = (c[i][0], c[i][1], c[i][2], c[i][3], c[i][4])
    mycursor.execute(query, val)

cnx.commit()
cnx.close()
