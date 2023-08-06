# sanic-conf
Django-like settings for Sanic

[![PyPI](https://img.shields.io/pypi/v/sanic-conf.svg)](https://pypi.org/project/sanic-conf/)
[![Build Status](https://travis-ci.org/dldevinc/sanic-conf.svg?branch=master)](https://travis-ci.org/dldevinc/sanic-conf)

## Quick Start

Installation
```
pip install sanic-conf
```

Create `settings.py` file
```
sanic
├─ app.py
└─ settings.py
```

Fill out the project settings
```
# settings.py

PROXIES_COUNT = 1
REAL_IP_HEADER = 'X-Real-IP'
```

Apply to Sanic config
```python
import os
from sanic import Sanic
from sanic_conf import settings

app = Sanic(__name__, load_env=False)

# settings
os.environ.setdefault('SANIC_SETTINGS_MODULE', 'settings')
app.config.update_config(settings)
```

## Environment variables 

Note that you can use [django-environ](https://github.com/joke2k/django-environ)
with Sanic.

```
pip install django-environ
```

```
# settings.py

import environ
env = environ.Env(
    DEBUG=(bool, False)
)

# reading .env file
environ.Env.read_env()

# False if not in os.environ
DEBUG = env('DEBUG')

PROXIES_COUNT = 1
REAL_IP_HEADER = 'X-Real-IP'
```
