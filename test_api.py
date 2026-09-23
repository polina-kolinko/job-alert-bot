import requests
url = "http://opendata.trudvsem.ru/api/v1/vacancies"
query = input("Что искать: ")
params = {
    "text": query,
    "limit": 5
}
response = requests.get(url, params=params)
data = response.json()

print(data['meta'])
#print(type(data['results']))
#print(data["results"].keys())
#print(type(data["results"]["vacancies"]))
#print(len(data["results"]["vacancies"]))
#print(data["results"]["vacancies"][0])
vac = data["results"]["vacancies"]
for item in vac:
    elem = item['vacancy']
    print(elem['job-name'])
    print(elem['company']['name'])
    print(elem['region']['name'])
    print(elem['salary'])
    print(elem['vac_url'])
    print("-----------------------")