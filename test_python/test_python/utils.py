import gzip
import json
from collections import namedtuple
from pyramid.request import Request
import redis

api_p=namedtuple('api','url pagesize order sort tagged site')('https://api.stackexchange.com/2.2/search?'
                                                              ,5,'desc','creation','','stackoverflow')
rs = redis.StrictRedis(host='localhost', port=6379, db=1)
def pagination(items,page_now,answers):
    list_end = items * int(page_now)
    list_start = list_end - items

    if (len(answers) - list_start) < items:
        page = answers[list_start:list_end]
    else:
        page = answers[list_start:list_end]

    if len(answers) % items:
        count_page = (len(answers) // items) + 1
    else:
        count_page = (len(answers) // items)

    return page, count_page


def unzip(response):
    tmp = gzip.decompress(response.body).decode('utf-8')
    result = json.loads(tmp)
    return result
def get_answers_to_api(search_str):
    r = Request.blank('{}page=1&pagesize={}&order={}&sort={}&tagged={}&site={}'.format(api_p.url, api_p.pagesize,
                                                                                       api_p.order, api_p.sort,
                                                                                       search_str, api_p.site))
    data_gzip = r.get_response()
    data = unzip(data_gzip)
    return data

