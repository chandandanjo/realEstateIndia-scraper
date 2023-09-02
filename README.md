# RealEstateIndia Property Scraper

This Python script is designed to scrape property records, including contact details, from [RealEstateIndia](https://www.realestateindia.com/). It saves the data in an xlsx format for easy access and analysis.

## Important Notes
Before running the script, please ensure the following:

1. Fill in your user details in the `contact_details` function of `realEstateIndia.py` to enable the contact information retrieval feature.

2. If you don't want to save HTML files for each property, you can remove that functionality from the `create_files` and `single_page` functions in `realEstateIndia.py`.

## Usage

#### Customization
- The script is set up to scrape only *commercial properties for lease*. You can tailor it to your specific needs by modifying the URLs and payloads. Look for the comments `#Change accordingly` in the code for guidance.

#### City IDs
- City IDs are necessary to scrape all the details. To obtain city IDs, you can use the separate script provided, which takes a list of cities and returns a dictionary containing city names and city IDs as key-value pairs. You can then pass this dictionary to the main `realEstateIndia` class when instantiating it to get the desired output.

#### Output Format
- The script saves data in xlsx format instead of CSV to avoid issues with phone numbers when viewing in MS Excel.

#### Performance
- The script's performance can be slow (e.g., scraping 300 properties in approximately 7 minutes) because it doesn't incorporate multithreading or multiprocessing. However, you can implement these features to improve speed.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- This script was created for educational purposes and should be used responsibly and in accordance with RealEstateIndia's terms of service.
- Special thanks to the BeautifulSoup and Requests libraries for making web scraping easier.
- Feel free to modify and customize the script to suit your specific web scraping requirements.
