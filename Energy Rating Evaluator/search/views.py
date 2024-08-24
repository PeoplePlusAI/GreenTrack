from django.shortcuts import render
from utils.search_db import find_closest_match
from utils.amazon import get_first_google_result, scrape_amazon_product
from . import client
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from utils.reading_invoice import process_invoice
from PIL import Image
import io

@require_http_methods(["POST", "GET"])
def search_products(request):
    if request.method == 'GET':
        return render(request, 'search/search.html')
    query = request.POST.get("query", "")
    first_url = get_first_google_result(query)
    features = scrape_amazon_product(first_url)
    rating = client.extract_rating(features)
    C = "Yes" if int(rating) >= 3 else "No"
    return render(
        request,
        "search/results.html",
        {"products": [[query, rating, C]], "query": query},
    )

@require_http_methods(["POST"])
def upload_invoice(request):
    if "image" not in request.FILES:
        return JsonResponse({"error": "No image uploaded"}, status=400)
    image_file = request.FILES["image"]
    image_bytes = image_file.read()
    pil_image = Image.open(io.BytesIO(image_bytes))
    names = process_invoice(pil_image)
    results = []
    for name in names:
        first_url = get_first_google_result(name)
        features = scrape_amazon_product(first_url)
        rating = client.extract_rating(features)
        C = "Yes" if int(rating) >= 3 else "No"
        results.append([name, rating, C])
    return render(
        request,
        "search/results.html",
        {"products": results},
    )
