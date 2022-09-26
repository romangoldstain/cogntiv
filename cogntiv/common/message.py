class Message:
    """
    Donates the common message DTO across the producer and the consumer.
    """
    def __init__(self, seq, payload):
        self.seq = seq
        self.payload = payload
