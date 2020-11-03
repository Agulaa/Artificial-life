from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter


from agents import Snail, Greenfly, Salad, Tomato
from model import Garden

COLORS = {"Greenfly": "#00AA00", "Snail": "#880000", "Salad": "#003330","Tomato": "#330000" }

def garden_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Greenfly:
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5
        portrayal["Layer"] = 0
        portrayal["Filled"]="true"
        portrayal["Color"] = ["#00AA00", "#00AA00"]



    elif type(agent) is Snail:
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5
        portrayal["Layer"] = 0
        portrayal["Filled"]="true"
        portrayal["Color"] = ["#880000", "#880000"]


    elif type(agent) is Salad:
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5
        portrayal["Layer"] = 0
        portrayal["Filled"]="true"
        portrayal["Color"] = ["#003330", "#003330"]

    elif type(agent) is Tomato:
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5
        portrayal["Layer"] = 3
        portrayal["Color"] = ["#330000", "#330000"]

    return portrayal


canvas_element = CanvasGrid(garden_portrayal, 20, 20, 500, 500)
chart = ChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)

model_params = {
    "height": 20,
    "width": 20,

    "initial_tomato": UserSettableParameter(
        "slider", "Initial Tomato Population", 100, 10, 300
    ),
    "initial_salad": UserSettableParameter(
        "slider", "Initial Salad Population", 100, 10, 300
    ),
    "initial_snail": UserSettableParameter(
        "slider", "Initial Snail Population", 100, 10, 300
    ),
    "initial_greenfly": UserSettableParameter(
        "slider", "Initial Greenfly Population", 100, 10, 300
    ),
    "preparation_1": UserSettableParameter(
        "slider", "Preparation_1", 20, 1, 50
    ),
    "preparation_2": UserSettableParameter(
        "slider", "Preparation_2", 20, 1, 50
    ),
    "fermon": UserSettableParameter(
        "slider", "Fermon", 1, 1, 20
    ),
    "steps": UserSettableParameter(
        "slider", "Steps", 20, 1, 50
    ),
    "target": UserSettableParameter(
        "slider", "Target", 20, 1, 50
    )

}
server = ModularServer(
    Garden, [canvas_element, chart], "Garden", model_params
)
server.port = 8521
