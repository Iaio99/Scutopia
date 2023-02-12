"""Module providingFunction printing python version."""

from datetime import datetime, date

from django.db import connection
from django.db.utils import IntegrityError
from django.db.models import Count, Max, Subquery, Q

from . import models


cursor = connection.cursor()


def save_publications(publication):
    while True:
        try:
            publication = models.Publications(
                publication["eid"], 
                publication["dc:title"],
                datetime.strptime(publication["prism:coverDate"], "%Y-%m-%d"),
                publication["prism:publicationName"],
                publication["prism:volume"],
                publication["prism:pageRange"],
                publication["prism:doi"],
                date.today(),
            )

            publication.save()
            break
        except KeyError as e:
            new_data = {str(e).replace("'",""): ""}
            publication.update(new_data)


def save_authorship(eid: str, authors: list):
    for author in authors:
        try:
            cursor.execute(f"\
                INSERT INTO Authorship (`Scopus ID`, `EID`) VALUES(\"{author['authid']}\", '{eid}');\
            ")
        except IntegrityError:
            pass


def get_last_download(author_id):
    args = models.Authorship.objects.select_related("eid").filter(scopus_id = author_id)
    download_date = args.aggregate(Max("eid__download_date"))["eid__download_date__max"]

    if args.count():
        return download_date.strftime("%Y")

    return 0


def get_publications(pub_date_gt, pub_date_lt, ssd):
    publications = models.Authorship.objects.select_related("eid").values("eid").annotate(
        authors = models.Concat("scopus_id")).values_list(
            "eid",
            "authors",
            "eid__publication_date",
            "eid__title",
            "eid__magazine",
            "eid__volume",
            "eid__page_range",
            "eid__doi",
            "eid__download_date",
            "scopus_id__ssd"
            ).filter(eid__publication_date__range = [pub_date_gt, pub_date_lt])

    if ssd is not None:
        publications = publications.filter(scopus_id__ssd = ssd)

    return publications


def get_ssd_data_from_date_range(pub_date_gt, pub_date_lt):
    professors_query = models.Professors.objects.annotate(
        num_professors = Count("scopus_id")).values_list("num_professors", "ssd", "scopus_id")

    data = (
        models.Authorship.objects.annotate(num_professors =
        Subquery(professors_query.values("num_professors")[:1]))
        .values("scopus_id__ssd", "num_professors")
        .annotate(num_pubblications = Count("eid", filter =
        Q(eid__publication_date__range = [pub_date_gt, pub_date_lt])))
    )

#SELECT SSD, num_professors, COUNT(EID)
#FROM Authorship JOIN
#(SELECT SSD, `Scopus ID`, COUNT(`Scopus ID`) as num_professors FROM Professors GROUP BY SSD, `Scopus ID`) as P ON Authorship.`Scopus ID` = P.`Scopus ID`
#GROUP BY Authorship.`Scopus ID`;

    return data
