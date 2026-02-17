from .processor import Processor
from .display_data import DisplayData



def assureBool(val):
    if type(val) is str:
            return val.lower() == "true"
    return val

class DisplayProcessor(Processor):

    def __init__(self,name,config,valueProvider,collect_data):
        super().__init__(name,config,valueProvider,collect_data)
        self._uploaded_file = None
    
    def getTemplate(self,value):
        raise NotImplementedError("Processor must provide a template!")

    def getDisplayData(self,value,actionHash,**kwargs) -> DisplayData:
        return DisplayData(actionHash)

    def getBoolParams(self):
        return []

    def getIntParams(self):
        return []
    
    def getFloatParams(self):
        return []

    def performActions(self,value,actionHash,**kwargs):
        return
    
    def providesState(self,value):
        return True

    def getState(self,value,actionHash,**kwargs):
        if not self.providesState(value):
            return ""
        kwargs= self.processParams(**kwargs)
        data=self.getDisplayData(value,actionHash,**kwargs)
        if data is None:
            return ""
        
        return self.ctx.render(self.getTemplate(value),displayData=data)

    def getAdditionalInfoForClient(self,data:DisplayData):
        return {}

    def processParams(self, **kwargs):
        for boolField in self.getBoolParams():
            if boolField in kwargs and kwargs[boolField] is not None:
                kwargs[boolField]=assureBool(kwargs[boolField])
        for intField in self.getIntParams():
            if intField in kwargs and kwargs[intField] is not None:
                kwargs[intField]=int(kwargs[intField])
        for floatField in self.getFloatParams():
            if floatField in kwargs and kwargs[floatField] is not None:
                kwargs[floatField]=float(kwargs[floatField])
        return kwargs

    def accecptUploadedFile(self,value,actionHash,**kwargs):
        return False

    def getUploadPath(self,value, file ,actionHash,**kwargs):
        return None

    def processFileUpload(self,file,value,actionHash,**kwargs):
        if self.accecptUploadedFile(value,actionHash,**kwargs):
            path = self.getUploadPath(value,file, actionHash,**kwargs)
            if path:
                self.ctx.files.save(file,path)
            self._uploaded_file = file


    def process(self,value,actionHash,file=None,**kwargs):
        self._uploaded_file = None
        kwargs= self.processParams(**kwargs)
        if file:
            self.processFileUpload(file,value,actionHash,**kwargs)
        self.performActions(value,actionHash,**kwargs)
        data=self.getDisplayData(value,actionHash,**kwargs)
        if data is None:
            return {}
        return {"html":  self.ctx.render(self.getTemplate(value),displayData=data),"stateChangeEvents":data.getStateChangeButtonData(),"data":data.getStateAsJson(),**self.getAdditionalInfoForClient(data)}