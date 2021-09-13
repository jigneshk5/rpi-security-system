from gpiozero import MotionSensor,LED
from picamera import PiCamera
import time
import smtplib
from datetime import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

pir = MotionSensor(4)
led= LED(2)
camera = PiCamera()
camera.resolution = (1024,768)
camera.rotation=180

from_email_addr = 'FROM_EMAIL'
from_email_password = 'FROM_EMAIL_PASSWORD'
to_email_addr = 'FROM_EMAIL'
subject='Security alert!'

while True:
    if pir.motion_detected:
        print("someone present")
        led.on()
        #camera warm-up time
        time.sleep(2)
        picname= datetime.now().strftime("%y-%m-%d-%H-%M")
        picname= picname+'.jpg'
        camera.capture(picname)
        time.sleep(5)
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = from_email_addr
        msg['To'] = to_email_addr
        
        fp= open(picname,'rb')
        img = MIMEImage(fp.read())
        fp.close()
        msg.attach(img)

        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(user = from_email_addr ,password=from_email_password)
        server.send_message(msg)
        server.quit()
    else:
        print("none")
        led.off()
  
