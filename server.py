import gevent
import zerorpc


class Server(object):
    client_inputs = []

    def get_client_uid(self):
        self.client_inputs.append([[0, 0], [0, 0]])
        return len(self.client_inputs) - 1

    def update_client_data(self, uid, data):
        self.client_inputs[uid] = data
        return True

    def get_client_inputs(self):
        return self.client_inputs


class Client:
    def __init__(self, is_host):
        self.serverclient = zerorpc.Client(timeout=2)
        if is_host:
            self.start_server()

    @staticmethod
    def start_server():
        server = zerorpc.Server(Server())
        server.bind("tcp://0.0.0.0:4242")
        print("Server Started!")
        gevent.spawn(server.run)
