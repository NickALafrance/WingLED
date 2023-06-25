class WebEvent:
    def __init__(self, req):
        self.method = req.method
        self.path = req.path
        self.requestData = req.form
        self.modelData = None
        self.responseData = { "OK": True }

    def isRead(self):
        return self.method == 'GET'
    def isWrite(self):
        return self.method == 'POST' or self.method == 'PUT'

    def getIdFromPath(self):
        pieces = self.path.split('/')
        if len(pieces) > 2:
            return int(pieces[2])
        return False
    
    def getSecondIdFromPath(self):
        pieces = self.path.split('/')
        if len(pieces) > 4:
            return int(pieces[4])
        return False
