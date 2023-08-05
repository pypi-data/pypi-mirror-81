class FurryAI:
    responses = {
        "greetings": [
            "hello",
            "hey",
            "hi",
            "hewwo",
            "hewo",
            "hai"
        ]
    }

    def __init__(self):
        # Do something here, I don't know?
        pass

    def __startswith_array(self, text, array):
        for i in array:
            if text.lower().split(" ")[0] == i:
                return True
        return False
    
    def respond(self, text):
        if self.__startswith_array(text, self.responses["greetings"]):
            return "hewwo owo"
        else:
            return "Could not respond to this message."
