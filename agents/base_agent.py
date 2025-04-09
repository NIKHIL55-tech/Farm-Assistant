import logging
logging.basicConfig(filename='logs/system.log', level=logging.INFO)

class BaseAgent:
    def __init__(self, name):
        self.name = name

    def send_message(self, receiver, message):
        logging.info(f"{self.name} ➡️ {receiver.name}: {message}")
        receiver.receive_message(self, message)

    def receive_message(self, sender, message):
        logging.info(f"{self.name} ⬅️ {sender.name}: {message}")
        self.process_message(sender, message)

    def process_message(self, sender, message):
        raise NotImplementedError("You need to implement this method")
