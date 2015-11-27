APP_CAPTION = "Red Alert"

winwidth = 800
winheight = 600
gridwidth = 96
gridheight = 47
battlewidth = 600
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
listboxx = 100
listboxy = 50
mousescrollwidth = 30
mapnamex = 684
mapnamey = 100
animationspeed = 1
defaultmapfile = "map0.txt"
mapwidth = 200
mapheight = 200
minimapx = 595
minimapy = 30
barlength = 160
barheight = 10
barx = 50
bary = 150
occupyx = 8
occupyy = 4

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

colorofowner = [RED,BLUE]

loadList = {
	"loadimg":"./img/startimage.png",
	"loadmap":"./img/loadmap.png",
	"menubttn":"./img/mnbttn.png",
	"menu":"./img/menu.png",
	"allyflag":"./img/icons/allyflag.png",
	"ctrlpanel":"./img/ctrlpanel.png",
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
}

defaultplayers = {
	"player0":{
		"flag":0,
		"position":[5,5],
		"initials":[
			{"type":"infantry","name":"E3","pos":(-150,-150)},
			{"type":"infantry","name":"E3","pos":(150,-150)},
			{"type":"infantry","name":"E3","pos":(-150,150)},
			{"type":"infantry","name":"E3","pos":(150,150)},
		],
	},
	"player1":{
		"flag":1,
		"position":[15,15],
		"initials":[
			{"type":"infantry","name":"E3","pos":(-150,-150)},
			{"type":"infantry","name":"E3","pos":(150,-150)},
			{"type":"infantry","name":"E3","pos":(-150,150)},
			{"type":"infantry","name":"E3","pos":(150,150)},
		],
	}
}
