from pyramid_celery import celery_app as app
import transaction
from pyramid.threadlocal import get_current_registry
from test_python.models import (
            get_engine,
            get_session_factory,
            get_tm_session,
            )

from test_python import models
from test_python.utils import get_answers_to_api
from sqlalchemy import func
from test_python.utils import rs


# rs = redis.StrictRedis(host='localhost', port=6379, db=1)

@app.task
def update(*args, **kwargs):
    mes=''
    registry = get_current_registry()
    settings = registry.settings
    engine = get_engine(settings)
    session_factory = get_session_factory(engine)
    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        list_requests = dbsession.query(models._Request).all()
        for r in list_requests:
            data=get_answers_to_api(r.name)
            count_ans=dbsession.query(func.count('*')).filter(models.Answer.request_id == r.id).scalar()
            r.create_date = func.current_timestamp()
            r.count = count_ans
            # print(count_ans)
            dbsession.add(r)
            for answer in data['items']:
                answer=models.Answer(answer)
                # print(answer.title)
                answer.request_id = r.id
                dbsession.merge(answer)
            if count_ans < dbsession.query(func.count('*')).filter(models.Answer.request_id == r.id).scalar():
                print(r.id,r.name,count_ans)
                if mes:
                    mes+=" ,"+r.name
                else:
                    mes =r.name

    rs.set('update', mes)
    # rs.expire('update', 60)
    print(rs.get('update'))







