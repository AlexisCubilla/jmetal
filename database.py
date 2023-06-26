import json
import requests

from data import Data


class Database:
    def __init__(self):
        self.url = "http://sim.cybiraconsulting.local:3001"


    def get_scenario(self, project_id, scenario_id):
        data = {
            "method": "POST",
            "action": "get_scenario_model",
            "project_id": project_id,
            "scenario_id": scenario_id
        }
        response = requests.post(self.url, json=data)

        if response.status_code == 200:
            result = response.text
        else:
            result = None
        return result


    def save_scenario(self, scenario, result):
        parsed_scenario = json.loads(scenario)
        variables_n = []
        variables = []


        variables_n = [self.create_variable_object(variable, value, True)
               for uuid, value in result.items()
               for node in parsed_scenario["nodes"]
               for variable in node["variables"]
               if variable["id"] == uuid]
            
        variables = [self.create_variable_object(variable, value, False)
             for uuid, value in result.items()
             for node in parsed_scenario["nodes"]
             for dmn_i in node["dmn_i"]
             for variable in dmn_i["variables"]
             if variable["id"] == uuid]

        
        for var_list, variable_type in [(variables_n, "variables_n"), (variables, "variables")]:
            if var_list:
                message = {
                    "method": "POST",
                    "action": "save_"+variable_type,
                    variable_type: var_list
                }
                response = requests.post(self.url, json=message)


    def create_variable_object(self, variable, value, is_global_variable) -> dict:
        # Set the expression of the variable to the given value
        variable["businessObject"]["expression"] = value
        # Use a ternary operator to assign the parent key based on the global flag
        parent = "node_id" if is_global_variable else "dmn_id"
        return {
            "id": variable["id"],
            parent: variable[parent],
            "metadata": {
                "businessObject": variable["businessObject"]
            }
        }
