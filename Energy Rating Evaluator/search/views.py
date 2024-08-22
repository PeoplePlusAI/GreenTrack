from django.shortcuts import render
from utils.search_db import find_closest_match
from utils.amazon import get_first_google_result,scrape_amazon_product
from . import client

def search_products(request):
    if request.method == 'POST':
        query = request.POST.get('query', '')
        first_url = get_first_google_result(query)
        features = scrape_amazon_product(first_url)
        rating = client.extract_rating(features)
        C = "Yes" if int(rating)>=3 else "No"
        return render(request, 'search/results.html', {'products': [[query,rating,C]], 'query': query})
    return render(request, 'search/search.html')
