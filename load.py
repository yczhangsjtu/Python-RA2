from pylash.ui import LoadingSample
from pylash.text import TextField, TextFormatWeight
from pylash.utils import stage
from pylash.display import RadialGradientColor, Graphics, Loader, Bitmap, BitmapData

class RA2Loading(LoadingSample):
	def __init__(self, **opt):
		super(RA2Loading, self).__init__(None)
		
		loader = Loader()
		loader.load("./img/glsl.png")
		self.background.addChild(Bitmap(BitmapData(loader.content)))

		opt["fontSize"] = stage.height * 0.2
		opt["vacantColor"] = "white"

		txt = TextField()
		txt.size = opt["fontSize"]
		txt.text = "Loading..."
		txt.textColor = opt["vacantColor"]
		txt.weight = TextFormatWeight.BOLD
		txt.x = (stage.width - txt.width) / 2
		txt.y = (stage.height - txt.height) / 2 + 30
		self.progressBar.addChild(txt)

		self.progressBarTotalWidth = txt.width
		self.progressBarHeight = txt.height

		opt["progressColor"] = RadialGradientColor(txt.width / 2, txt.height / 2, txt.width / 2)
		opt["progressColor"].addColorStop(0, "red");  
		opt["progressColor"].addColorStop(0.3, "orange")
		opt["progressColor"].addColorStop(0.4, "yellow")
		opt["progressColor"].addColorStop(0.5, "green")
		opt["progressColor"].addColorStop(0.8, "blue")
		opt["progressColor"].addColorStop(1, "violet")
		self.progressColor = opt["progressColor"]

		self.__coverTxt = TextField()
		self.__coverTxt.x = txt.x
		self.__coverTxt.y = txt.y
		self.__coverTxt.weight = txt.weight
		self.__coverTxt.size = opt["fontSize"]
		self.__coverTxt.text = txt.text
		self.__coverTxt.textColor = opt["progressColor"]
		self.__coverTxt.mask = Graphics()
		self.progressBar.addChild(self.__coverTxt)

		self.__coverTxt.mask.beginFill()
		self.__coverTxt.mask.drawRect(0, 0, 0, 0)
		self.__coverTxt.mask.endFill()

		self.label = TextField()
		self.label.text = "0%"
		self.label.textColor = "blue"
		self.label.size = 40
		self.label.x = (stage.width - self.label.width) / 2
		self.label.y = (stage.height - self.label.height) / 2 - 60
		self.addChild(self.label)
	
	def setProgress(self, value):
		ratio = value / 100
		totalWidth = self.progressBarTotalWidth

		self.label.text = "%s%%" % round(value)
		self.label.x = (stage.width - self.label.width) / 2

		self.__coverTxt.mask.clear()
		self.__coverTxt.mask.beginFill()
		self.__coverTxt.mask.drawRect(0, 0, totalWidth * ratio, self.progressBarHeight)
		self.__coverTxt.mask.endFill()
