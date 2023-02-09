from rest_framework import serializers
from .models import Professors, Publications


class ProfessorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professors
        fields = ('scopus_id',
                  'cf',
                  'nominative',
                  'registration_number',
                  'ssd',
                  'department',
                  'hire_date',
                  'role')


class PublicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publications
        fields = ('eid',
                  'title',
                  'publication_date',
                  'magazine',
                  'volume',
                  'page_range',
                  'doi',
                  'download_date',
                  'scopus_id')