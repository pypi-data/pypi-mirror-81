from abc import ABCMeta, abstractmethod
from typing import Callable, Dict

from logzero import logger
from pdchaos.middleware.core import call_repeatedly
from pdchaos.middleware.core.config import AppConfig


class AttackLoader(metaclass=ABCMeta):
    """
    This class is a base class for implementing different type of attack config loaders.

    For example, different loaders implementation can load an attack configuration from a file, network or other source.
    The loading mechanism depends on the configured settings.
    """
    _cancel_synch_operation = None
    _set_attacks_action_func = None

    @abstractmethod
    def is_allowed_to_call_endpoint(self):
        """ Checks whether the loader is allowed to call the endpoint, e.g. when all parameters are set. """
        pass

    def load(self, set_attacks_action_func: Callable[[Dict], None]):
        """ Load function. Call callback function to set new attack actions.  """
        if self.is_allowed_to_call_endpoint():
            interval = 30
            cancel_future_calls, future = call_repeatedly(interval, self.run, set_attacks_action_func)
            self._cancel_synch_operation = cancel_future_calls
            self._set_attacks_action_func = set_attacks_action_func
            future.add_done_callback(self.safe_guard)
        else:
            logger.warn('Is not allowed to call the endpoint')

    @abstractmethod
    def run(self, set_attacks_action_func: Callable[[Dict], None]):
        """ Load function. Call callback function to set new attack actions.  """
        pass

    def safe_guard(self, future):
        """"Safe guard: In case of unforeseen events, we cancel the thread's synchronize operation and
            reset the attack configuration"""
        try:
            future.result()
        except Exception as e:
            logger.warn("Cancelling synchronize operation with the chaos middleware. Reason: %s" % str(e))
            if self._cancel_synch_operation:
                self._cancel_synch_operation()
                logger.debug("Cancelled synchronize operation")
                self._cancel_synch_operation = None
            else:
                logger.debug("Unable to cancel synchronize operation")
            self.unload_actions()

    def unload_actions(self):
        self._set_attacks_action_func([])
        logger.debug("Unload attack actions")


def init(loaded_app_config, set_attack_action) -> AttackLoader:
    """Init the loader"""
    provider = loaded_app_config.get(AppConfig.ATTACK_LOADER, "proofdock")

    loader = _create_loader(loaded_app_config, provider)
    loader = _setup_loader(loader, set_attack_action)

    return loader


def _setup_loader(loader, set_attack_action):
    if loader and loader.is_allowed_to_call_endpoint():
        loader.load(set_attack_action)

    else:
        logger.info("Missing configuration for the provided loader. Only HEADER types attack will be accepted.")
        loader = None
    return loader


def _create_loader(loaded_app_config: AppConfig, provider: str):
    if provider == "proofdock":
        from pdchaos.middleware.core.proofdock.loader import ProofdockAttackLoader
        loader = ProofdockAttackLoader(loaded_app_config)

    else:
        logger.warning(
            "Unable to find an attack loader provider '{}'. "
            "Please set a valid CHAOS_MIDDLEWARE_ATTACK_LOADER, e.g. 'proofdock'".format(provider))
        loader = None
    return loader
