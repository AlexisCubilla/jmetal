import json
from websockets.sync.client import connect
def minimizar(valores):
    # Asume que valores es una lista de dos elementos
    # Retorna
    return (valores[0]**2 - valores[1]**2)

def maximizar(valores):
    # Asume que valores es una lista de dos elementos
    # Retorna la suma de los dos valores, buscando maximizar esta suma
    return 2* valores[0] + 3*valores[1]


with connect("ws://localhost:8002", open_timeout=None, close_timeout=None) as websocket:
    message = {
    "type": "optimization",
    "max_evaluations": 2000,
    "extra_evaluations": 1000,
    "population": 4,
    "offspring_population": 2,
    "number_of_objectives": 1,
    "periods": 1,
    "iterations": 1,
    "outputs":[
        {
            "id": "1",
            "objective": "minimize",
        },
        {
            "id": "2",
            "objective": "maximize",
        }
    ],
    "inputs":[
        # {
        #     "id": "0", 
        #     "type": "binary",
        # },
        #    {
        #     "id": "00", 
        #     "type": "binary",
        # },
        # {
        #     "id": "1",
        #     "type": "integer",
        #     "lowerBound": 0,
        #     "upperBound": 10
        # },
         {
            "id": "1",
            "type": "integer",
            "lowerBound": 0,
            "upperBound": 10   
        },
            {
            "id": "2",
            "type": "float",
            "lowerBound": 0.0,
            "upperBound": 10.0    
        }
    ],
 
    },
    
    json_string = json.dumps(message)


    print(json_string)
    websocket.send(str(json_string))
    while True:
        message = websocket.recv()
        parsed_message = json.loads(message)
        try:
            action = parsed_message.get("action")
        except:
            action = None
        if action == "simulate":
            valores = [float(parsed_message["message"]["variables"]["values"][0]), float(parsed_message["message"]["variables"]["values"][1])]
            print("Valores recibidos: ", valores)
            resultado_minimizar = minimizar(valores)
            resultado_maximizar = maximizar(valores)
            reply = {
                "result": {
                    "uuids": ["1","2"],
                    "values": [resultado_minimizar, resultado_maximizar]
                }
            }
            websocket.send(str(json.dumps(reply)))
        else:
            print("Mensaje recibido: ", parsed_message)
            break
        
    