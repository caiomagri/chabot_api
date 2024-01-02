import inject

from app.settings import Settings


def configure_di(binder) -> None:
    # General
    settings = Settings()
    binder.bind(Settings, settings)


def di_inject() -> None:
    inject.configure(configure_di)
