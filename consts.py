APP_CAPTION = "Red Alert"

numofplayer = 2
winwidth = 800
winheight = 600
gridwidth = 96
gridheight = 47
battlewidth = 640
battleheight = 570
scrollspeed = 15
optionheight = 20
boxwidth = 300
boxheight = 500
boxpad = 5
menubuttonx = 634
menubuttony = 270
colorbuttonx = 600
colorbuttony = 270
gamectrlbuttonx = 50
gamectrlbuttony = 568
lendcapx = 20
lendcapy = 568
rendcapx = 604
rendcapy = 568
bttnbkgdx = 50
bttnbkgdy = 568
listboxx = 100
listboxy = 50
mousescrollwidth = 10
mapnamex = 684
mapnamey = 100
creditx = 632
credity = 0
topx = 632
topy = 16
diplobtnx = 644
diplobtny = 16
repairbtnx = 652
repairbtny = 146
radarx = 632
radary = 44
tabbtnx = 659
tabx = 632
taby = 154
createbtnboxx = 632
createbtnboxy = 223
createbtnx = 656
createbtny = 223
createbtnw = 60
createbtnh = 48
createn = 7
animationspeed = 1
defaultmapfile = "map0.txt"
mapwidth = 200
mapheight = 200
minimapx = 644
minimapy = 48
minimapw = 142
minimaph = 110
powerx = 632
powery = 568
powern = 172
powerthresh = 20
barlength = 160
barheight = 10
barx = 50
bary = 150
groupw = 10
grouph = 15
occupyx = 8
occupyy = 4
maxsize = 25
createspeed = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

colorofplayer = [RED, BLUE]

