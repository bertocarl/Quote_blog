import urllib.request,json
from .models import Quotes



# Getting api key
api_key = None
# Getting the quotes base url
base_url = None

def configure_request(app):
    global api_key,base_url
    api_key = app.config['QUOTES_API_KEY']
    base_url = app.config['QUOTES_API_BASE_URL']


def get_quotes(country,category,):
    get_quotes_url = base_url.format(country,category,api_key)
    print(get_quotes_url)
    with urllib.request.urlopen(get_quotes_url) as url:
        get_quotes_data = url.read()
        get_quotes_response = json.loads(get_quotes_data)
        print(get_quotes_response)
        quotes_results = None
        if get_quotes_response['quote']:
            quotes_results_list = get_quotes_response['quote']
            quotes_results = process_results(quotes_results_list)
    return quotes_results

def process_results(quotes_list):
    quotes_results = []
    for quotes_item in quotes_list:
        source = quotes_item.get('source')
        author = news_item.get('author')
        id = news_item.get('id')
        quotes = quotes_item.get('quotes')
        permalink = quotes_item.get('permalink')
        

       
    return quotes_results