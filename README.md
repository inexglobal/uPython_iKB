# uPythoniKB
ไลบรารีการใช้งาน iKB สำหรับภาษา microPython
## ผนวกชุดคำสั่งควบคุมการทำงานของ I2C และ Pin
  from machine import I2C,Pin	
## ผนวกชุดคำสั่งจากไลบรารี ikb
  import ikb       	
## ระบุขาของ I2C
  i2c = I2C(scl = Pin(22),sda=Pin(21),freq=1000000)    
## กำหนดการใช้งาน I2C ของ ikb
k = ikb.IKB(i2c) หรือ k = ikb.IKB()       
## เริ่มต้นใช้งาน ikb
k.begin()                                                                         
## คำสั่งใช้งานเอาต์พุตจากพอร์ตหมายเลข 0
k.output(0,1) 		
## อ่านค่าอินพุต จากพอร์ตหมายเลข 0
x = k.input(0)  คืนค่า 0,1 
## คำสั่งใช้งานอ่านค่าแอนาลอกจากพอร์ตหมายเลข 2 
an = k.analog(2)  คืนค่า 0-1023                                                              
## คำสั่งควบคุมมอเตอร์ด้านซ้ายให้เดินหน้า 100 %
k.motor(1,100)  
## คำสั่งควบคุมมอเตอร์ด้านขวาให้ถอยหลัง 100 %
k.motor(2,-100)                                                    
## คำสั่งควบคุมเซอร์โวมอเตอร์พอร์ต 15 ให้หมุนไปที่มุม 0 องศา
k.servo(15,0) 	
## เดินหน้า 100 %
k.fd(100) 	 
## ถอยหลัง 80 %
k.bk(80) 	  
## หมุนซ้าย 60 %
k.sl(60)
## หมุนขวา 40 %
k.sr(40) 	    
## เลี้ยวซ้าย 60 %
k.tl(60) 	 
## เลี้ยวขวา 60 %
k.tr(60) 	   
## เดินหน้าแบบปรับความเร็วแต่ละมอเตอร์ ล้อซ้าย 100 % ล้อขวา 50 %
k.fd2(100,50) 
## ถอยหลังแบบปรับความเร็วแต่ละมอเตอร์ ล้อซ้าย 55 % ล้อขวา 50 %
k.bk2(55,50) 	  
## หยุดเคลื่อนที่
k.stop()	                                      
