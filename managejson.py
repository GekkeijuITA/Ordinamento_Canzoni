import json

def addArtistToJson(name,country,fileName="artists.json"):
    with open(fileName,'r+') as file:
        file_data = json.load(file)
        alreadyIn = False
        for tuple in file_data["artists"]:
            if tuple["name"] == name:
                alreadyIn = True
                break
        if not alreadyIn:
            file_data["artists"].append({"name":name,"area":country})
            file.seek(0)
            json.dump(file_data,file,indent=4,ensure_ascii=False)

s = "io2nonsopiùchefarelooooooool"

addArtistToJson("io2","boh")

addArtistToJson("lui2","marocchino")

file = open("artists.json")
data = json.load(file)

print("Io2" in s)

file.close()