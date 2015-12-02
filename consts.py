APP_CAPTION = "Red Alert"

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
barlength = 160
barheight = 10
barx = 50
bary = 150
groupw = 10
grouph = 15
occupyx = 8
occupyy = 4
maxsize = 25

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

colorofplayer = [RED,BLUE]

sizeofunit = {
	"adog":1,
	"E3":1,
	"MCV":6,
	"AirCmd":12,
	"Gcnst":20,
}
modify = {
	"AirCmd":[-50,0],
	"Gcnst":[20,-20],
}

loadList = {
	"loadimg":"./img/startimage.png",
	"loadmap":"./img/loadmap.png",
	"menubttn":"./img/mnbttn.png",
	"menu":"./img/menu.png",
	"allyflag":"./img/icons/allyflag.png",
	"ctrlpanel":"./img/ctrlpanel.png",
	"button00":"./img/icons/button00.png",
	"button01":"./img/icons/button01.png",
	"button02":"./img/icons/button02.png",
	"button03":"./img/icons/button03.png",
	"button04":"./img/icons/button04.png",
	"button06":"./img/icons/button06.png",
	"button09":"./img/icons/button09.png",
	"lspacer":"./img/icons/lspacer.png",
	"lendcap":"./img/icons/lendcap.png",
	"rendcap":"./img/icons/rendcap.png",
	"bttnbkgd":"./img/icons/bttnbkgd.png",
	"credits":"./img/icons/credits.png",
	"top":"./img/icons/top.png",
	"diplobtn":"./img/icons/diplobtn.png",
	"optbtn":"./img/icons/optbtn.png",
	"repairbtn":"./img/icons/repair.png",
	"sellbtn":"./img/icons/sell.png",
	"tabtop":"./img/icons/side1.png",
	"tabbtm":"./img/icons/side3.png",
	"tabbtn0":"./img/icons/tab00.png",
	"tabbtn1":"./img/icons/tab01.png",
	"tabbtn2":"./img/icons/tab02.png",
	"tabbtn3":"./img/icons/tab03.png",
	"sideb":"./img/icons/side2b.png",
	"radar":"./img/icons/radar.png",
	"powerp":"./img/icons/powerp.png",
	"editorpanel":"./img/editorpanel.png",
	"selectmap":"./img/selectmap.png",
	"ground":"./img/ground.png",
	"lightground":"./img/lightground.png",
	"red":"./img/red.png",
	"green":"./img/green.png",
	"bar":"./img/bar.png",
	"bloodbar":"./img/bloodbar.png",
	"buildingbloodbar":"./img/buildingbloodbar.png",
	"listboxbg":"./img/listboxbg.png",
	"listboxbar":"./img/listboxbar.png",
	"aircmd":"./img/Building/aircmd.png",
	"gcnst":"./img/Building/gcnst.png",
	"E3":"./img/Infantry/E3.png",
	"adog":"./img/Infantry/adog.png",
	"mcv":"./img/Vehicle/mcv.png",
	"createGrass":"./img/creat/grass.png",
	"createWater":"./img/creat/water.png",
	"createPower":"./img/creat/ggpowricon.png",
}

requisite = {
	"Power":["Gcnst"],
}

defaultplayers = {
	"player0":{
		"flag":0,
		"position":[5,5],
		"initials":[
			{"name":"E3","pos":(-150,-150),"animation":"standne"},
			{"name":"E3","pos":(150,-150),"animation":"standnw"},
			{"name":"E3","pos":(-150,150),"animation":"standse"},
			{"name":"E3","pos":(150,150),"animation":"standsw"},
			{"name":"Adog","pos":(-150,0),"animation":"standn"},
			{"name":"Adog","pos":(150,0),"animation":"stande"},
			{"name":"Adog","pos":(0,150),"animation":"standw"},
			{"name":"Adog","pos":(0,-150),"animation":"stands"},
		],
	},
	"player1":{
		"flag":1,
		"position":[185,185],
		"initials":[
			{"name":"E3","pos":(-150,-150),"animation":"standne"},
			{"name":"E3","pos":(150,-150),"animation":"standnw"},
			{"name":"E3","pos":(-150,150),"animation":"standse"},
			{"name":"E3","pos":(150,150),"animation":"standsw"},
			{"name":"Adog","pos":(-150,0),"animation":"standn"},
			{"name":"Adog","pos":(150,0),"animation":"stande"},
			{"name":"Adog","pos":(0,150),"animation":"standw"},
			{"name":"Adog","pos":(0,-150),"animation":"stands"},
		],
	}
}
