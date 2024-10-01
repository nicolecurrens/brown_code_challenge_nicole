import spacy

class spacy_obj():

    def __init__(self):
        sp = spacy.load("en_core_web_sm")
        self.sp = sp

    def do_ner(self, search_words):
        entities = self.sp(search_words)
        return entities.ents
