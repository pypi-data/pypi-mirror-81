from trainingtracker import training_tracker_server
import socket
# TrainingTracker Main Script

def start_server():
    internal_state = {}

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    print("TrainingTracker IP Address: " + str(ip))
    s.close()

    queue = training_tracker_server.start_server()
    return TTServer(queue, internal_state)

class TTServer:
    def __init__(self, queue, internal_state):
        self.queue = queue
        self.internal_state = internal_state\

    def add_scalar(self, tag, value, step):
        '''Add scalar value.\n
        tag (String): The category tag for the value, such as 'loss'
        value (float): The actual value, the "Y-Axis"
        step (int): The global step of the value, the "X-Axis"
        '''
        # Adjust the internal state
        if tag in self.internal_state.keys():
            self.internal_state[tag] += [{"y":value, "x":step}]
        else:
            self.internal_state[tag] = [{"y":value, "x":step}]
        # Update the server process
        self.queue.put_nowait(self.internal_state)

    def add_scalar_list(self, tag, values, steps):
        '''Add a list of scalar values.\n
        tag (String): The category tag for the value, such as 'loss'
        values (float): The list of actual values, the "Y-Axis"
        steps (int): The list of global steps of the values, the "X-Axis"
        '''
        # Adjust the internal state
        if tag in self.internal_state.keys():
            self.internal_state[tag] += [{"y":values[i], "x":steps[i]} for i in range(len(values))]
        else:
            self.internal_state[tag] = [{"y":values[i], "x":steps[i]} for i in range(len(values))]
        # Update the server process
        self.queue.put_nowait(self.internal_state)