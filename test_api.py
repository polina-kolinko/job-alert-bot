import requests

def get_vacancies(query):
    url = "http://opendata.trudvsem.ru/api/v1/vacancies"
    params = {
        "text": query,
        "limit": 5
    }
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
    except requests.RequestException:
        return None
    
    data = response.json()
    return data["results"].get("vacancies", [])
def format_vacancy(elem):
    return f"{elem['job-name']}\n {elem['company']['name']}\n {elem['region']['name']}\n {elem['salary']}\n {elem['vac_url']}"

query = input("Что искать: ")
vac = get_vacancies(query)
if vac is None:
    print("не удалось получить вакансии")
elif not vac:
    print("По вашему запросу вакансий не найдено")
else:
    for item in vac:
        elem = item['vacancy']
        print(format_vacancy(elem))
        print("-----------------------")