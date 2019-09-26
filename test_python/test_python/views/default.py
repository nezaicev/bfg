from datetime import datetime

from pyramid.view import view_config
from pyramid.request import Request
import pyramid.httpexceptions as exc

from test_python.utils import unzip
from test_python.utils import pagination
from test_python.utils import get_answers_to_api
from test_python.utils import api_p
from sqlalchemy import func

import redis
import pickle



from .. import models

rs = redis.StrictRedis(host='localhost', port=6379, db=1)

@view_config(route_name='index', renderer='../templates/all_request.jinja2')
def index(request):
    query = request.dbsession.query(models._Request)
    requests = query.all()
    
    return {'requests': requests}


@view_config(route_name='get_answers', renderer='../templates/one_request.jinja2')
def get_answers(request):
    items = int(request.GET['count'])
    sort='desc'

    if rs.get(request.GET['query']) and rs.get('sort')==request.GET['sort']:
        rs_data=pickle.loads(rs.get(request.GET['query']))
        page,count_page=pagination(items,request.GET['page'],rs_data)

    else:
        request_id = request.dbsession.query(models._Request.id).filter(models._Request.name == request.GET['query'])


        if request.GET['sort']=='asc':
            # print(request.GET['sort'])

            answers = request.dbsession.query(models.Answer).order_by(models.Answer.creation_date.asc()).filter(
                models.Answer.request_id == request_id).all()
        else:
            # print(request.GET['sort'])

            answers = request.dbsession.query(models.Answer).order_by(models.Answer.creation_date.desc()).filter(
                models.Answer.request_id == request_id).all()
                # answers = request.dbsession.query(models.Answer).order_by(models.Answer.last_activity_date).filter(request_id == models.Answer.request_id).all()
        # else:

        page,count_page=pagination(items,request.GET['page'],answers)
        rs_data=pickle.dumps(answers)
        rs.set(request.GET['query'],rs_data)
        rs.set('sort',request.GET['sort'])
        rs.expire('sort', 60)
        rs.expire(request.GET['query'],60)

    return {'answers': page, 'page_count': count_page, 'query': request.GET['query'],
            'count_items': request.GET['count'],'now_page':request.GET['page'],'sort':sort}


@view_config(route_name='search', renderer='../templates/search.jinja2')
def search(request):
    return {}


@view_config(route_name='get_requests', request_method='GET')
def get_requests(request):
    search_str = request.GET['query']
    data=get_answers_to_api(search_str)

    req = request.dbsession.query(models._Request).filter(models._Request.name == search_str).first()

    if req:
        req.create_date = func.current_timestamp()
        for answer in data['items']:
            models.Answer(answer).update_answers(req.id,request.dbsession)

    else:

        req = models._Request(request)
        req.add_request()
        req = request.dbsession.query(models._Request).filter(models._Request.name == search_str).first()

        for answer in data['items']:
            models.Answer(answer).add_answers(req.id,request)


    request.dbsession.flush()
    return exc.HTTPFound(request.route_url("index"))
