from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required, login_required
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from .models import Professors, Pubblications
from .serializers import ProfessorsSerializer, PubblicationsSerializer


def view_departements(request) -> JsonResponse:
   return JsonResponse("")


@csrf_exempt
@login_required(login_url="/accounts/login")
def view_pubblications(request):
   if request.method == 'GET' and request.user.has_perm("Scutopia.view_pubblications"):
      pubblications = Pubblications.objects.all()
      pubblications_serializer = PubblicationsSerializer(pubblications, many=True)
      return JsonResponse(pubblications_serializer.data, safe=False)
   
   elif request.method == 'POST' and request.user.has_perm("Scutopia.add_pubblications"):
         pubblication_data=JSONParser().parse(request)
         pubblications_serializer = PubblicationsSerializer(data=pubblication_data)

         pubblication_data["pubblication_date"] = datetime.strptime(pubblication_data["pubblication_date"], '%Y-%m-%d').date()
         pubblication_data["download_date"] = datetime.strptime(pubblication_data["download_date"], '%Y-%m-%d').date()        

         if pubblications_serializer.is_valid():
            pubblications_serializer.save()
            return JsonResponse("Added Successfully!!", safe=False)

         return JsonResponse("Failed to Add.",safe=False)


@csrf_exempt
def view_authors(request) -> JsonResponse:
   if request.method == 'GET':
      professors = Professors.objects.all()
      professors_serializer = ProfessorsSerializer(professors, many=True)
      return JsonResponse(professors_serializer.data, safe=False)
   
   elif request.method == 'POST':
         professor_data=JSONParser().parse(request)
         professors_serializer = ProfessorsSerializer(data=professor_data)

         if professors_serializer.is_valid():
            professors_serializer.save()
            return JsonResponse("Added Successfully!!", safe=False)

         return JsonResponse("Failed to Add.",safe=False)


@csrf_exempt
def view_ssd(request) -> JsonResponse:
   return JsonResponse("")


@csrf_exempt
def view_adu(request) -> JsonResponse:
   return JsonResponse("")


@csrf_exempt
def view_login(request):
   username = request.POST['username']
   password = request.POST['password']
   user = authenticate(request, username=username, password=password)

   if user is not None:
      login(request, user)


@csrf_exempt
def view_logout(request):
   logout(request)
# Create your views here.
