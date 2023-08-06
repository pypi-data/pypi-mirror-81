import logging.config
from typing import Type

from django.utils.log import DEFAULT_LOGGING

from ._base import ComposedConfiguration, ConfigMixin


def _filter_favicon_messages(record):
    if (
        record.name == 'django.request'
        and hasattr(record, 'request')
        and record.request.path == '/favicon.ico'
    ):
        return False

    if record.name == 'django.server' and '/favicon.ico' in str(record.args[0]):
        return False

    return True


class LoggingMixin(ConfigMixin):
    """
    Configure Django logging.

    This requires the `rich` package to be installed.
    """

    # Disable existing Django logging configuration
    LOGGING_CONFIG = None
    LOGGING = None

    @staticmethod
    def before_binding(configuration: Type[ComposedConfiguration]) -> None:
        logging.config.dictConfig(
            {
                'version': 1,
                'disable_existing_loggers': False,
                'formatters': {'rich': {'datefmt': '[%X]'}},
                'handlers': {
                    'console': {
                        'class': 'rich.logging.RichHandler',
                        'formatter': 'rich',
                        'filters': ['filter_favicon_messages'],
                    },
                    'django.server': {
                        'class': 'rich.logging.RichHandler',
                        'formatter': 'rich',
                        'filters': ['filter_favicon_messages'],
                    },
                },
                'loggers': {
                    '': {'level': 'INFO', 'handlers': ['console'], 'propagate': False},
                    'django.server': DEFAULT_LOGGING['loggers']['django.server'],
                },
                'filters': {
                    'filter_favicon_messages': {
                        '()': 'django.utils.log.CallbackFilter',
                        'callback': _filter_favicon_messages,
                    }
                },
            }
        )
