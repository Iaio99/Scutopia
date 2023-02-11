from django.db.utils import IntegrityError
from django.db.models import Max

from . import cursor
from .models import Authorship


def save_authorship(eid: str, authors: list):
    for author in authors:
        try:
            cursor.execute(f"INSERT INTO Authorship (`Scopus ID`, `EID`) VALUES(\"{author['authid']}\", '{eid}');")
        except IntegrityError:
            pass


def get_last_download(author_id):
    args = Authorship.objects.select_related("eid").filter(scopus_id = author_id)
    download_date = args.aggregate(Max("eid__download_date"))["eid__download_date__max"]

    if args.count():
        return download_date.strftime("%Y")
    
    return 0