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
    except requests.RequestException as e:
        print(type(e).__name__, e)
        return None
    
    data = response.json()
    return data["results"].get("vacancies", [])
def format_vacancy(elem):
    return f"{elem['job-name']}\n {elem['company']['name']}\n {elem['region']['name']}\n {elem['salary']}\n {elem['vac_url']}"

