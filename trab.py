import csv
with open('Colonia.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
cities = []
for row in reader:
    city = row['Cidade']
    x,y = map(int, row['X:Y'].split(';'))
    cities.append(city,x,y)
print(cities)


