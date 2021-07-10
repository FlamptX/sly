import json

class Object:
    def __init__(self, **data):
        for key in data.keys():
            if isinstance(data[key], dict):
                setattr(self, key, Object(**data[key]))
            else:
                setattr(self, key, data[key])
    
    @classmethod
    def from_json(cls, fp):
        with open(fp, 'r') as f:
            data = json.loads(f.read())
        
        return cls(**data)
