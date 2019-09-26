def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('index', '/')
    config.add_route('search', '/search')
    config.add_route('get_answers', '/answers')
    config.add_route('get_requests', '/request')

