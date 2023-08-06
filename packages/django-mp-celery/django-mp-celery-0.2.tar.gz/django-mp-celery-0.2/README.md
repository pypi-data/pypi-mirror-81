# MP-celery

Django celery app.

### Installation

Install with pip:

```
pip install django-mp-celery
```

core/\_\_init\_\_.py
``` 
from core.celery_app import celery_app
 
 
__all__ = ['celery_app']
```

core/celery_app.py

```
import cbsettings
 
from celery import Celery
 
 
cbsettings.configure('core.settings.Settings')
 
celery_app = Celery('core')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
```

core/common_settings.py
```
from mpcelery.settings import CelerySettings
```
