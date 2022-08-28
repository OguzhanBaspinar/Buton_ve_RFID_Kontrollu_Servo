from pirc522 import RFID
import signal
import time
import RPi.GPIO as GPIO
GPIO.setwarnings (False)
 
yesilled = 7                    # yeşil led 7 numaralı BOARD pinine atanmıştır
kirmiziled = 13                 # kırmızı led 13 numaralı BOARD pinine atanmıştır


GPIO.setmode(GPIO.BOARD)             # 1..40 olarak board dizilimini kullanılacaktır.
GPIO.setup(yesilled, GPIO.OUT)

GPIO.setup(kirmiziled, GPIO.OUT)
oku = RFID()
util = oku.util()                    # RFID haberleşmeyi başlat. 
util.debug = True
GPIO.output(yesilled, False)
while True:
    try:
        oku.wait_for_tag()
        (error, data) = oku.request()
        if not error:
            print("\nKart Algilandi!")
            (error, kartid) = oku.anticoll()          # doğru okunan RFID kart bilgisini kartid değişkenine aktar
            if not error:
                kart = str(kartid[0])+" "+str(kartid[1])+" "+str(kartid[2])+" "+str(kartid[3])+" "+str(kartid[4])
            print(kart)
            kirmiziled = 13
            
            sayac=1
            if kart == "171 195 128 13 229" and sayac == 1:
                sayac == 2
                print("GİRİŞ ONAYLANDI")
                GPIO.output(yesilled, True)
                GPIO.output(kirmiziled, False)
                btnarti = 8
                btneksi = 10
                btnorta = 12
                servo = 11
                deger = 2.5
                
                GPIO.setup(servo, GPIO.OUT)
                GPIO.setup(btnarti, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # btnarti pini giris olarak atanıp dahili olarak
                GPIO.setup(btneksi, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # pull up direnc atanmistir.
                GPIO.setup(btnorta, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
                
                p = GPIO.PWM(servo, 50)       # servo pinin bagli oldugu cikis 50Hz bir frekans ile tetiklenmistir.
                p.start(deger)                # servo sinyalimiz 2.5('deger' değişkeni) ms ile baslatılmıstır.
                
                try:
                    
                    while True:
                        artideger = GPIO.input(btnarti)    # giris pininden gelen deger artideger degiskenine atanmistir.
                        eksideger = GPIO.input(btneksi)  
                        ortadeger = GPIO.input(btnorta)
                        if artideger == False:
                            deger += 0.2  
                            time.sleep(0.3)
                        elif eksideger == False:
                            deger -= 0.2
                            time.sleep(0.3)
                        elif ortadeger == False:
                            deger = 7.7
                        if deger > 12.5:
                            deger = 12.5
                        elif deger < 2.5:
                            deger = 2.5
                        p.ChangeDutyCycle(deger)
                        print(deger)
                except KeyboardInterrupt:
                    p.stop()
                    GPIO.cleanup()
            elif kart == "171 195 128 13 229" and sayac == 2:
                btnarti = 0
                btneksi = 0
                btnorta = 0
                servo = 0
                sayac = 1
                print("YEŞİL LED OFF")
                GPIO.output(yesilled, False)
                GPIO.output(kirmiziled, True)
            else:
                print("Finish")
                
    except KeyboardInterrupt():
       GPIO.cleanup()
       break









