import socket
import threading
import pickle
import pygame

# Server Settings
HOST = "127.0.0.1"  # Listen on localhost
PORT = 6000  # Changed port number

# Players Data
players = {}
lock = threading.Lock()

# Function to handle each client
def handle_client(conn, addr, player_id):
    global players
    print(f"New connection from {addr}, assigned Player {player_id}")
    conn.send(pickle.dumps(player_id))  # Send player ID
    
    while True:
        try:
            data = pickle.loads(conn.recv(1024))
            if not data:
                break
            
            with lock:
                players[player_id] = data  # Update player position
            
            conn.sendall(pickle.dumps(players))  # Send all player positions
        except Exception as e:
            print(f"Player {player_id} disconnected: {e}")
            break
    
    with lock:
        del players[player_id]  # Remove player on disconnect
    conn.close()
    print(f"Player {player_id} disconnected")

# Start Server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server started on {HOST}:{PORT}")
    
    player_id = 0
    
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr, player_id)).start()
        player_id += 1

if __name__ == "__main__":
    start_server()

# Client Code
def client_program():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    player_id = pickle.loads(client.recv(1024))
    
    position = [100 + player_id * 50, HEIGHT - 100]
    speed = 5
    
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            position[0] -= speed
        if keys[pygame.K_RIGHT]:
            position[0] += speed
        if keys[pygame.K_UP]:
            position[1] -= speed
        if keys[pygame.K_DOWN]:
            position[1] += speed
        
        client.sendall(pickle.dumps(position))
        players_data = pickle.loads(client.recv(1024))
        
        for p_id, pos in players_data.items():
            color = (0, 255, 0) if p_id == player_id else (255, 0, 0)
            pygame.draw.rect(screen, color, (*pos, 40, 60))
        
        pygame.display.flip()
        clock.tick(30)
    
    client.close()
    pygame.quit()

if __name__ == "__main__":
    client_program()
