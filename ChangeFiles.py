import UnityPy
from PIL import Image
import os
from tkinter import Tk
from tkinter.filedialog import askdirectory
from console import Main as ConsoleClass

Console = ConsoleClass()
Console.showLogo()
DataPath = askdirectory(title='Bazooka GameData folder')
DataPath += "/data.unity3d"

if not os.path.exists("./Replacements"):
    os.mkdir("Replacements")
    Console.output(Console.Types.Info, "Replacements folder was created!")
else:
    Console.output(Console.Types.Info, "Replacements folder exists, searching for files...")

Replacements = {}
AllowedTypes = ["png", "jpg", "jpeg"]
Patched = 0
files = os.listdir("./Replacements")
for file in files:
    Name = file.split(".")[0]
    Type = file.split(".")[1]
    if not Type in AllowedTypes:
        Console.output(Console.Types.Warning, f".{Type} is not a valid image type!")
        continue
    FilePath = "Replacements/" + file
    Replacements[Name] = FilePath
MaxPatched = len(Replacements)

UnityData = UnityPy.load(DataPath)

for Object in UnityData.objects:
    try:
        if Object.type.name == "Sprite":
            if Patched == MaxPatched:
                break
            Sprite = Object.read()
            
            if Sprite.m_Name in Replacements:
                Texture = Sprite.m_RD.texture.read()
                rect = Sprite.m_RD.textureRect

                NewImage = Image.open(Replacements[Sprite.m_Name]).convert("RGBA")
                NewImage = NewImage.resize((int(rect.width), int(rect.height)), Image.LANCZOS)
        
                Texture.image = NewImage
                Texture.save()
                Patched += 1
    except Exception as e:
        Console.output(Console.Types.Warning, f"{e}") 

if MaxPatched != 0 and MaxPatched == Patched:
    Console.output(Console.Types.Success, "All files were patched!!")
elif MaxPatched > 0:
    Console.output(Console.Types.Error, f"Only {Patched}/{len(Replacements.keys())} were patched! Maybe the files dosen't exist?")
else:
    Console.output(Console.Types.Warning, f"No files were found in the replacements folder!")

with open(DataPath, "wb") as f:
    f.write(UnityData.file.save())