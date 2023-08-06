from .io_utils import load_state
from .web import Server
from .io_utils import prepare_state
import os

os.makedirs("data", exist_ok=True)
state_p = "data/unstate.pkl"
if not os.path.exists(state_p):
    prepare_state(state_p)
state = load_state(state_p)
server = Server(state)
server.plot()
server.app.run_server(debug=True)