import socket
import json
import random
import threading
import time
import logging
from typing import List, Dict, Any

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class QuizGame:
    def __init__(self, host: str = '0.0.0.0', port: int = 65432, time_limit: int = 30):
        self.host = host
        self.port = port
        self.time_limit = time_limit
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients: List[socket.socket] = []
        self.nicknames: List[str] = []
        self.scores: Dict[str, int] = {}
        self.current_turn = 0
        self.lock = threading.Lock()
        self.turn_timer: threading.Timer = None
        self.questions: List[Dict[str, Any]] = []

    def start_server(self):
        self.server.bind((self.host, self.port))
        self.server.listen()
        logging.info(f"Servidor escuchando en {self.host}:{self.port}")
        self.accept_connections()

    def accept_connections(self):
        while True:
            client, address = self.server.accept()
            logging.info(f"Nueva conexión de {address}")
            threading.Thread(target=self.handle_client_connection, args=(client, address)).start()

    def handle_client_connection(self, client: socket.socket, address: tuple):
        try:
            self.send_message(client, 'NICKNAME')
            nickname = client.recv(1024).decode('utf-8').strip()
            
            with self.lock:
                if nickname in self.nicknames:
                    index = self.nicknames.index(nickname)
                    if self.clients[index] is None:
                        self.clients[index] = client
                        logging.info(f"{nickname} se ha reconectado.")
                    else:
                        self.send_message(client, "Nickname ya está en uso. Desconectando.")
                        client.close()
                        return
                else:
                    self.nicknames.append(nickname)
                    self.clients.append(client)
                    self.scores[nickname] = 0
                    logging.info(f"Nuevo jugador: {nickname}")
                    self.broadcast(f"{nickname} se ha unido al juego!")
                    self.send_message(client, "Conectado al servidor!")

                if len(self.clients) == 2:  # Iniciar el juego con dos jugadores
                    self.start_game()

        except Exception as e:
            logging.error(f"Error en la conexión del cliente: {e}")
            self.remove_client(client)

    def start_game(self):
        self.questions = self.load_questions('preguntas.json')
        random.shuffle(self.questions)
        self.broadcast("¡El juego está comenzando!")
        self.handle_turn()

    def handle_turn(self):
        if not self.clients:
            self.end_game()
            return

        while self.clients[self.current_turn] is None:
            self.current_turn = (self.current_turn + 1) % len(self.clients)

        client = self.clients[self.current_turn]
        nickname = self.nicknames[self.current_turn]
        threading.Thread(target=self.handle_client_turn, args=(client, nickname)).start()

    def handle_client_turn(self, client: socket.socket, nickname: str):
        if not self.questions:
            self.end_game()
            return

        question = self.questions.pop(0)
        self.send_question(client, question)

        def time_expired():
            logging.info(f"Tiempo expirado para {nickname}")
            self.send_message(client, "Tiempo expirado. Siguiente jugador.")
            self.next_turn()

        self.turn_timer = threading.Timer(self.time_limit, time_expired)
        self.turn_timer.start()

        try:
            answer = client.recv(1024).decode('utf-8').strip().lower()
            self.turn_timer.cancel()

            if answer == question['respuesta_correcta'].lower():
                self.send_message(client, "¡Respuesta correcta!")
                self.scores[nickname] += 1
            else:
                self.send_message(client, f"Respuesta incorrecta. La respuesta correcta era: {question['respuesta_correcta']}")

            self.send_message(client, f"Puntuación actual: {self.scores[nickname]}")
            self.broadcast(f"Puntuación de {nickname}: {self.scores[nickname]}")
            self.next_turn()

        except Exception as e:
            logging.error(f"Error durante el turno de {nickname}: {e}")
            self.remove_client(client)
            self.next_turn()

    def next_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.clients)
        self.handle_turn()

    def end_game(self):
        ranking = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        result = "\n¡Juego terminado!\nRanking final:\n"
        for i, (nickname, score) in enumerate(ranking, start=1):
            result += f"{i}. {nickname} - {score} puntos\n"
        self.broadcast(result)
        self.reset_game()

    def reset_game(self):
        self.clients = []
        self.nicknames = []
        self.scores = {}
        self.current_turn = 0
        self.questions = []

    def remove_client(self, client: socket.socket):
        with self.lock:
            if client in self.clients:
                index = self.clients.index(client)
                self.clients[index] = None
                nickname = self.nicknames[index]
                logging.info(f"{nickname} se ha desconectado.")
                self.broadcast(f"{nickname} ha abandonado el juego.")

    def broadcast(self, message: str):
        for client in self.clients:
            if client:
                self.send_message(client, message)

    def send_message(self, client: socket.socket, message: str):
        try:
            client.send(message.encode('utf-8'))
        except Exception as e:
            logging.error(f"Error al enviar mensaje: {e}")
            self.remove_client(client)

    def send_question(self, client: socket.socket, question: Dict[str, Any]):
        message = json.dumps({
            'pregunta': question['enunciado'],
            'opciones': question['opciones']
        })
        self.send_message(client, message)

    @staticmethod
    def load_questions(file_path: str) -> List[Dict[str, Any]]:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            logging.error(f"Archivo de preguntas no encontrado: {file_path}")
            return []
        except json.JSONDecodeError:
            logging.error(f"Error al decodificar el archivo JSON: {file_path}")
            return []

if __name__ == "__main__":
    game = QuizGame()
    game.start_server()














   
   