from django.shortcuts import render
from utils.search_db import find_closest_match
from utils.amazon import get_first_google_result,scrape_amazon_product
from . import client
from utils.reading_invoice import process_invoice

def search_products(request):
    if request.method == 'POST':
        query = request.POST.get('query', '')
        first_url = get_first_google_result(query)
        features = scrape_amazon_product(first_url)
        rating = client.extract_rating(features)
        C = "Yes" if int(rating)>=3 else "No"
        return render(request, 'search/results.html', {'products': [[query,rating,C]], 'query': query})
    return render(request, 'search/search.html')

def upload_invoice(request):
    if request.method == 'POST':
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image uploaded'}, status=400)
        image_file = request.FILES['image']
        image_bytes = image_file.read()
        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        names = process_invoice(img)
        names = [f"{k} {v}" for k,v in names.items()]
        results = []
        for name in names:
            first_url = get_first_google_result(name)
            features = scrape_amazon_product(first_url)
            rating = client.extract_rating(features)
            C = "Yes" if int(rating)>=3 else "No"
            results.append([name, rating, C])
        return render(request, 'search/results.html', {'products': [[query,rating,C]], 'query': query})
    return render(request, 'search/search.html')
