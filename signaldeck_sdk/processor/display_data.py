import json

from ..context import ApplicationContext

def transform_params(button_data,active, actionhash):
    if "params" in button_data:
        if active:
            if button_data.get("toggleable", False):
                button_data["params"][button_data["button_active_condition"][0]] = not button_data["params"][button_data["button_active_condition"][0]]
        
        button_data["id"] = button_data["name"]+ "_"+str(actionhash)
        button_data["actionhash"] = actionhash
        for p in button_data["params"].keys():
            
            if isinstance(button_data["params"][p], str):
                if button_data["params"][p][0] == "@":
                    button_data["params"][p] = button_data["params"][p]+"_"+str(actionhash)
        button_data["get_params"] = json.dumps(button_data["params"])
    return button_data

class DisplayData:
    def __init__(self,ctx: ApplicationContext,hash):
        self.hash=hash
        self.ctx=ctx
        self.buttons_to_display_cache=None
        
    def t(self, key, **kwargs):
        return self.ctx.t(key, **kwargs)

    def withData(self,data):
        for key in data:
            setattr(self,key,data[key])
        return self

    def getStateChangeButtonData(self):
        res = []
        buttons = self.buttons_to_display()
        for button in buttons.keys():
            res.append(buttons[button])
        return res

    def getStateAsJson(self):
        res={}
        for a in self.getExportFields():
            res[a]=getattr(self,a)
        return res

    def withOffset(self,offset):
        self.offset=offset
        return self

    def getExportFields(self):
        return []
    
    def buttons(self) -> dict:
        return {}
    
    def buttons_to_display(self):
        if self.buttons_to_display_cache:
            return self.buttons_to_display_cache
        self.buttons_to_display_cache= {k: transform_params(v,self.isButtonActive(k), self.hash) for k, v in self.buttons().items()}
        return self.buttons_to_display_cache
    
    def isButtonActive(self,buttonName):
        button = self.buttons().get(buttonName)
        if button and "button_active_condition" in button:
            attr, expected_value = button["button_active_condition"]
            actual_value = getattr(self, attr, None)
            return actual_value == expected_value
        return False
    
    def getCSSClass(self,buttonName):
        if self.isButtonActive(buttonName):
            return " active"
        return ""
    
    def getStatefullFields(self):
        return []

    def getStatefullParams(self):
        res={}
        for a in self.getStatefullFields():
            if hasattr(self, a):
                res[a]=getattr(self,a)
        return json.dumps(res)