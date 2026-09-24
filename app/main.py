from app.trudvsem_api import get_vacancies, format_vacancy
def main():
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
if __name__ == "__main__":
    main()