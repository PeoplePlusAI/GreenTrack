from django.shortcuts import render
from googlesearch import search
from django.shortcuts import render
from utils.search_db import find_closest_match
from utils.amazon import most_relevant_amazon_product

def search_products(request):
    if request.method == 'POST':
        query = request.POST.get('query', '')
        print(most_relevant_amazon_product(query))
        M, R = find_closest_match(query,"./resources/csvs/DeepFreezersSample.csv",1)
        C = ["Yes" if int(v)>=3 else "No" for v in R]
        return render(request, 'search/results.html', {'products': list(zip(M,R,C)), 'query': query})
    return render(request, 'search/search.html')
