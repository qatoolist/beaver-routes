import logging
from typing import Optional

from beaver_routes.core.route import Route


logger = logging.getLogger(__name__)


class BaseScenario:
    def __init__(self) -> None:
        self._route: Optional[Route] = None

    @property
    def route(self) -> Route | None:
        return self._route

    @route.setter
    def route(self, route: Route) -> None:
        if not isinstance(route, Route):
            error_message = f"route should be of type 'Route', not '{type(route)}'"
            logger.error(error_message)
            raise ValueError(error_message)
        self._route = route

class Scenario(BaseScenario):
    pass