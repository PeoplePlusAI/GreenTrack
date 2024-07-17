from django.shortcuts import render
from googlesearch import search
from django.shortcuts import render
from utils.search_db import find_closest_match

def search_products(request):
    if request.method == 'POST':
        query = request.POST.get('query', '')
        M, R = find_closest_match(query,"./resources/csvs/full-db.csv",5)
        C = ["Yes" if int(v)>=3 else "No" for v in R]
        return render(request, 'search/results.html', {'products': list(zip(M,R,C)), 'query': query})
    return render(request, 'search/search.html')
