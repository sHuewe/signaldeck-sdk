import asyncio
import pandas as pd
import logging
from typing import List 
from pathlib import Path
from ..cmd import Cmd
from ..value_provider import ValueProvider
from ..context import ApplicationContext

class Processor:

    def __init__(self,name,config,valueProvider,collect_data):
        self.config=config
        self.cachedFiles={}
        self.ctx=None
        self.name=name
        self.className=None
        self.collect_data=collect_data
        self.valueProvider: ValueProvider =valueProvider
        self.logger=logging.getLogger(__name__)
        self.valueProvider.registerProcessor(self,config.get("export",None))

    def init(self,ctx: ApplicationContext):
        self.ctx=ctx
        
    def withClassName(self,className):
        self.className=className
        return self

    def get_asyncio_tasks(self,collect_data) -> List[asyncio.Future]:
        return []

    def process(self,value,actionHash,file=None,**params):
        raise NotImplementedError("to be implemented")

    def must_be_queued(self):
        if "queued" not in self.config:
            return False
        return self.config["queued"]


    def getState(self,value,actionHash):
        return ""

    def getValue(self,fieldName):
        if hasattr(self,fieldName):
            return getattr(self,fieldName)
        return None

    def getMethodValue(self, methodName,*args,**kwargs):
        return getattr(self,methodName)(*args,**kwargs)
    
    def shutdown(self):
        pass


    def registerCommands(self, cmd: Cmd):
        return


    def refresh(self):
        if "values" in self.config:
            for val in self.config["values"]:
                if val["type"]=="field":
                    setattr(self,val["name"],self.valueProvider.getValue(val["from"]))
                if val["type"]=="method":
                    argrs = val.get("args",[])
                    params= val.get("params",{})
                    setattr(self,val["name"],self.valueProvider.getMethodValue(val["from"],*argrs,**params))
        if "methods" in self.config:
            for method in self.config["methods"]:
                setattr(self,method["name"],self.valueProvider.methods[method["from"]][1])