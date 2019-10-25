from tkinter import Tk, Canvas
from PIL import ImageTk, Image, ImageDraw, ImageFont
from src.config import Configuration as GLOBALS
from src.config.Configuration import config
from src.config.ConfigNames import *

# Choose a 'greenscreen' color that is unlikely to appear in a normal image
# All partially transparent Pixels in the Overlay will be blended with this color
# Unfortunately this also makes it impossible to have proper Antialias
TRANSCOLOR = '#020301'

class Overlay(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.configure(background = TRANSCOLOR)

        # Generate default canvas 
        self.canvas = Canvas(self,
                             width = 0, height = 0, # Values get Overridden by updateWidget()
                             bg = TRANSCOLOR, highlightthickness = 0)
        self.canvas.pack()
        self.overlayWidget = None
        self.hideOverlay()

        # Set Font Settings
        self.fontSize = 20
        self.font = ImageFont.truetype("calibri.ttf", self.fontSize)
        self.textXOffset = 25
        self.textYSpacing = 5
        self.imageXStart = 20
        self.imageSpacing = 20

        # Make window virtually invisible
        self.wm_attributes('-transparentcolor', TRANSCOLOR)
        self.wm_attributes("-topmost", True)
        self.overrideredirect(True)

    def tryUpdate(self):
        if config(OVERLAY_MODE) == "images":
            overlayPath = config(RESOURCE_PATH) + config(OVERLAY_IMAGES)
            renderingFunction = self.renderImageLayer
        else:
            overlayPath = config(RESOURCE_PATH) + config(OVERLAY_LABELS)
            renderingFunction = self.renderTextLayer

        soundMatrix = GLOBALS.SOUNDS_BY_STROKES
        try:
            self.updateWidget(overlayPath, soundMatrix, renderingFunction)
        except Exception as e:
            s = "Error starting Overlay:\n"
            s += str(e) + "\n\n"
            s += "Make sure '{}' points to a valid image file.\n".format(overlayPath)

            raise RuntimeError(s)

    ''' Adjust canvas dimensions to match new image and pre-render text overlays '''
    def updateWidget(self, overlay, soundMatrix, renderingFunction):
        # Load overlay Image, set dimensions
        self.overlayBase = Image.open(overlay)
        self.width = self.overlayBase.size[0]
        self.height = self.overlayBase.size[1]

        self.posX = 0
        self.posY = self.winfo_screenheight() // 2 - self.height // 2

        # Move window to be centered on the left side of the screen and adjust Canvas size
        self.canvas.config(width=self.width, height=self.height)
        self.moveWindow(self.posX, self.posY)

        # Render overlays and init canvas Image
        self.overlays = []
        for soundList in soundMatrix:
            self.overlays.append(ImageTk.PhotoImage(renderingFunction(self.overlayBase.copy(), soundList)))

    ''' Render text from an array vertically centered onto an image'''
    def renderTextLayer(self, overlayBase, soundList):
        textLayer = ImageDraw.Draw(overlayBase)
        yStart = self.height // 2 - len(soundList) / 2 * (self.fontSize + self.textYSpacing)
        for i in range(len(soundList)):
            textLayer.text((self.textXOffset, yStart+i*(self.fontSize+self.textYSpacing)),
                           "[{}] {}".format(i + 1, soundList[i].label),
                           fill = (255, 255, 255),
                           font = self.font)
        return overlayBase

    ''' Render small thumbnails with positions matching the numpad keys '''
    def renderImageLayer(self, overlayBase, soundList):
        imageLayer = Image.new("RGBA", overlayBase.size, color = (255, 255, 255, 0))

        imageEdgeLength = config(SOUND_IMAGE_EDGE_LENGTH)

        absoluteCenterX = int(self.imageXStart + imageEdgeLength * 1.5 + self.imageSpacing)
        absoluteCenterY = self.height//2

        for i in range(len(soundList)):
            if soundList[i].image is None:
                continue

            xIndex = i % 3 - 1
            yIndex = 1 - i // 3

            imageCenterX = absoluteCenterX + (imageEdgeLength + self.imageSpacing) * xIndex
            imageCenterY = absoluteCenterY + (imageEdgeLength + self.imageSpacing) * yIndex

            imageLayer.paste(soundList[i].image, (
                imageCenterX - imageEdgeLength // 2, imageCenterY - imageEdgeLength // 2,
                imageCenterX + imageEdgeLength // 2, imageCenterY + imageEdgeLength // 2))

        overlayBase.alpha_composite(imageLayer, (0, 0))
        return overlayBase

    ''' Render an image on the canvas and restore window'''
    def drawOverlay(self, index):
        self.overlayWidget = self.canvas.create_image(0, 0, image=self.overlays[index], anchor="nw")
        self.deiconify()

    ''' Iconify Window so no mouse events get swallowed
        (Only an issue after compiling with Pyinstaller) '''
    def hideOverlay(self):
        if self.overlayWidget:
            self.canvas.delete(self.overlayWidget)
        self.withdraw()

    ''' Place NW Corner of window at (x, y)'''
    def moveWindow(self, x, y):
        self.wm_geometry('+' + str(x) + '+' + str(y))
