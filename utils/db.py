import json

async def get_db():
    with open("./databases/db.json") as f:
        data = json.load(f)
    
    return data

async def update_db(data):
    try:
        with open("./databases/db.json", 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except:
        return False
    