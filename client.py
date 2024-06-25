import socket
import json
import threading
import time

class QuizClient:
    def __init__(self, host='localhost', port=65432):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nickname = ""

    def start(self):
        try:
            self.client.connect((self.host, self.port))
            print(f"Conectado al servidor {self.host}:{self.port}")
            
            self.nickname = input("Ingresa tu nickname: ")
            self.client.send(self.nickname.encode('utf-8'))

            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.start()

            self.send_messages()
        except Exception as e:
            print(f"Error al conectar al servidor: {e}")

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if not message:
                    print("Conexión cerrada por el servidor.")
                    break

                if message.startswith('{') and message.endswith('}'):
                    # Es un mensaje JSON (pregunta)
                    self.handle_question(message)
                else:
                    print(message)
            except Exception as e:
                print(f"Error al recibir mensaje: {e}")
                break
        
        self.client.close()

    def handle_question(self, message):
        try:
            question_data = json.loads(message)
            print("\n" + question_data['pregunta'])
            for i, option in enumerate(question_data['opciones'], start=1):
                print(f"{i}. {option}")
        except json.JSONDecodeError:
            print("Error al decodificar la pregunta.")

    def send_messages(self):
        while True:
            try:
                message = input()
                self.client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error al enviar mensaje: {e}")
                break

if __name__ == "__main__":
    client = QuizClient()
    client.start()




