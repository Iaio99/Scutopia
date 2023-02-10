from datetime import datetime
from django.db import connection
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
#      return JsonResponse({"message": "Login Successfull!"})


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

      query_pub_year = request.GET.get('year', None) 
      query_pub_month = request.GET.get('month', None) 

      if query_pub_year is not None and query_pub_month is not None:
         publications = [{"eid": x.eid, "authors": [], "title": str(x.title), "publication_date": x.publication_date, "magazine": x.magazine, "volume": x.volume, "page_range": x.page_range, "doi": x.doi, "download_date": x.download_date} for x in models.Publications.objects.filter(publication_date__year = query_pub_year).filter(publication_date__month = query_pub_month)]

      elif query_pub_year is not None:
         publications = [{"eid": x.eid, "authors": [], "title": str(x.title), "publication_date": x.publication_date, "magazine": x.magazine, "volume": x.volume, "page_range": x.page_range, "doi": x.doi, "download_date": x.download_date} for x in models.Publications.objects.filter(publication_date__year = query_pub_year)]
      
      else:
         publications = [{"eid": x.eid, "authors": [], "title": str(x.title), "publication_date": x.publication_date, "magazine": x.magazine, "volume": x.volume, "page_range": x.page_range, "doi": x.doi, "download_date": x.download_date} for x in models.Publications.objects.all()]

      for p in publications:
         authors = models.Authorship.objects.get(eid=p["eid"])
         p["authors"] = str(authors.scopus_id.scopus_id)
      
      return JsonResponse(publications, safe=False)
   
#   elif request.method == 'POST' and request.user.has_perm('Scutopia.add_publications'):
#         publication_data=JSONParser().parse(request)
#         publications_serializer = serializers.PublicationsSerializer(data=publication_data)
#
#         publication_data['publication_date'] = datetime.strptime(publication_data['publication_date'], '%Y-%m-%d').date()
#         publication_data['download_date'] = datetime.strptime(publication_data['download_date'], '%Y-%m-%d').date()        
#
#         if publications_serializer.is_valid():
#            publications_serializer.save()
#            return JsonResponse('Added Successfully!!', safe=False)

#         return JsonResponse('Failed to Add.',safe=False)


@csrf_exempt
@login_required(login_url='/accounts/login')
def view_ssd(request) -> JsonResponse:
   if request.method == 'GET':
      with connection.cursor() as cursor:
         cursor.execute("""SELECT 
        `SSD`.`Code` AS `SSD`,
        (SELECT 
                COUNT(0)
            FROM
                `Professors`
            WHERE
                (`Professors`.`SSD` = `SSD`.`Code`)) AS `Docenti`,
        COUNT(0) AS `Pubblicazioni`
    FROM
        ((`SSD`
        JOIN `Professors` ON ((`SSD`.`Code` = `Professors`.`SSD`)))
        JOIN `Authorship` ON ((`Authorship`.`Scopus ID` = `Professors`.`Scopus ID`)))
    GROUP BY `SSD`.`Code`""")

         columns = [col[0] for col in cursor.description]
         
         results = []
         for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
               
   return JsonResponse(results, safe=False)
