import threading


class VectorFaucet:
    """
    Responsible for constantly creating new vectors and posting them to provided message bus.
    The faucet suspends when the bus cannot accept newly generated vectors.
    """

    def __init__(self, vector_factory, bus):
        self.vector_factory = vector_factory
        self.bus = bus
        self.running = False

    def start(self):
        if self.running:
            return
        
        self.running = True
        th = threading.Thread(target=self.keep_em_running, daemon=True, args=())
        th.start()
        return th

    def stop(self):
        self.running = False

    def keep_em_running(self):
        while self.running:
            vector = self.vector_factory.create()
            self.bus.put(vector)
