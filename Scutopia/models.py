from django.db import models

# Create your models here.


class Adu(models.Model):
    code = models.PositiveIntegerField(db_column='Code', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ADU'


class Authorship(models.Model):
    scopus_id = models.OneToOneField('Professors', models.DO_NOTHING, db_column='Scopus ID', primary_key=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eid = models.ForeignKey('Pubblications', models.DO_NOTHING, db_column='EID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Authorship'
        unique_together = (('scopus_id', 'eid'),)


class Professors(models.Model):
    scopus_id = models.CharField(db_column='Scopus ID', primary_key=True, max_length=32)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cf = models.CharField(db_column='CF', max_length=16)  # Field name made lowercase.
    nominative = models.CharField(db_column='Nominative', max_length=32)  # Field name made lowercase.
    registration_number = models.CharField(db_column='Registration Number', max_length=16)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ssd = models.ForeignKey('Ssd', models.DO_NOTHING, db_column='SSD')  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=64)  # Field name made lowercase.
    hire_date = models.DateField(db_column='Hire Date')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    role = models.CharField(db_column='Role', max_length=11)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Professors'


class Pubblications(models.Model):
    eid = models.CharField(db_column='EID', primary_key=True, max_length=32)  # Field name made lowercase.
    title = models.TextField(db_column='Title', max_length=65535)  # Field name made lowercase.
    pubblication_date = models.DateField(db_column='Pubblication Date')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    magazine = models.CharField(db_column='Magazine', max_length=255, blank=True, null=True)  # Field name made lowercase.
    volume = models.CharField(db_column='Volume', max_length=45, blank=True, null=True)  # Field name made lowercase.
    page_range = models.CharField(db_column='Page Range', max_length=45, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    doi = models.CharField(db_column='DOI', max_length=255, blank=True, null=True)  # Field name made lowercase.
    download_date = models.DateField(db_column='Download Date')  # Field name made lowercase. Field renamed to remove unsuitable characters.
#    scopus_id = models.ForeignKey(Professors, models.DO_NOTHING, db_column='Scopus ID')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    scopus_id = models.CharField(db_column='Scopus ID', max_length=32)


    class Meta:
        managed = False
        db_table = 'Pubblications'


class Sc(models.Model):
    code = models.CharField(db_column='Code', primary_key=True, max_length=2)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255)  # Field name made lowercase.
    adu = models.ForeignKey(Adu, models.DO_NOTHING, db_column='ADU')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SC'


class Ssd(models.Model):
    code = models.CharField(db_column='Code', primary_key=True, max_length=12)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255)  # Field name made lowercase.
    sc = models.ForeignKey(Sc, models.DO_NOTHING, db_column='SC')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SSD'