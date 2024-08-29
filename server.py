import gevent
import zerorpc


class Server(object):
    client_inputs = []
    score = 0
    fireballs = []
    running = True

    def get_client_uid(self):
        self.client_inputs.append([[0, 0], [0, 0]])
        return len(self.client_inputs) - 1

    def update_client_data(self, uid, data):
        self.client_inputs[uid] = data
        return True

    def get_client_inputs(self):
        return self.client_inputs

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score
        return True

    def get_fireballs(self):
        return self.fireballs

    def set_fireball(self, size, direction, speed, start_pos, rotation_direction, position, uid):
        self.fireballs.append([size, direction, speed, start_pos, rotation_direction, position, uid])
        return True

    def update_fireballs(self, positions):
        for fireball, pos in zip(self.fireballs, positions):
            fireball[5] = pos
        return True

    def remove_fireball(self, index):
        self.fireballs.pop(index)
        return True

    def get_running(self):
        return self.running

    def set_running(self, running):
        self.running = running
        return True


class Client:
    def __init__(self, is_host):
        self.serverclient = zerorpc.Client(timeout=2)
        if is_host:
            self.start_server()

    @staticmethod
    def start_server():
        import socket
        ip = socket.gethostbyname(socket.gethostname())
        server = zerorpc.Server(Server())
        server.bind(f"tcp://{ip}:4242")
        print("Your local ip: ", ip)
        print("Server Started!")
        gevent.spawn(server.run)
