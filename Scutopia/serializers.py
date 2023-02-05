from rest_framework import serializers
from .models import Professors, Pubblications


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


class PubblicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pubblications
        fields = ('eid',
                  'title',
                  'pubblication_date',
                  'magazine',
                  'volume',
                  'page_range',
                  'doi',
                  'download_date',
                  'scopus_id')