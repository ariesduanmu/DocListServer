import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
settings = {
    'static_path': os.path.join(BASE_DIR, "app", "static"),
    "static_url_prefix": "/doc/static/",
    'template_path': os.path.join(BASE_DIR, "app", "template"),
    'autoreload': True,
}
