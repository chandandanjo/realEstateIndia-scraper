import requests
from bs4 import BeautifulSoup
from datetime import datetime
import xlsxwriter
import os


city_dict = {} # Dictionary containing key(city name) and value(city id) pairs. eg : city_dict = {'Miraj Kupwad': 9145, 'Gulbarga': 1368, 'Howrah': 5956}


class realEstateIndia:
    def __init__(self, city_name, city_id):
        self.city_name = city_name
        self.city_id = city_id
        self.session = requests.Session()
        self.properties_url_list = []
        self.add_properties_url_list = []
        self.main_url = f'https://www.realestateindia.com/search.php?searchlistfor=2&allcategory=17&cityname={city_name}&cityname_hidden={city_id}' #Change accordingly

    def create_files(self):
        self.directory = f'./content/cities_htmls/{self.city_name}_HTMLS'
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        
        if not os.path.exists('./content/cities_xls'):
            os.makedirs('./content/cities_xls')
        self.workbook = xlsxwriter.Workbook(f'./content/cities_xls/{self.city_name}.xlsx')
        self.worksheet = self.workbook.add_worksheet()
        header = ['city', 'address', 'location', 'seller', 'seller company', 'seller type', 'phone number', 'posted on', 'built up area', 'carpet area', 'property type', 'summary', 'url', 'timestamp']
        column = 0
        for item in header:
            self.worksheet.write(0, column, item)
            column+=1
        

    def total_prop_count(self):
        resp = requests.get(self.main_url)
        soup = BeautifulSoup(resp.content, 'html5lib')
        self.total_properties = 0
        try:
            self.total_properties = int(soup.find('ul', {'class':'psc-cat mb20px'}).find('li', {'class':'on'}).find('a').find('b').get_text().strip())
        except:
            pass


    def initial_properties(self):
        s = self.session
        url = self.main_url
        resp = s.get(url)
        soup = BeautifulSoup(resp.content, 'html5lib')
        self.properties = soup.find_all('div', class_='ps-list mb15px bdr bdrddd')
        add_properties = soup.find_all('div', class_='p10px bdrt bdrddd pr')
        for property in self.properties:
            url = property.find('h3').find('a')['href']
            self.properties_url_list.append(url)
        for j in add_properties:
            if j.find('a', class_='w100px tac blue u lh14em small'):
                self.add_properties_url_list.append(j.find('a', class_='w100px tac blue u lh14em small')['href'])
            else:
                related_properties = j.find('ul').find_all('li')
                for k in related_properties:
                    self.properties_url_list.append(k.find('a')['href'])


    def scraper(self):
        s = self.session
        self.initial_properties()
        url = "https://www.realestateindia.com/Functions/property_fetch_results.php"
        headers = {}
        headers["content-type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        headers["referer"] = self.main_url
        pageno = 1
        while True:
            #Change accordingly
            payload = {
                'pageno': pageno,
                'page_type': 'search_page',
                'propertyfor': 2,
                'sub_cat': 17,
                'city': self.city_id,
                'city_label': 2,
                'request_type': 'load_more',
            }
            resp = s.post(url, headers=headers, data=payload)
            if resp.status_code != 200:
                    continue
            else:
                soup = BeautifulSoup(resp.content, 'html5lib')
                properties = soup.find_all('div', class_='ps-list mb15px bdr bdrddd')
                add_properties = soup.find_all('div', class_='p10px bdrt bdrddd pr')
                if len(properties) == 0:
                    if resp.status_code != 200:
                        continue
                    else:
                        break
                else:
                    for i in properties:
                        self.properties_url_list.append(i.find('h3').find('a')['href'])

                    for j in add_properties:
                        if j.find('a', class_='w100px tac blue u lh14em small'):
                            self.add_properties_url_list.append(j.find('a', class_='w100px tac blue u lh14em small')['href'])
                        else:
                            related_properties = j.find('ul').find_all('li')
                            for k in related_properties:
                                self.properties_url_list.append(k.find('a')['href'])
                pageno += 1

    def add_scraper(self,):
        s = self.session
        for l in self.add_properties_url_list:
            member_id = l.split('/')[-2].split('-')[-1]

            #initial
            url = f"https://www.realestateindia.com/script-files/company-profile/property_fetch_results.php?action_id=filter_property&propertyfor=2&member_id={member_id}&sub_cat=17&prop_proj_type=property&cid={self.city_id}"    #Change accordingly
            headers = {}
            headers["referer"] = l
            resp = s.get(url, headers=headers)
            soup = BeautifulSoup(resp.content, 'html5lib')
            try:
                url_list = soup.find('ul', {'id':'prop_sale_rent_results'}).find_all('li')
                for m in url_list:
                    self.properties_url_list.append(m.find('div')['data-url'])
            except:
                pass

            #next pages
            if soup.find('a', {'title':'Load more'}):
                url = "https://www.realestateindia.com/script-files/company-profile/property_fetch_results.php"
                headers = {}
                headers["content-type"] = "application/x-www-form-urlencoded; charset=UTF-8"
                headers["referer"] = l

                page_ = 1

                while True:
                    #Change accordingly
                    payload = {
                        'pageno': page_,
                        'propertyfor': 2,
                        'member_id': member_id,
                    }
                    resp = s.post(url, headers=headers, data=payload)
                    soup = BeautifulSoup(resp.content, 'html5lib')
                    url_list_all= soup.find_all('li')
                    url_list = []

                    for x in url_list_all:
                        if 'Office Spaces for Rent' in x.find('p', class_='ttd-title').get_text():
                            url_list.append(x)

                    if len(url_list_all) < 1:
                        if resp.status_code != 200:
                            continue
                        else:
                            break
                    else:
                        for urls in url_list:
                            self.properties_url_list.append(urls.find('div')['data-url'])
                    page_ += 1


    def single_page(self, serial, url, via_saved_file = False):
        if via_saved_file == False:
            s = self.session

            resp = s.get(url)
            soup = BeautifulSoup(resp.content, 'html5lib')

            #Writing HTML files.
            with open(f'{self.directory}/{url[8:].replace(".", "").replace("/","_")}.html', 'w', encoding='utf-8') as s:
                s.write(soup.prettify())

        elif via_saved_file == True:
            file_ = open(self.directory+'/'+url)
            soup = BeautifulSoup(file_.read(), 'html5lib')

        location, built_up_area, carpet_area, property_type, phone_no, posted_on, seller_type = 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'
        a = soup.find('a', {'title':'Get Phone No.'})['onclick'].lstrip('Propertyclassified_EnqueryPopup').rstrip(';').split(',')
        mailto = int(a[1].strip().strip("'"))
        prop_id = int(a[2].strip().strip("'"))
        try:
            seller_type, seller, seller_company, phone_no = self.contact_details('https://' + url.rstrip('.html').replace('_','/'), mailto, prop_id)
        except:
            pass
        address = soup.find('h1', class_='pd-title').get_text()
        city = address.split()[-1].strip(',')
        try:
            posted_on = soup.find('div', class_='pdp-pd').find('span').get_text()
        except Exception as e:
            pass
        summary = soup.find('div', class_='pd-ap').find('p').get_text().replace('/n','').strip()
        other_details = soup.find('ul', class_='pdoi-list').find_all('li')
        for detail in other_details:
            key = detail.find('div').find('span').get_text()
            value = detail.find('div').get_text().lstrip(key)
            if 'Location' in key:
                location = value
            if 'Built Up Area' in key:
                built_up_area = value
            if 'Carpet Area' in key:
                carpet_area = value
            if 'Type' in key:
                property_type = value
            if built_up_area == 'NA':
                if 'Super Area' in key:
                    built_up_area = value
        timestamp_ = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        row_ = [city, address, location, seller, seller_company, seller_type, phone_no, posted_on, built_up_area, carpet_area, property_type, summary, url, timestamp_]

        row = serial + 1
        column = 0
        for item in row_:
            self.worksheet.write(row, column, item)
            column+=1


    def contact_details(self, url_, mailto, prop_id):
        s = self.session
        url = "https://www.realestateindia.com/view_enquiry_now.php?"

        headers = {}
        headers["content-type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        headers["referer"] = url_

        # Modify below data according to your own credentials. Mainly fname, user_name, mobile and sometimes loginusr, member_type also.
        data = {
            'country' : '+91',
            'loginusr' : 'new_user',
            'mailto' : {mailto},
            'prop_id' : {prop_id},
            'id' : 'send_prop_enq_contact',
            'action_type' : 'send_inquiry',
            'page_url' : {url_.replace(':','%3A').replace('/','%2F')},
            'fname' : 'YOUR USERNAME',
            'user_name' : 'YOUR EMAIL',
            'mobile' : 'YOUR PHONE NUMBER',
            'member_type' : 1
        }

        resp = s.post(url, headers=headers, data=data)
        soup = BeautifulSoup(resp.content, 'html5lib')
        dealer_info = soup.find('div', class_='delear-info')
        seller_type, seller, seller_company, contact_num = 'NA', 'NA', 'NA', 'NA'
        try:
            seller_type = dealer_info.find('p', class_='di-title').get_text().strip().split()[0]
        except Exception as e:
            pass
        try:
            seller = ''.join(c for c in str(dealer_info.find('p', class_='dname').get_text()) if ord(c) < 128)
        except Exception as e:
            pass
        try:
            seller_company = dealer_info.find('p', class_='dc-name').get_text()
        except Exception as e:
            pass
        try:
            contact_num = dealer_info.find('p', class_='dmn').get_text()
        except Exception as e:
            pass

        return seller_type, seller, seller_company, contact_num


    def scrape_from_html(self):
        url_files = [f for f in os.listdir(f'{self.directory}') if f.endswith('.html')]
        print(f'Total length of properties in {self.city_name} are : ', len(set(url_files)))
        for serial, url in enumerate(list(set(url_files))):
            self.single_page(serial, url, via_saved_file = True)
        self.workbook.close()


    def main(self):
        retries = 0
        self.total_prop_count()
        print(f'Actual properties in {self.city_name} are : ', self.total_properties)
        if self.total_properties != 0:
            self.create_files()        
            self.scraper()
            self.add_scraper()
            max_properties_url_list = set(self.properties_url_list)
            while self.total_properties > 10 + len(set(self.properties_url_list)) and retries < 5:
                print(f'Got only {len(set(self.properties_url_list))} properties retrying.........')
                retries += 1
                self.scraper()
                self.add_scraper()
                if len(set(self.properties_url_list)) > len(max_properties_url_list):
                    max_properties_url_list = set(self.properties_url_list)
                else:
                    self.properties_url_list = list(max_properties_url_list)
            print(f'Length of scraped properties in {self.city_name} are : ', len(set(self.properties_url_list)))
            for serial, url in enumerate(list(set(self.properties_url_list))):
                self.single_page(serial, url, via_saved_file = False)
            self.workbook.close()

for name, id in city_dict.items():
    obj = realEstateIndia(name, id)
    obj.main()
