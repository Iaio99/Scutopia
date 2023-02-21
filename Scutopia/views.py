"""Module providingFunction printing python version."""

from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.decorators import permission_required, login_required
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie, requires_csrf_token
from rest_framework.parsers import JSONParser
from django.shortcuts import render, redirect

from . import db
from . import models
from . import forms
from .serializers import ProfessorsSerializer

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
#@login_required(login_url='/accounts/login')
def view_adu(request) -> JsonResponse:
   return JsonResponse('')


@csrf_exempt
#@login_required(login_url='/accounts/login')
def view_authors(request) -> JsonResponse:
   if request.method == 'GET':
      professors = models.Professors.objects.all()
      professors_serializer = ProfessorsSerializer(professors, many=True)
      return JsonResponse(professors_serializer.data, safe=False)
   
   elif request.method == 'POST':
         professor_data=JSONParser().parse(request)
         professors_serializer = ProfessorsSerializer(data=professor_data)

         if professors_serializer.is_valid():
            professors_serializer.save()
            return JsonResponse('Added Successfully!!', safe=False)

         return JsonResponse('Failed to Add.',safe=False)


@csrf_exempt
#@login_required(login_url='/accounts/login')
def view_departements(request) -> JsonResponse:
   return JsonResponse('')


@csrf_protect
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

      publications = db.get_publications(pub_date_gt, pub_date_lt, ssd)
      
      return JsonResponse(list(publications), safe=False)
      

@csrf_exempt
#@login_required(login_url='/accounts/login')
def view_ssd(request) -> JsonResponse:
    if request.method == 'GET':      
        try:
            pub_date_gt = request.GET['date_gt']
        except KeyError:
            pub_date_gt = '0001-1-1'

        try:
            pub_date_lt = request.GET['date_lt']
        except KeyError:
            pub_date_lt = '9999-1-1'

        data = db.get_ssd_data_from_date_range(pub_date_gt, pub_date_lt)

        return JsonResponse(list(data), safe=False)

@csrf_exempt
#@login_required(login_url='/accounts/login')
def add_professor(request):
   if request.method == 'POST':  
      form = forms.professor_form(request.POST)

      if form.is_valid():
        form.save(commit=True)
        return redirect('/api/accounts/login')
   else:
      form = forms.professor_form() 

   return render(request, 'insert_professor.html', {'prop_form': forms.professor_form})