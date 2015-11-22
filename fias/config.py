#coding: utf-8
from __future__ import unicode_literals, absolute_import

import django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_module
from fias.weights import weights

DJ_VERSION = django.VERSION[0] + 10*django.VERSION[1]

_DEFAULT = ('landmark', 'houseint', 'house')

FIAS_TABLES = ['socrbase', 'normdoc', 'addrobj']
FIAS_TABLES.extend([x.lower() for x in list(getattr(settings, 'FIAS_TABLES', _DEFAULT)) if x.lower() in _DEFAULT])


FIAS_DELETED_TABLES = ('addrobj', 'house', 'houseint', 'normdoc')

FIAS_DATABASE_ALIAS = getattr(settings, 'FIAS_DATABASE_ALIAS', 'default')

if FIAS_DATABASE_ALIAS not in settings.DATABASES:
    raise ImproperlyConfigured('FIAS: database alias `{0}` was not found in DATABASES'.format(FIAS_DATABASE_ALIAS))


FIAS_SPHINX_ADDROBJ_INDEX_NAME = getattr(settings, 'FIAS_SPHINX_ADDROBJ_INDEX_NAME', 'addrobj')

FIAS_SPHINX_ADDROBJ_INDEX = FIAS_DATABASE_ALIAS + '_' + FIAS_SPHINX_ADDROBJ_INDEX_NAME

user_weights = getattr(settings, 'FIAS_SB_WEIGHTS', {})
if not isinstance(user_weights, dict):
    raise ImproperlyConfigured('FIAS_SB_WEIGHTS should be a dict type')

weights.update(user_weights)

# Чтобы использовать для данных ФИАС другую базу данных,
# добавьте роутер 'fias.routers.FIASRouter' в список `DATABASE_ROUTERS`

row_filters = getattr(settings, 'FIAS_TABLE_ROW_FILTERS', [])
TABLE_ROW_FILTERS = []
for flt_path in row_filters:
    try:
        flt = import_module(flt_path)
    except ImportError:
        raise ImproperlyConfigured('Table row filter module `{0}` does not exists'.format(flt_path))
    else:
        TABLE_ROW_FILTERS.append(flt)

FIAS_SEARCHD_CONNECTION = {
    'ENGINE': 'django.db.backends.mysql',
    'host': '127.0.0.1',
    'port': 9306,
}
FIAS_SEARCHD_CONNECTION.update(getattr(settings, 'FIAS_SEARCHD_CONNECTION', {}))
