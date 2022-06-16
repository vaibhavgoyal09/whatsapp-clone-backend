from tortoise.contrib.fastapi import register_tortoise

from app.core.config import settings


TORTOISE_ORM = {
    "connections": {"default": f'{settings.DATABASE_URI}'},
    "apps": {
        "models": {
            "models":
            ["data.model.user", "data.model.status", "data.model.chat",
                "data.model.message", "data.model.group", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def init_db(app):
    register_tortoise(
        app,
        db_url=str(settings.DATABASE_URI),
        modules={
            "models":
            ["data.model.user", "data.model.status", "data.model.chat",
                "data.model.message", "data.model.group"]
        },
        generate_schemas=False,
        add_exception_handlers=False
    )
