from django.shortcuts import render
from rest_framework.views import APIView, Request, Response, status
from .serializers import PetSerializer
from .models import Pet


class PetView(APIView):
    def get(self, req: Request) -> Response:
        pets = Pet.objects.all()
        
        serializer = PetSerializer(pets, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, req: Request) -> Response:
        serializer = PetSerializer(data=req.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        pet = Pet.objects.create(**serializer.validated_data)

        serializer = PetSerializer(pet)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
