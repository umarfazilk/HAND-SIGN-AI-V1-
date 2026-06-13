# modules/sentence_builder.py

class SentenceBuilder:
    def __init__(self):
        self.last = ""

    def build(self, word):
        if word == "" or word == self.last:
            return ""

        self.last = word

        if word == "FOOD":
            return "Please give me food"
        if word == "WATER":
            return "I need water"
        if word == "MEDICINE":
            return "I need medicine"
        if word == "REST":
            return "I want to rest"

        return word