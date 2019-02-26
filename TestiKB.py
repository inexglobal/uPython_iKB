from machine import I2C,Pin
import ipstw
import ikb
import time
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=1000000)
print (i2c.scan())
ik=ikb.IKB(i2c)
ik.begin()
w=ipstw.IPSTW()
w.begin()
while 1:
  ik.output(0,1)
  ik.motor(1,100)
  ik.motor(2,-100)
  time.sleep(0.5) 
  ik.output(0,0)
  ik.motor(2,100)
  ik.motor(1,-100)
  time.sleep(0.5)
  val=ik.analog(1)
  print(val)
  
