import mysql.connector
from sklearn.linear_model import LinearRegression

"""in this code we use linear regression to predict the price of houses which placed in tehran. The neighbour is labeled
by sum(ord()) function"""

cnx = mysql.connector.connect(
    host='127.0.0.1',
    user="root",
    passwd="1375Javad", database='learn'
)

x = []
y = []
cursor = cnx.cursor(buffered=True)
sql_select_query = """select * from user"""
cursor.execute(sql_select_query)
record = cursor.fetchall()

for row in record:
    z = [ord(x) for x in row[3]]
    s = sum(z)
    x.append([row[0], row[1], row[2], s])
    y.append(row[4])

regressor = LinearRegression()
regressor.fit(x, y)
# w = [[500, 0, 3, 12893]]
while True:
    try:
        a = int(input('input Area: '))
        b = int(input('input year: '))
        c = int(input('bedrooms: '))
        d = input('neighbuor(like ولنجک): ')
        d = sum([ord(x) for x in d])
        break
    except ValueError:
        print('please reenter the data')

answer = [[a, b, c, d]]
y_pred = regressor.predict(answer)
print('{} miliard toman'.format(y_pred))
cnx.close()
