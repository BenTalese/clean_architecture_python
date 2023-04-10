import uuid

class TestDto():
    
    def __init__(self, id: uuid, test_text: str):
        self.id = id
        self.test_text = test_text
        