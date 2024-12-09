import os
import colorlog
from .environment import BASE_DIR

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} | {asctime} | {module} | {process:d} | {thread:d} : {message}",
            "style": "{",
        },
        "simple": {
            "format": "{log_color}{levelname} | {message}",
            "style": "{",
            "()": "colorlog.ColoredFormatter",
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        },
        "development": {
            "format": "{log_color}[- {levelname} | {pathname} | {lineno} | {asctime} -] = {message}",
            "style": "{",
            "()": "colorlog.ColoredFormatter",
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        }
    },
    "filters": {
        # "special": {
        #     "()": "project.logging.SpecialFilter",
        #     "foo": "bar",
        # },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "verbose",
            "filename": os.path.join(BASE_DIR / "logs/logs.log"),
        },
        "custom_console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "development",
        },
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            # "filters": ["special"],
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "propagate": True,
        },
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
        "debugger": {
            "handlers": ["custom_console", "file"],
            "level": "DEBUG",
            # "filters": ["special"],
        },
    },
}
