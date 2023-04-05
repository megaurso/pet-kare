from django.shortcuts import render
from rest_framework.views import APIView, Request, Response, status
from .serializers import PetSerializer
from .models import Pet
from traits.models import Trait
from groups.models import Group
from rest_framework.pagination import PageNumberPagination


class PetView(APIView, PageNumberPagination):
    def get(self, req: Request) -> Response:
        pets = Pet.objects.all().order_by("id")
        result_page = self.paginate_queryset(pets, req)

        serializer = PetSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, req: Request) -> Response:
        serializer = PetSerializer(data=req.data)

        serializer.is_valid(raise_exception=True)

        group = serializer.validated_data.pop("group")
        traits = serializer.validated_data.pop("traits")

        group_dic = Group.objects.filter(
            scientific_name__iexact=group["scientific_name"]
        ).first()

        if not group_dic:
            group_dic = Group.objects.create(**group)

        pet = Pet.objects.create(**serializer.validated_data, group=group_dic)

        for trait in traits:
            trait_obj = Trait.objects.filter(name__iexact=trait["name"]).first()

            if not trait_obj:
                trait_obj = Trait.objects.create(**trait)

            pet.traits.add(trait_obj)

        pet.save()
        serializer = PetSerializer(pet)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
