#!/usr/bin/python

from gimpfu import *
import gtk
import gimp
from gobject import timeout_add
from PIL import Image


class result(gtk.Window):
    def __init__(self, img, bnw, gray, sat, *args):
        self.img = img  
        self.pathfile = img.filename
        self.label = gtk.Label()
        r = gtk.Window.__init__(self, *args)
        self.add(self.label)
        self.label.set_text("\n  Por favor aguarde, processando imagem... .  \n")
        self.label.show()
        self.show()
        self.bnw = bnw
        self.gray = gray
        self.sat = sat
        timeout_add(100, self.update, self)    
        return r
    
    def update(self, *args):
        text = self.analysis(self, *args)        
        self.label.set_text(text)

    def analysis(self, *args):
        try:
            imagePIL = Image.open(self.pathfile)
            imgformat = imagePIL.format 
            imgmode = imagePIL.mode
            imageW = imagePIL.size[0]
            imageH = imagePIL.size[1]
            pixelsCount = imageW * imageH
            RGBamouts = [0, 0, 0]
            luminosidadeRGB = 0
            CMYKamouts = [0, 0, 0, 0]
            luminosidadeCMYK = 0
            ival = -1
            if imgmode != 'RGB':
                imageRGB = imagePIL.convert('RGB')
            else:
                imageRGB = imagePIL
            if imgmode != 'CMYK':
                imageCMYK = imagePIL.convert('CMYK')
            else:
                imageCMYK = imagePIL
            if self.bnw:
                imageBnw = Image.new("RGB", (imageW,imageH))
                valBnw = list(imageBnw.getdata())
            if self.gray:
                imageGray = Image.new("RGB", (imageW,imageH))
                valGray = list(imageGray.getdata())
            if self.sat:
                imageSat = Image.new("RGB", (imageW,imageH))
                valSat = list(imageSat.getdata())
            for x in range(imageH):
                for y in range(imageW):
                    maiorRGB = 0
                    incidenciaRGB = 0
                    RGBchannels = [0, 0, 0]
                    somaChannelsRGB = 0
                    for zRGB in range(len(RGBchannels)):
                        RGBchannels[zRGB] = imageRGB.getpixel((y, x))[zRGB]
                    for cRGB in range(len(RGBchannels)):
                        somaChannelsRGB += RGBchannels[cRGB]
                        if (RGBchannels[cRGB] >= RGBchannels[0]):
                            if (RGBchannels[cRGB] >= RGBchannels[1]):
                                if (RGBchannels[cRGB] >= RGBchannels[2]):
                                    incidenciaRGB += 1
                                    maiorRGB = RGBchannels[cRGB]
                    if self.sat:
                        r = 0
                        g = 0
                        b = 0
                        if RGBchannels[0] >= maiorRGB:
                            r = 1
                        if RGBchannels[1] >= maiorRGB:
                            g = 1
                        if RGBchannels[2] >= maiorRGB:
                            b = 1 
                    ival += 1
                    if somaChannelsRGB > 378:
                        luminosidadeRGB  += 1.00000
                        if self.bnw:
                            valBnw[ival] = (255,255,255)
                    else:
                        if self.bnw:
                            valBnw[ival] = (0,0,0)
                    if self.gray:
                        valGray[ival] = (somaChannelsRGB/3,somaChannelsRGB/3,somaChannelsRGB/3)
                    if self.sat:
                        valSat[ival] = (int(r*255/incidenciaRGB),int(g*255/incidenciaRGB),int(b*255/incidenciaRGB))
                    for iRGB in range(len(RGBchannels)):
                        if RGBchannels[iRGB] >= maiorRGB:
                            RGBamouts[iRGB] += (1.00000 / incidenciaRGB)
                    maiorCMYK = 0
                    incidenciaCMYK = 0
                    CMYKchannels = [0,0,0,0]
                    somaChannelsCMYK = 0
                    for zCMYK in range(len(CMYKchannels)):
                            CMYKchannels[zCMYK] = imageCMYK.getpixel((y,x))[zCMYK] 
                    for cCMYK in range(len(CMYKchannels)):
                            somaChannelsCMYK += CMYKchannels[cCMYK]
                            if(CMYKchannels[cCMYK] >= CMYKchannels[0]):
                                if (CMYKchannels[cCMYK] >= CMYKchannels[1]):
                                    if (CMYKchannels[cCMYK] >= CMYKchannels[2]):
                                        if (CMYKchannels[cCMYK] >= CMYKchannels[3]):
                                            incidenciaCMYK += 1
                                            maiorCMYK = CMYKchannels[cCMYK]
                    if somaChannelsCMYK < 368:
                        luminosidadeCMYK  += 1.00000                                  
                    for iCMYK in range(len(CMYKchannels)):
                        if CMYKchannels[iCMYK] >= maiorCMYK:
                            CMYKamouts[iCMYK] += (1.00000/incidenciaCMYK)             

            Description = "\n General Ratio - um interpretador de imagem por pixel  \n"
            Description += "\n Imagem format - %s" % imgformat
            Description += "\n Imagem mode - %s" % imgmode
            Ratio = " \n\n RGB: \n"
            Ratio += "  Predominante Red Pixels: %d (%.2f %%) \n" % (RGBamouts[0], (RGBamouts[0] / pixelsCount) * 100)
            Ratio += "  Predominante Green Pixels: %d (%.2f %%) \n" % (RGBamouts[1], (RGBamouts[1] / pixelsCount) * 100)
            Ratio += "  Predominante Blue Pixels: %d (%.2f %%) \n" % (RGBamouts[2], (RGBamouts[2] / pixelsCount) * 100)
            Ratio += "  Predominancia luminosa RGB: %d (%.2f %%) \n" % (luminosidadeRGB, (luminosidadeRGB/pixelsCount)*100)
            Ratio += " \n CMYK: \n"
            Ratio += "  Predominante Ciano Pixels: %d (%.2f %%) \n" % (CMYKamouts[0], (CMYKamouts[0]/pixelsCount)*100)
            Ratio += "  Predominante Magenta Pixels: %d (%.2f %%) \n" % (CMYKamouts[1], (CMYKamouts[1]/pixelsCount)*100)
            Ratio += "  Predominante Yellow Pixels: %d (%.2f %%) \n" % (CMYKamouts[2], (CMYKamouts[2]/pixelsCount)*100)
            Ratio += "  Predominante Black Pixels: %d (%.2f %%) \n" % (CMYKamouts[3], (CMYKamouts[3]/pixelsCount)*100)
            Ratio += "  Predominancia luminosa CMYK: %d (%.2f %%) \n" % (luminosidadeCMYK, (luminosidadeCMYK/pixelsCount)*100)
            Result = " \n Altura (height): %d \n Largura (weight): %d \n Pixels: %d \n" % (imageH ,imageW, pixelsCount)
            if self.bnw:
                saveBnw = self.pathfile + "_bnw.jpg"
                imageBnw.putdata(valBnw)
                imageBnw.save(saveBnw, "JPEG")
                Result += " \n Uma copia preto e branco foi salva em: " + saveBnw
            if self.gray:
                saveGray = self.pathfile + "_gray.jpg"
                imageGray.putdata(valGray)
                imageGray.save(saveGray, "JPEG")
                Result += " \n Uma em tom de cinza foi salva em: " + saveGray
            if self.sat:
                saveSat = self.pathfile + "_sat.jpg"
                imageSat.putdata(valSat)
                imageSat.save(saveSat, "JPEG")
                Result += " \n Uma supersaturada foi salva em: " + saveSat     
            Result = Description + Ratio + Result
            return Result
        except:
            return " Nao foi possivel processar a imagem, tente uma imagem .jpg, .gif ou .png "  


def img_ratio (img,drw,bnw,gray,sat):
    statusProcess = result(img,bnw,gray,sat)
    gtk.main() 
    
register(
        "img_ratio",
        "General Ratio \n A general ratio for images \n por Fabio R. Santos \n exclusivo para fins educacionais",
        "A general ratio for images",
        "Fabio R. Santos",
        "Fabio R. Santos",
        "2016",
        "<Image>/Tools/General Ratio...",
        "*",
        [
         (PF_BOOL, "bnw", "Criar uma copia preto e branco:", 0),
         (PF_BOOL, "gray", "Criar uma copia em tons de cinza:", 0),
         (PF_BOOL, "sat", "Criar uma copia supersaturada:", 0)
         ],
        [],
        img_ratio)

main()
