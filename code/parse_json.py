import json

class jsonUtils:
    @staticmethod
    def add(data: dict, file: str = "user-data.json"):
        with open(file) as f:
            original_data: dict = json.load(f)
        
        modified_data = original_data | data # add data to original_data. Information in data will override original
        # print(modified_data)
        with open(file, "w") as f:
            f.write(json.dumps(modified_data, indent=4))
            
    @staticmethod
    def clearfile(file: str = "user-data.json"):
        with open(file, "w") as f:
            f.write("{}")


def main():
    j = jsonUtils
    j.clearfile()
    j.add({"name": "Bob"})
    j.add({"age": 2})
            

if __name__ == "__main__":         
    main()