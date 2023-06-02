from client_ws import WsClient
import json

ws = WsClient("ws://localhost:8001")

int_lower_bound = [-20, -20]
int_upper_bound = [20, 20]
float_lower_bound = [-20.0, -20.0]
float_upper_bound = [20.0, 20.0]
directions= [-1,-1]
number_of_bits = 10

max_evaluations = 1000

message = {
    # "int": {
    #     "lower_bound": int_lower_bound,
    #     "upper_bound": int_upper_bound,

    # },
    "float": {
        "lower_bound": float_lower_bound,
        "upper_bound": float_upper_bound
    },
    "binary": {
        "number_of_bits": number_of_bits
    },
    "stop_criteria": {  #recibir solo uno de los siguientes criterios de parada
        "max_evaluations": max_evaluations,
        "max_seconds": 0
    },
    "number_of_objectives": 1,
    "directions":directions,
    "population": 100,
    "offspring_population": 100,
    "simulation_periods":100,
    "mutation": {#puede existir o uno o todos los tipos de mutacion 
        # "int": {#si existe este este tipo "int", entonces elegir uno de los tipos de mutacion que se listan, esto sucede para todos los siguientes, tambien en crossover
        #     "IntegerPolynomialMutation": {
        #         "probability": 0.01,
        #         "distribution_index": 20
        #     }
        # },
        "float": {
            "PolynomialMutation": {
                "probability": 0.01,
                "distribution_index": 20
            }
            # ,
            # "SimpleRandomMutation": {
            #     "probability": 0.01
            # },
            # "UniformMutation": {
            #     "probability": 0.01,
            #     "perturbation": 0.5
            # },
            # "NonUniformMutation": { no existe este
            #     "probability": 0.01,
            #     "perturbation": 0.5,
            #     "max_iterations": 100
            # }
        },
        "binary": {
            "BitFlipMutation": {
                "probability": 0.01
            }
        }
        
    },
    "crossover": {
        # "int": {
        #     "IntegerSBXCrossover": {
        #         "probability": 1.0,
        #         "distribution_index": 20
        #     }
        # },
        "float": {
            "SBXCrossover": {
                "probability": 1.0,
                "distribution_index": 20
            },
        },
        "binary": {
            "SPXCrossover": {
                "probability": 1.0
            }
        }
    }


}

json_string = json.dumps({"action": "optimize", "message": message})

print(json_string)
objetives=ws.send_data(json_string)
print(objetives)