sizeofunit = {
    "Adog": 1,
    "Engineer": 1,
    "E3": 1,
    "MCV": 6,
    "Power": 10,
    "Gpile": 10,
    "Grefn": 12,
    "AirCmd": 12,
    "Gcnst": 20,
    "Gyard": 20,
    "Gweap": 12,
    "Gpill": 6,
}
fullHPofunit = {
    "Adog": 100,
    "Engineer": 100,
    "E3": 100,
    "MCV": 3000,
    "Power": 1000,
    "Gpile": 1000,
    "Grefn": 2000,
    "AirCmd": 1000,
    "Gcnst": 3000,
    "Gyard": 1500,
    "Gweap": 1000,
    "Gpill": 400,
}
powerofbuilding = {
    "Power": 200,
    "Gpile": -25,
    "Grefn": -35,
    "AirCmd": -25,
    "Gcnst": 0,
    "Gyard": -25,
    "Gweap": -25,
    "Gpill": 0,
}
modify = {
    "Power": [0, 24],
    "Grefn": [0, 54],
    "Gpile": [-28, 11],
    "AirCmd": [-50, 0],
    "Gcnst": [20, -20],
    "Gyard": [0, 0],
    "Gpill": [0, 0],
    "Gweap": [0, -10],
}
typeofunit = {
    "Adog": "infantry",
    "Engineer": "infantry",
    "E3": "infantry",
    "MCV": "vehicle",
    "Power": "building",
    "Gpile": "building",
    "Grefn": "building",
    "AirCmd": "building",
    "Gyard": "building",
    "Gweap": "building",
    "Gcnst": "building",
    "Gpill": "defence",
}
costofunit = {
    "Adog": 200,
    "Engineer": 500,
    "E3": 100,
    "MCV": 3000,
    "Power": 800,
    "Grefn": 2000,
    "Gpile": 500,
    "AirCmd": 1000,
    "Gyard": 1000,
    "Gweap": 2000,
    "Gpill": 500,
    "Gcnst": 3000,
}
canland = {
    "Adog": True,
    "Engineer": True,
    "E3": True,
    "MCV": True,
    "Power": True,
    "Grefn": True,
    "Gpile": True,
    "AirCmd": True,
    "Gyard": False,
    "Gweap": True,
    "Gpill": True,
    "Gcnst": True,
}
canwater = {
    "Adog": False,
    "Engineer": False,
    "E3": False,
    "MCV": False,
    "Power": False,
    "Grefn": False,
    "Gpile": False,
    "AirCmd": False,
    "Gyard": True,
    "Gweap": False,
    "Gpill": False,
    "Gcnst": False,
}
requisite = {
    "Power": ["Gcnst"],
    "Grefn": ["Gcnst", "Power"],
    "Gpile": ["Gcnst", "Power"],
    "AirCmd": ["Gpile", "Gcnst", "Grefn"],
    "Gyard": ["Gpile", "Gcnst", "Grefn"],
    "Gweap": ["Gpile", "Gcnst", "Grefn"],
    "Gpill": ["Gpile", "Gcnst"],
    "E3": ["Gpile"],
    "Adog": ["Gpile"],
    "Engineer": ["Gpile", "Grefn"],
    "MCV": ["Gweap"],
}
createPosition = {
    "Gpile": (-50, 50),
    "Gweap": (100, 50),
}
createAnimation = {
    "E3": "runsw",
    "Adog": "runsw",
    "Engineer": "runsw",
    "MCV": "runse",
}
pointerset = {
    "Power": [(0, 0), (-1, 1), (1, 1), (0, 1)],
    "Grefn": [(0, 0), (-1, 1), (1, 1), (0, 1),
              (-2, 1), (-1, 2), (0, 2), (1, 2), (2, 1)],
    "Gpile": [(0, 0), (-1, 1), (1, 1), (0, 1), (-1, 0), (-2, 0)],
    "AirCmd": [(0, 0), (-1, 1), (1, 1), (0, 1), (-1, 0), (-2, 0)],
    "Gyard": [(0, 0), (0, -1), (-1, 0), (1, 0), (-2, 0), (2, 0),
              (-3, 1), (-1, 1), (1, 1), (3, 1),
              (-2, 1), (0, 1), (2, 1), (-1, 2), (1, 2), (0, 2)],
    "Gweap": [(0, 0), (0, -1), (-1, 0), (1, 0), (-2, 0), (2, 0),
              (-1, 1), (1, 1), (3, 1), (0, 1), (2, 1), (1, 2)],
    "Gpill": [(0, 0)],
}
allbuildings = [
    "Power", "Grefn", "Gpile", "AirCmd", "Gweap", "Gyard",
]
alldefences = [
    "Gpill",
]
allinfantries = [
    "E3", "Adog", "Engineer",
]
allvehicles = [
    "MCV",
]
allunits = {
    "building": allbuildings,
    "defence": alldefences,
    "infantry": allinfantries,
    "vehicle": allvehicles,
}

