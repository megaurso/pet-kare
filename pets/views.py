from django.shortcuts import render
from rest_framework.views import APIView, Request, Response, status
from .serializers import PetSerializer
from .models import Pet
from traits.models import Trait
from groups.models import Group
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404


class PetView(APIView, PageNumberPagination):
    def get(self, req: Request) -> Response:
        pets = Pet.objects.all()
        trait = req.query_params.get("trait", None)

        if trait:
            pets = pets.filter(traits__name__iexact=trait)

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


class PetInfoView(APIView):
    def get(self, req: Request, pet_id: int) -> Response:

        pet = get_object_or_404(Pet, id=pet_id)

        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, req: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(data=req.data, partial=True)

        serializer.is_valid(raise_exception=True)

        if "group" in serializer.validated_data:
            group = serializer.validated_data.pop("group")
            group_dic = Group.objects.filter(
                scientific_name__iexact=group["scientific_name"]
            ).first()

            if not group_dic:
                group_dic = Group.objects.create(**group)

            pet.group = group_dic

        if "traits" in serializer.validated_data:
            traits = serializer.validated_data.pop("traits")
            new_list_traits = []
            for trait in traits:
                trait_name = trait["name"]
                trait_obj = Trait.objects.filter(name__iexact=trait_name).first()
                if not trait_obj:
                    trait_obj = Trait.objects.create(**trait)
                new_list_traits.append(trait_obj)
            pet.traits.set(new_list_traits)

        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)

        pet.save()
        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, req: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
