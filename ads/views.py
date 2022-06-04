import json
import os

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView
import pandas
from ads.models import Ad, Category


class AddInfo(View):
    def get(self, request):
        data_ads = pandas.read_csv('/Users/NurmiQ/PycharmProjects/djangoHW_27/data/ads.csv', sep=',').to_dict()

        i = 0

        while max(data_ads['Id'].keys()) > i:
            ad = Ad.objects.create(
                name=data_ads["name"][i],
                author=data_ads["author"][i],
                price=data_ads["price"][i],
                description=data_ads["description"][i],
                address=data_ads["address"][i],
                is_published=data_ads["is_published"][i],
            )
            i += 1
        return JsonResponse("Everything is ok", safe=False, status=200)


class AddInfoCat(View):
    def get(self, request):
        data_ads = pandas.read_csv('/Users/NurmiQ/PycharmProjects/djangoHW_27/data/categories.csv', sep=',').to_dict()

        i = 0

        while max(data_ads['id'].keys()) > i:
            cat = Category.objects.create(
                name=data_ads["name"][i]
            )
            i += 1
        return JsonResponse("Everything is ok", safe=False, status=200)


class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()
        response = []
        for category in categories:
            response.append({
                "id": category.id,
                "name": category.name,
            })

        return JsonResponse(response, safe=False)


    def post(self, request):
        category_data = json.loads(request.body)

        category = Category()
        category.name = category_data["name"]

        try:
            category.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        category.save()
        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        try:
            category = self.get_object()
        except:
            return JsonResponse({"error": "Not found"}, status=404)
        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


class AdView(View):
    def get(self, request):
        ads = Ad.objects.all()
        response = []
        for ad in ads:
            response.append({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price,
            })

        return JsonResponse(response, safe=False)

    def post(self, request):
        ad_data = json.loads(request.body)

        ad = Ad()
        ad.name = ad_data["name"]
        ad.author = ad_data["author"]
        ad.price = ad_data["price"]
        ad.description = ad_data["description"]
        ad.address = ad_data["address"]
        ad.is_published = ad_data["false"]

        try:
            ad.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        ad.save()
        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published,
        })


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
        except:
            return JsonResponse({"error": "Not found"}, status=404)
        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published,
        })