loadList = {
    "loadimg": "./img/startimage.png",
    "loadmap": "./img/loadmap.png",
    "menubttn": "./img/mnbttn.png",
    "menu": "./img/menu.png",
    "allyflag": "./img/icons/allyflag.png",
    "ctrlpanel": "./img/ctrlpanel.png",
    "button00": "./img/icons/button00.png",
    "button01": "./img/icons/button01.png",
    "button02": "./img/icons/button02.png",
    "button03": "./img/icons/button03.png",
    "button04": "./img/icons/button04.png",
    "button06": "./img/icons/button06.png",
    "button09": "./img/icons/button09.png",
    "lspacer": "./img/icons/lspacer.png",
    "lendcap": "./img/icons/lendcap.png",
    "rendcap": "./img/icons/rendcap.png",
    "bttnbkgd": "./img/icons/bttnbkgd.png",
    "credits": "./img/icons/credits.png",
    "top": "./img/icons/top.png",
    "diplobtn": "./img/icons/diplobtn.png",
    "optbtn": "./img/icons/optbtn.png",
    "repairbtn": "./img/icons/repair.png",
    "sellbtn": "./img/icons/sell.png",
    "tabtop": "./img/icons/side1.png",
    "tabbtm": "./img/icons/side3.png",
    "tabbtn0": "./img/icons/tab00.png",
    "tabbtn1": "./img/icons/tab01.png",
    "tabbtn2": "./img/icons/tab02.png",
    "tabbtn3": "./img/icons/tab03.png",
    "sideb": "./img/icons/side2b.png",
    "radar": "./img/icons/radar.png",
    "powerp": "./img/icons/powerp.png",
    "progress": "./img/icons/ambttn.png",
    "editorpanel": "./img/editorpanel.png",
    "selectmap": "./img/selectmap.png",
    "ground": "./img/ground.png",
    "lightground": "./img/lightground.png",
    "red": "./img/red.png",
    "green": "./img/green.png",
    "black": "./img/creat/black.png",
    "bar": "./img/bar.png",
    "bloodbar": "./img/bloodbar.png",
    "buildingbloodbar": "./img/buildingbloodbar.png",
    "listboxbg": "./img/listboxbg.png",
    "listboxbar": "./img/listboxbar.png",
    "aircmd": "./img/Building/aircmd.png",
    "gcnst": "./img/Building/gcnst.png",
    "power": "./img/Building/ggpowr.png",
    "grefn": "./img/Building/ggrefn.png",
    "gpile": "./img/Building/ggpile.png",
    "gyard": "./img/Building/ggyard.png",
    "gweap": "./img/Building/ggweap.png",
    "gpill": "./img/Building/ggpill.png",
    "E3": "./img/Infantry/E3.png",
    "adog": "./img/Infantry/adog.png",
    "engineer": "./img/Infantry/engineer.png",
    "mcv": "./img/Vehicle/mcv.png",
    "createGrass": "./img/creat/grass.png",
    "createWater": "./img/creat/water.png",
    "createPower": "./img/creat/ggpowricon.png",
    "createGrefn": "./img/creat/reficon.png",
    "createGpile": "./img/creat/brrkicon.png",
    "createE3": "./img/creat/e3icon.png",
    "createAdog": "./img/creat/adogicon.png",
    "createEngineer": "./img/creat/engnicon.png",
    "createMCV": "./img/creat/mcvicon.png",
    "createAirCmd": "./img/creat/heliicon.png",
    "createGyard": "./img/creat/ayaricon.png",
    "createGweap": "./img/creat/gwepicon.png",
    "createGpill": "./img/creat/pillicon.png",
}

defaultplayers = {
    "player0": {
        "flag": 0,
        "position": [10, 10],
        "initials": [
            {"name": "E3", "pos": (-150, -150), "animation": "standne"},
            {"name": "E3", "pos": (
                150, -150), "animation": "standnw"},
            {"name": "E3", "pos": (-150, 150),
             "animation": "standse"},
            {"name": "E3", "pos": (
                150, 150), "animation": "standsw"},
            {"name": "Adog",
             "pos": (-150, 0), "animation": "standn"},
            {"name": "Adog", "pos": (
                150, 0), "animation": "stande"},
            {"name": "Adog", "pos": (
                0, 150), "animation": "standw"},
            {"name": "Adog", "pos": (
                0, -150), "animation": "stands"},
        ],
    },
    "player1": {
        "flag": 1,
        "position": [185, 185],
        "initials": [
            {"name": "E3", "pos": (-150, -150), "animation": "standne"},
            {"name": "E3", "pos": (
                150, -150), "animation": "standnw"},
            {"name": "E3", "pos": (-150, 150),
             "animation": "standse"},
            {"name": "E3", "pos": (
                150, 150), "animation": "standsw"},
            {"name": "Adog",
             "pos": (-150, 0), "animation": "standn"},
            {"name": "Adog", "pos": (
                150, 0), "animation": "stande"},
            {"name": "Adog", "pos": (
                0, 150), "animation": "standw"},
            {"name": "Adog", "pos": (
                0, -150), "animation": "stands"},
        ],
    }
}
