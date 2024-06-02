from beaver_routes.core.scenario import BaseScenario


class PongScenarios(BaseScenario):
    def group_scenario(self, request_args) -> None:
        request_args.params.userDetails = {"DOB": "01/01/2011"}
