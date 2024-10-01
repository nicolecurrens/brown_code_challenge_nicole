import spacy

class spacy_obj():

    def __init__(self):
        # en_core_web_sm is the basic English model for spacy
        sp = spacy.load("en_core_web_sm")
        self.sp = sp

    def do_ner(self, search_words):
        # spacy object automatically processes named entities on the string
        # we can return the entites by accessing .ents
        entities = self.sp(search_words)
        return entities.ents
