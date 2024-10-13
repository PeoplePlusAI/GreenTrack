from django.shortcuts import render
from utils.amazon import scrape_amazon_product, get_top_non_sponsored_products
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from utils.reading_invoice import process_invoice
from utils.agent import call_agent
from PIL import Image
import io

@require_http_methods(["POST", "GET"])
def search_products(request):
    if request.method == 'GET':
        return render(request, 'search/search.html')
    query = request.POST.get("query", "")
    first_url = get_top_non_sponsored_products(query)[0]
    prod_name, features = scrape_amazon_product(first_url)
    features.append('Name:' + prod_name)
    rating = call_agent(''.join(features), prompt_file=f"star_rating.txt")
    C = "Yes" if int(rating) >= 3 else "No"
    return render(
        request,
        "search/results.html",
        {"products": [[prod_name, rating, C]], "query": query},
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
        name = call_agent(name, prompt_file=f"product_name.txt")
        first_url = get_top_non_sponsored_products(name)[0]
        prod_name, features = scrape_amazon_product(first_url)
        features.append('Name:' + prod_name)
        rating = call_agent('\n'.join(features), prompt_file="star_rating.txt")
        C = "Yes" if int(rating) >= 3 else "No"
        results.append([prod_name, rating, C])
    return render(
        request,
        "search/results.html",
        {"products": results},
    )
