import json
import requests
from datetime import date
from os.path import dirname
from urllib.parse import quote_plus as url_encode

from django_cron import CronJobBase, Schedule
from django.db.utils import IntegrityError

from . import cursor
from .models import Professors
from .serializers import PubblicationsSerializer, ProfessorsSerializer


localhost = "http://localhost:8000/"


class MaximumRequestsError(Exception):
    "Reached the maximum queries that can be aksed to Scopus"


def get_pubblications(apikey: str,  author_id: str, index = "scopus", view = "COMPLETE"):
    global reset_time
    reset_time = None

    url = "https://api.elsevier.com/content/search/" + index + "?query={}&view=" + view + "&apikey=" + apikey
    url = url.format(f"AU-ID({url_encode(author_id)})")
    r = requests.get(url)
    
    match r.status_code:
        case 200:
            api_response = json.loads(r.text)
            result_set = api_response["search-results"]["entry"]

            num_pubblications = int(api_response['search-results']['opensearch:totalResults'])

            while num_pubblications > len(result_set):
                for e in api_response["search-results"]["link"]:
                    if e['@ref'] == 'next':
                        next_url = e['@href']

                r = requests.get(next_url)
                api_response = json.loads(r.text)
                result_set += api_response["search-results"]["entry"]

            for pubblication in result_set:
                save_pubblications(pubblication)
                save_authorship(pubblication["eid"], pubblication["author"])

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


def save_pubblications(pubblication):
    while True:
        try:
            pubblications_serializer = PubblicationsSerializer(data={
                "eid": pubblication["eid"], 
                "title": pubblication["dc:title"],
                "pubblication_date": pubblication["prism:coverDate"],
                "magazine": pubblication["prism:publicationName"],
                "volume": pubblication["prism:volume"],
                "page_range": pubblication["prism:pageRange"],
                "doi": pubblication["prism:doi"],
                "download_date": str(date.today()),
                "scopus_id": pubblication["dc:identifier"].replace("SCOPUS_ID:", "")})

            if pubblications_serializer.is_valid():
                pubblications_serializer.save()

            break
        except KeyError as e:
            new_data = {str(e).replace("'",""): ""}
            pubblication.update(new_data)


def save_authorship(eid: str, authors: list):
    for author in authors:
        try:
            cursor.execute(f"INSERT INTO Authorship (`Scopus ID`, `EID`) VALUES(\"{author['authid']}\", '{eid}');")
        except IntegrityError:
            pass


class ScopusScraper(CronJobBase):
    RUN_AT_TIMES = ['18:16']
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
                get_pubblications(APIKEY, author["scopus_id"])
        except MaximumRequestsError as e:
            print(f"{str(e)}. The counter of requests will be resetted in date {str(date.fromtimestamp(reset_time))}")