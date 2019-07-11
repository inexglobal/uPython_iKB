from micropython import const
from machine import ADC,Pin,I2C,PWM
from time import sleep
import neopixel
import sys
import struct
import neopixel
import framebuf
import ure
# MicroPython SSD1306 OLED driver, I2C and SPI interfaces
import time
currentBoard=""
if(sys.platform=="esp8266"):
  currentBoard="esp8266"
elif(sys.platform=="esp32"):
  currentBoard="esp32"
# register definitions
SET_CONTRAST        = const(0x81)
SET_ENTIRE_ON       = const(0xa4)
SET_NORM_INV        = const(0xa6)
SET_DISP            = const(0xae)
SET_MEM_ADDR        = const(0x20)
SET_COL_ADDR        = const(0x21)
SET_PAGE_ADDR       = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP       = const(0xa0)
SET_MUX_RATIO       = const(0xa8)
SET_COM_OUT_DIR     = const(0xc0)
SET_DISP_OFFSET     = const(0xd3)
SET_COM_PIN_CFG     = const(0xda)
SET_DISP_CLK_DIV    = const(0xd5)
SET_PRECHARGE       = const(0xd9)
SET_VCOM_DESEL      = const(0xdb)
SET_CHARGE_PUMP     = const(0x8d)
 



class IKB():
  
  def __init__(self,i2c=I2C(scl=Pin(22), sda=Pin(21), freq=1000000),address = const(0x48) ):

    self.temp = bytearray(2)
    self.i2c = i2c
    self.con_ipstw = 0

    self.address = address
    self.begin()
  def map(self,value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))
  def begin(self):
    if(72 in self.i2c.scan()):
      self.con_ipstw=1
    else:
      self.con_ipstw=0
      print('Not found IKB !')
    if self.con_ipstw==1:
      reg = bytearray(1)
      reg[0]=0x00
      self.i2c.writeto(self.address,reg)
    #self.np.write()
      print('IKB....Run')
    
  
  def motor(self,m,speed):
    
    sp=(int(speed)).to_bytes(1,'little')
    reg=0x00
    if m==1: 
      reg=0x21 
    elif m==2:
      reg=0x22
    elif m==3:
      reg=0x24
    elif m==4:
      reg=0x28
    if self.con_ipstw==1:
      self.i2c.writeto_mem(self.address,reg,sp)
  def servo(self,m,pos):
    pos=(int(pos)).to_bytes(1,'little')
    reg=0x40
    if m==10: 
      reg=reg|0x01
    elif m==11:
      reg=reg|0x02
    elif m==12:
      reg=reg|0x04
    elif m==13:
      reg=reg|0x08
    elif m==14:
      reg=reg|0x10
    elif m==15:
      reg=reg|0x20
    if self.con_ipstw==1:
      self.i2c.writeto_mem(self.address,reg,pos)
  def analog(self,port):
    if port<8:
      if self.con_ipstw==1:
        reg=0x80|(port<<4)
        data = self.i2c.readfrom_mem(self.address,reg, 2)
        value = (data[0] << 8 | data[1]) & 0x3ff
        return value
      return -1
  
  def output(self,port,logic):
    if logic >1:
      logic=1
    logics=(int(logic)).to_bytes(1,'little')
    if port<8:
      if self.con_ipstw==1:
        reg=0x08|port
        self.i2c.writeto_mem(self.address,reg,logics)

  def input(self,port):
    if(port<8):
      if self.con_ipstw==1:
        reg = bytearray(2)
        reg[0]=0x08|port
        reg[1]=0x02
        self.i2c.writeto(self.address,reg)

        data = self.i2c.readfrom(self.address,1)
        value =  data[0] & 0x01
        return value
      return -1




  def fd(self,speed):
    sp1=(int(speed)).to_bytes(1,'little')
    sp2=(int(speed*-1)).to_bytes(1,'little')
    regL = 0x21
    regR = 0x22
    if self.con_ipstw==1:
      self.i2c.writeto_mem(self.address,regL,sp1)
      self.i2c.writeto_mem(self.address,regR,sp1)
      
  
          
  def bk(self,speed):
    sp1=(int(speed)).to_bytes(1,'little')
    sp2=(int(speed*-1)).to_bytes(1,'little')
    regL = 0x21
    regR = 0x22
    if self.con_ipstw==1:
      self.i2c.writeto_mem(self.address,regL,sp2)
      self.i2c.writeto_mem(self.address,regR,sp2)
  def sl(self,speed):
    sp1=(int(speed)).to_bytes(1,'little')

    sp2=(int(speed*-1)).to_bytes(1,'little')
    regL = 0x21
    regR = 0x22
    if self.con_ipstw==1:
      self.i2c.writeto_mem(self.address,regL,sp2)
      self.i2c.writeto_mem(self.address,regR,sp1)
  def sr(self,speed):
    sp1=(int(speed)).to_bytes(1,'little')
    sp2=(int(speed*-1)).to_bytes(1,'little')
    regL = 0x21
    regR = 0x22
    if self.con_ipstw==1:
      self.i2c.writeto_mem(self.address,regL,sp1)
      self.i2c.writeto_mem(self.address,regR,sp2)
  def tl(self,speed):
    sp1=(int(speed)).to_bytes(1,'little')
    sp2=(int(speed*-1)).to_bytes(1,'little')
    sp0=(int(0)).to_bytes(1,'little')
    regL = 0x21
    regR = 0x22
    if self.con_ipstw==1:
      self.i2c.writeto_mem(self.address,regL,sp0)
      self.i2c.writeto_mem(self.address,regR,sp1)
  def tr(self,speed):
    sp1=(int(speed)).to_bytes(1,'little')
    sp2=(int(speed*-1)).to_bytes(1,'little')
    sp0=(int(0)).to_bytes(1,'little')
    regL = 0x21
    regR = 0x22
    if self.con_ipstw==1:
      self.i2c.writeto_mem(self.address,regL,sp1)
      self.i2c.writeto_mem(self.address,regR,sp0)
  def fd2(self,speed1,speed2):
    spfd1=(int(speed1*1)).to_bytes(1,'little')
    spfd2=(int(speed2*1)).to_bytes(1,'little')
    regL = 0x21
    regR = 0x22
    if self.con_ipstw==1:
      self.i2c.writeto_mem(self.address,regL,spfd1)
      self.i2c.writeto_mem(self.address,regR,spfd2)
  def bk2(self,speed1,speed2):
    spbk1=(int(speed1*-1)).to_bytes(1,'little')
    spbk2=(int(speed2*-1)).to_bytes(1,'little')
    regL = 0x21
    regR = 0x22
    if self.con_ipstw==1:
      self.i2c.writeto_mem(self.address,regL,spbk1)
      self.i2c.writeto_mem(self.address,regR,spbk2)
  def stop(self):
    spbk1=(int(0)).to_bytes(1,'little')
    regL = 0x21
    regR = 0x22
    if self.con_ipstw==1:
      self.i2c.writeto_mem(self.address,regL,spbk1)
      self.i2c.writeto_mem(self.address,regR,spbk1)

































