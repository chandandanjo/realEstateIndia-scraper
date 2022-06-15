# realEstateIndia-scraper
Fetch property records along with contact details from https://www.realestateindia.com/ in xlsx format.

### NOTE : PLEASE FILL THE USER DETAILS IN contact_details FUNCTION OF realEstateIndia.py BEFORE EXECUTION.
### NOTE : IF YOU DON'T WANT TO SAVE THE HTML FILES OF EACH PROPERTY THEN REMOVE IT FROM create_files & single_page FUNCTIONS IN realEstateIndia.py BEFORE EXECUTION.

#### SOME IMPORTANT POINTS :
  - I have written this script to scrape only *commercial properties for lease*. You can modify the URLs and Payloads according to your specific needs.
      - I've commented **#Change accordingly** wherever changes are required for tailoring your own custom request.
  - City ids are necessary to scrape all the details, so for that I've written a separate script which takes list of cities and returns a dictionary containing city name and city id as key:value pairs respectively. This can then be passed to the main realEstateIndia class while instantiating it to get the output.
  - Previously I tried using csv instead of xlsx but there was an issue with phone-number while viewing on MS EXCEL.
  - It's really slow (300 properties in ~7 minutes) as I haven't incorporated multithreading/multiprocessing. BUT YOU CAN.
