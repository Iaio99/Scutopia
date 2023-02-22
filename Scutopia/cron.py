"""Module providingFunction printing python version."""

from os.path import dirname
#from urllib.parse import quote_plus as url_encode

import json
import requests

from django_cron import CronJobBase, Schedule

from .db import save_authorship, get_last_download, save_publications
from .models import Professors


class MaximumRequestsError(Exception):
    def __init__(self, reset_time):
        self.__reset_time = reset_time

    def __str__(self):
        return "Reached the maximum queries that can be aksed to Scopus"

    @property
    def reset_time(self):
        return self.__reset_time


def get_publications_scopus(apikey: str, author_id: str, index="scopus", view="COMPLETE"):
    last_downlad = get_last_download(author_id)
    query = f"AU-ID({(author_id)}) AND PUBYEAR > {last_downlad}"

    url = f"https://api.elsevier.com/content/search/{index}?query={query}&view={view}&apikey={apikey}"
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
                save_authorship(publication["eid"], author_id)

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
            raise MaximumRequestsError(int(r.headers["X-RateLimit-Reset"]))
        case 500:
            raise Exception("Generic Error")


class ScopusScraper(CronJobBase):
    RUN_AT_TIMES = ['01:20']
    RETRY_AFTER_FAILURE_MINS = 1
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'Scutopia.ScopusScraper'

    def do(self):
        professors = Professors.objects.all().values("scopus_id")

        with open(dirname(__file__)+"/../keys.json", "r", encoding="UTF-8") as fp:
            keys = json.load(fp)
            apikey = keys["apikey"]

        try:
            for author in professors:
                get_last_download(author["scopus_id"])
                get_publications_scopus(apikey, author["scopus_id"])
        except MaximumRequestsError as e:
            print(f"{str(e)}. The counter of requests will be resetted in date {e.reset_time}")
