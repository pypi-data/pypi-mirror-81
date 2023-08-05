import json

class connect:
    def __init__(self, name, *, path=""):
        self.name = name
        self.path = path

        try:
            r = open(f"{self.path}{self.name}.cuprite", "r").read()
        except FileNotFoundError:
            w = open(f"{self.path}{self.name}.cuprite", "w+").write("{}")
            r = open(f"{self.path}{self.name}.cuprite", "r").read()

        self.database = json.loads(r)


    def get(self, *, printf=False):
        if printf: print(self.database)
        return self.database

    def save(self):
        return json.dump(self.database, open(f"{self.path}{self.name}.cuprite", "w+"), indent=4)

    def get_item(self, key, *, printf=False):
        if type(key) is str:
            if printf: print(self.database[key])
            return self.database[key]
        else:
            keys = ""
            for i in range(key.__len__()):
                keys += f"[\"{key[i]}\"]"
            if printf: print(eval(f"self.database{keys}"))
            return eval(f"self.database{keys}")


    def set_item(self, key, value):
        if type(key) is str:
            self.database[key] = value
        else:
            keys = ""
            for i in range(key.__len__()):
                keys += f"[\"{key[i]}\"]"
            exec(f"self.database{keys} = value")
