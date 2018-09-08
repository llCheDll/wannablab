import lya

from pathlib import Path

PROJECT_DIR = Path(__file__).parent.as_posix()

settings_default = Path(PROJECT_DIR, 'configs', 'settings.default.yaml')
settings_local = Path(PROJECT_DIR, 'configs', 'settings.local.yaml')


class SettingNotDefinedError(Exception):
    pass


class BaseSettings:
    __slots__ = ('_settings', )

    def __getattr__(self, key):
        try:
            return self._settings.__getattr__(key)
        except KeyError:
            raise SettingNotDefinedError('Setting {} is not defined'.format(key))

    def __contains__(self, item):
        return item in self._settings


class Settings(BaseSettings):
    def __init__(self):
        self._settings = lya.AttrDict.from_yaml(settings_default.as_posix())
        if settings_local.exists():
            self._settings.update_yaml(settings_local.as_posix())


settings = Settings()
