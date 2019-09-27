# bfg

для запуска требуется redis, mysql, celery

Запуск обработчика обновлений : celery worker --beat -A pyramid_celery.celery_app --ini development.ini
Запуск уведомлений по websocket : python websocket.py
Данные задачи можно вынести в supervisor
