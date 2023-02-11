from datetime import datetime
from django.db import connection
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import Count, Subquery, F, Q
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
#@login_required(login_url='/accounts/login')
def view_publications(request):
   if request.method == 'GET':# and request.user.has_perm('Scutopia.view_publications'):
      try:
         pub_date_gt = request.GET['date_gt']
      except KeyError:
         pub_date_gt = '0001-1-1'

      try:
         pub_date_lt = request.GET['date_lt']
      except KeyError:
         pub_date_lt = '9999-1-1'

      try:
         ssd = request.GET['ssd']
      except KeyError:
         ssd = None

      publications = models.Authorship.objects.select_related("eid").values("eid").annotate(authors = models.Concat("scopus_id")).values_list("eid", "authors", "eid__publication_date", "eid__title", "eid__magazine", "eid__volume", "eid__page_range", "eid__doi", "eid__download_date", "scopus_id__ssd").filter(eid__publication_date__range = [pub_date_gt, pub_date_lt])

      if ssd is not None:
         publications = publications.filter(scopus_id__ssd = ssd)
      
      return JsonResponse(list(publications), safe=False)
      

@csrf_exempt
@login_required(login_url='/accounts/login')
def view_ssd(request) -> JsonResponse:
   if request.method == 'GET':
      with connection.cursor() as cursor:
      
         try:
            pub_date_gt = request.GET['date_gt']
         except KeyError:
            pub_date_gt = '0001-1-1'

         try:
            pub_date_lt = request.GET['date_lt']
         except KeyError:
            pub_date_lt = '9999-1-1'

         num_professors_query = models.Professors.objects.values("ssd").annotate(ssd_p=F("ssd")).annotate(num_professors = Count("scopus_id")).all().values_list("num_professors", "ssd_p", "scopus_id")
         
         data = (
            models.Authorship.objects.annotate(num_professors = Subquery(num_professors_query.values("num_professors")))
            .values("scopus_id__ssd", "num_professors")
            .annotate(num_pubblications = Count("eid", filter = Q(eid__publication_date__range = [pub_date_gt, pub_date_lt])))
         )

#      with connection.cursor() as cursor:
#         cursor.execute("""SELECT 
#        `SSD`.`Code` AS `SSD`,
#        (SELECT 
#                COUNT(0)
#            FROM
#                `Professors`
#            WHERE
#                (`Professors`.`SSD` = `SSD`.`Code`)) AS `Docenti`,
#        COUNT(0) AS `Pubblicazioni`
#    FROM
#        ((`SSD`
#        JOIN `Professors` ON ((`SSD`.`Code` = `Professors`.`SSD`)))
#        JOIN `Authorship` ON ((`Authorship`.`Scopus ID` = `Professors`.`Scopus ID`)))
#    GROUP BY `SSD`.`Code`""")
#
#         columns = [col[0] for col in cursor.description]
#         
#         data = (dict(zip(columns, row)) for row in cursor.fetchall():)
               
   return JsonResponse(list(data), safe=False)
