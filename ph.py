import os
import time

import requests  # noqa
from bs4 import BeautifulSoup  # noqa


class FDA_PH(object):
    def __init__(self):
        session = requests.Session()
        session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) " \
                                        "Gecko/20100101 Firefox/115.0"

        self.session = session

    def request(self):
        uri = "https://www.fda.gov.ph/wp-admin/admin-ajax.php"
        session = self.session

        request_headers = {
            "TE": "trailers",
            "Host": "www.fda.gov.ph",
            "Origin": "https://www.fda.gov.ph",
            "Referer": "https://www.fda.gov.ph/advisories/",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json, text/javascript, */*; q=0.01",
        }
        payload = {
            'draw': '1', 'columns[0][data]': 'date', 'columns[0][name]': 'date', 'columns[0][searchable]': 'true',
            'columns[0][orderable]': 'true', 'columns[0][search][value]': '', 'columns[0][search][regex]': 'false',
            'columns[1][data]': 'image', 'columns[1][name]': 'image', 'columns[1][searchable]': 'false',
            'columns[1][orderable]': 'false', 'columns[1][search][value]': '', 'columns[1][search][regex]': 'false',
            'columns[2][data]': 'title', 'columns[2][name]': 'title', 'columns[2][searchable]': 'true',
            'columns[2][orderable]': 'true', 'columns[2][search][value]': '', 'columns[2][search][regex]': 'false',
            'columns[3][data]': 'categories', 'columns[3][name]': 'categories', 'columns[3][searchable]': 'true',
            'columns[3][orderable]': 'false', 'columns[3][search][value]': '', 'columns[3][search][regex]': 'false',
            'columns[4][data]': 'categories_hfilter', 'columns[4][name]': 'categories_hfilter',
            'columns[4][searchable]': 'true', 'columns[4][orderable]': 'true', 'columns[4][search][value]': '',
            'columns[4][search][regex]': 'false', 'order[0][column]': '0', 'order[0][dir]': 'desc', 'start': '0',
            'length': '50', 'search[value]': '', 'search[regex]': 'false', 'table_id': 'ptp_0430655160c1850c_2',
            'action': 'ptp_load_posts', '_ajax_nonce': 'eef8799c9b'
        }

        r = session.post(uri, data=payload, headers={**session.headers, **request_headers})
        # r.raise_for_status()
        # print(r.text)
        return r

    def get_details(self):
        response = self.request()

        for i in response.json()["data"]:
            post_id, title = i["__attributes"]["id"], i["title"]
            uri = BeautifulSoup(title, "lxml").a.attrs["href"]
            self.get_detail(uri=uri, name=post_id)

            time.sleep(1)

        return response.text

    def get_detail(self, uri, name):
        base_dir = "data/ph"
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        r = self.session.get(uri)
        with open(f"{base_dir}/{name}.html", "w") as wf:
            wf.write(r.text)


if __name__ == '__main__':
    print(FDA_PH().get_details())
