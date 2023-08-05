from trainingtracker import training_tracker_server
import socket
# TrainingTracker Main Script

internal_state = {}

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
print("TrainingTracker IP Address: " + str(ip))
s.close()

queue = training_tracker_server.start_server()

def add_scalar(tag, value, step):
    '''Add scalar value.\n
    tag (String): The category tag for the value, such as 'loss'
    value (float): The actual value, the "Y-Axis"
    step (int): The global step of the value, the "X-Axis"
    '''
    # Adjust the internal state
    if tag in internal_state.keys():
        internal_state[tag] += [{"y":value, "x":step}]
    else:
        internal_state[tag] = [{"y":value, "x":step}]
    # Update the server process
    queue.put_nowait(internal_state)

def add_scalar_list(tag, values, steps):
    '''Add a list of scalar values.\n
    tag (String): The category tag for the value, such as 'loss'
    values (float): The list of actual values, the "Y-Axis"
    steps (int): The list of global steps of the values, the "X-Axis"
    '''
    # Adjust the internal state
    if tag in internal_state.keys():
        internal_state[tag] += [{"y":value[i], "x":step[i]} for i in range(len(values))]
    else:
        internal_state[tag] = [{"y":value[i], "x":step[i]} for i in range(len(values))]
    # Update the server process
    queue.put_nowait(internal_state)