from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required, login_required
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from . import models, serializers

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


@csrf_exempt
@login_required(login_url='/accounts/login')
def view_adu(request) -> JsonResponse:
   return JsonResponse('')


@csrf_exempt
@login_required(login_url='/accounts/login')
def view_authors(request) -> JsonResponse:
   if request.method == 'GET':
      professors = models.Professors.objects.all()
      professors_serializer = serializers.ProfessorsSerializer(professors, many=True)
      return JsonResponse(professors_serializer.data, safe=False)
   
   elif request.method == 'POST':
         professor_data=JSONParser().parse(request)
         professors_serializer = serializers.ProfessorsSerializer(data=professor_data)

         if professors_serializer.is_valid():
            professors_serializer.save()
            return JsonResponse('Added Successfully!!', safe=False)

         return JsonResponse('Failed to Add.',safe=False)


@csrf_exempt
@login_required(login_url='/accounts/login')
def view_departements(request) -> JsonResponse:
   return JsonResponse('')


@csrf_exempt
@login_required(login_url='/accounts/login')
def view_publications(request):
   if request.method == 'GET' and request.user.has_perm('Scutopia.view_publications'):
      publications = models.Publications.objects.all()
      publications_serializer = serializers.PublicationsSerializer(publications, many=True)
      return JsonResponse(publications_serializer.data, safe=False)
   
   elif request.method == 'POST' and request.user.has_perm('Scutopia.add_publications'):
         publication_data=JSONParser().parse(request)
         publications_serializer = serializers.PublicationsSerializer(data=publication_data)

         publication_data['publication_date'] = datetime.strptime(publication_data['publication_date'], '%Y-%m-%d').date()
         publication_data['download_date'] = datetime.strptime(publication_data['download_date'], '%Y-%m-%d').date()        

         if publications_serializer.is_valid():
            publications_serializer.save()
            return JsonResponse('Added Successfully!!', safe=False)

         return JsonResponse('Failed to Add.',safe=False)


@csrf_exempt
@login_required(login_url='/accounts/login')
def view_ssd(request) -> JsonResponse:
   return JsonResponse('')
