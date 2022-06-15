import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from threading import Lock


lock = Lock()

city_names_list = []    # List of name all the cities you want to get ids of. eg : ['Ahmedabad', 'Bangalore', 'Chennai', 'Delhi']


class getCityIds:
    def __init__(self, city_list):
        self.session = requests.Session()
        self.city_list = city_list
        self.city_name_id_dict = {}
        self.main()


    def get_city_id(self, city):
        url = f'https://www.realestateindia.com/search.php?searchlistfor=2&allcategory=17&cityname={city}'  #Change accordingly (but not required maybe)
        resp = self.session.get(url)
        soup = BeautifulSoup(resp.content, 'html5lib')
        city_id = int(soup.find('input', {'name':'allcity'}).attrs['value'])
        lock.acquire()
        self.city_name_id_dict[city] = city_id
        lock.release()


    def main(self):
        with ThreadPoolExecutor(max_workers=500) as executor:
            executor.map(self.get_city_id, self.city_list)
        
        return self.city_name_id_dict


city_dict = getCityIds(city_names_list)
