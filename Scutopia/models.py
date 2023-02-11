from django.db import models


class Adu(models.Model):
    code = models.PositiveIntegerField(db_column='Code', primary_key=True)
    name = models.CharField(db_column='Name', max_length=255)

    class Meta:
        managed = False
        db_table = 'ADU'


class Authorship(models.Model):
    scopus_id = models.OneToOneField('Professors', models.DO_NOTHING, db_column='Scopus ID', primary_key=True)
    eid = models.ForeignKey('Publications', models.DO_NOTHING, db_column='EID')

    class Meta:
        managed = False
        db_table = 'Authorship'
        unique_together = (('scopus_id', 'eid'),)


class Professors(models.Model):
    scopus_id = models.CharField(db_column='Scopus ID', primary_key=True, max_length=32)
    cf = models.CharField(db_column='CF', max_length=16)
    nominative = models.CharField(db_column='Nominative', max_length=32)
    registration_number = models.CharField(db_column='Registration Number', max_length=16)
    ssd = models.ForeignKey('Ssd', models.DO_NOTHING, db_column='SSD')
    department = models.CharField(db_column='Department', max_length=64)
    hire_date = models.DateField(db_column='Hire Date')
    role = models.CharField(db_column='Role', max_length=11)

    class Meta:
        managed = False
        db_table = 'Professors'


class Publications(models.Model):
    eid = models.CharField(db_column='EID', primary_key=True, max_length=32)
    title = models.TextField(db_column='Title', max_length=65535)
    publication_date = models.DateField(db_column='Publication Date')
    magazine = models.CharField(db_column='Magazine', max_length=255, blank=True, null=True)
    volume = models.CharField(db_column='Volume', max_length=45, blank=True, null=True)
    page_range = models.CharField(db_column='Page Range', max_length=45, blank=True, null=True)
    doi = models.CharField(db_column='DOI', max_length=255, blank=True, null=True)
    download_date = models.DateField(db_column='Download Date')

    class Meta:
        managed = False
        db_table = 'Publications'


class Sc(models.Model):
    code = models.CharField(db_column='Code', primary_key=True, max_length=2)
    name = models.CharField(db_column='Name', max_length=255)
    adu = models.ForeignKey(Adu, models.DO_NOTHING, db_column='ADU')

    class Meta:
        managed = False
        db_table = 'SC'


class Ssd(models.Model):
    code = models.CharField(db_column='Code', primary_key=True, max_length=12)
    name = models.CharField(db_column='Name', max_length=255)
    sc = models.ForeignKey(Sc, models.DO_NOTHING, db_column='SC')

    class Meta:
        managed = False
        db_table = 'SSD'


class Concat(models.Aggregate):
    function = 'GROUP_CONCAT'
    template = '%(function)s(%(distinct)s%(expressions)s)'

    def __init__(self, expression, distinct=False, **extra):
        super(Concat, self).__init__(
            expression,
            distinct='DISTINCT ' if distinct else '',
            output_field= models.CharField(),
            **extra)
