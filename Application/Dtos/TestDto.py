import uuid

class TestDto():
    def __init__(self, id: uuid, testText: str):
        self._id = id
        self._testText = testText
        