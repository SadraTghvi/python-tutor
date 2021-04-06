from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from . import models
import requests

# Create your views here.
BASE_CRAIGSLIST_URL = "https://losangeles.craigslist.org/search/?quesry={}"

def home(request):
    return render(request,"base.html")

def new_search(request):
    search = request.POST["search"]
    models.Search.objects.create(search=search)
    response = requests.get("https://losangeles.craigslist.org/search/?quesry=python%20tutor")
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    data = response.text
    soup = BeautifulSoup(data,features="html.parser")

    post_listing = soup.findAll("li", {"class": "result-row"})
    post_title = post_listing[0].find(class_="result-title").text
    post_url = post_listing[0].find("a").get("href")
    post_price = post_listing[0].find(class_="result-price").text

    print(post_title)
    print(post_url)
    print(post_price)
    stuff_for_frontend = {
        "search": search
        }
    return render(request, "myapp/new_search.html",stuff_for_frontend)
    
