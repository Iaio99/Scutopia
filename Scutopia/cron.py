import json
import requests
from datetime import date
from os.path import dirname
from urllib.parse import quote_plus as url_encode

from django_cron import CronJobBase, Schedule
from django.db.utils import IntegrityError
from django.db.models import Max

from . import cursor
from .models import Professors, Authorship
from .serializers import ProfessorsSerializer,  PublicationsSerializer


localhost = "http://localhost:8000/"


class MaximumRequestsError(Exception):
    "Reached the maximum queries that can be aksed to Scopus"


def get_last_download(author_id):
    args = Authorship.objects.select_related("eid").filter(scopus_id = author_id)
    download_date = args.aggregate(Max("eid__download_date"))["eid__download_date__max"]

    if args.count:
        return download_date.strftime("%Y")
    
    return 0


def get_publications(apikey: str,  author_id: str, index = "scopus", view = "COMPLETE"):
    global reset_time
    reset_time = None

    url = "https://api.elsevier.com/content/search/" + index + "?query={}&view=" + view + "&apikey=" + apikey
    url = url.format(f"AU-ID({url_encode(author_id)}) AND PUBYEAR > {get_last_download(author_id)}")
    r = requests.get(url)
    
    match r.status_code:
        case 200:
            api_response = json.loads(r.text)
            result_set = api_response["search-results"]["entry"]

            num_publications = int(api_response['search-results']['opensearch:totalResults'])

            if num_publications == 0:
                return None

            while num_publications > len(result_set):
                for e in api_response["search-results"]["link"]:
                    if e['@ref'] == 'next':
                        next_url = e['@href']

                r = requests.get(next_url)
                api_response = json.loads(r.text)
                result_set += api_response["search-results"]["entry"]

            for publication in result_set:
                save_publications(publication)
                save_authorship(publication["eid"], publication["author"])

        case 400:
            raise Exception("Invalid Request")
        case 401:
            raise Exception("Authentication Error")
        case 403:
            raise Exception("Authorization Error")
        case 405:
            raise Exception("Invalid HTTP Method")
        case 406:
            raise Exception("Invalid Mime Type")
        case 429:
            reset_time = int(r.headers["X-RateLimit-Reset"])
            raise MaximumRequestsError      
        case 500:
            raise Exception("Generic Error")  


def save_publications(publication):
    while True:
        try:
            publications_serializer = PublicationsSerializer(data={
                "eid": publication["eid"], 
                "title": publication["dc:title"],
                "publication_date": publication["prism:coverDate"],
                "magazine": publication["prism:publicationName"],
                "volume": publication["prism:volume"],
                "page_range": publication["prism:pageRange"],
                "doi": publication["prism:doi"],
                "download_date": str(date.today()),
                "scopus_id": publication["dc:identifier"].replace("SCOPUS_ID:", "")})

            if publications_serializer.is_valid():
                publications_serializer.save()

            break
        except KeyError as e:
            new_data = {str(e).replace("'",""): ""}
            publication.update(new_data)


def save_authorship(eid: str, authors: list):
    for author in authors:
        try:
            cursor.execute(f"INSERT INTO Authorship (`Scopus ID`, `EID`) VALUES(\"{author['authid']}\", '{eid}');")
        except IntegrityError:
            pass


class ScopusScraper(CronJobBase):
    RUN_AT_TIMES = ['13:18']
    RETRY_AFTER_FAILURE_MINS = 1
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'Scutopia.ScopusScraper'

    def do(self):
        professors = Professors.objects.all()
        professors_serializer = ProfessorsSerializer(professors, many=True)
        authors_id = professors_serializer.data

        with open(dirname(__file__)+'/../keys.json') as fp:
            keys = json.load(fp)
            APIKEY = keys["apikey"]
        
        try:
            for author in authors_id:
                get_last_download(author["scopus_id"])
                get_publications(APIKEY, author["scopus_id"])
        except MaximumRequestsError as e:
            print(f"{str(e)}. The counter of requests will be resetted in date {str(date.fromtimestamp(reset_time))}")