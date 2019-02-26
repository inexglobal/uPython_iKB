from micropython import const
from machine import Pin,I2C
from time import sleep
import sys
import struct
import machine
import time
currentBoard=""
if(sys.platform=="esp8266"):
  currentBoard="esp8266"
elif(sys.platform=="esp32"):
  currentBoard="esp32"
class IKB:
  def __init__(self,i2c,address = 72):
    self.i2c = i2c
    self.con_ipstw = 0
    self.address = address
  def begin(self):
    if(72 in self.i2c.scan()):
      self.con_ipstw=1
    else:
      self.con_ipstw=0
    if self.con_ipstw==1:
      reg = bytearray(1)
      reg[0]=0x00
      self.i2c.writeto(self.address,reg)
    #print('Run....')
    #print(sys.platform)
    #print(self.con_ipstw)
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
    if port<8 and self.con_ipstw==1:
      if self.con_ipstw==1:
        reg=0x08|port
        self.i2c.writeto_mem(self.address,reg,logics)
  def input(self,port):
    if port<8 and self.con_ipstw==1:
        reg = bytearray(2)
        reg[0]=0x08|port
        reg[1]=0x02
        self.i2c.writeto(self.address,reg)
        data = self.i2c.readfrom(self.address,1)
        value =  data[0] & 0x01
        return value
    else:
      return -1
    
  















