from rest_framework import serializers
from . import models


class ProfessorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Professors
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
        model = models.Publications
        fields = ('eid',
                  'title',
                  'publication_date',
                  'magazine',
                  'volume',
                  'page_range',
                  'doi',
                  'download_date')
