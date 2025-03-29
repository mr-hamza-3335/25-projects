import socket
import threading
import pickle

# Server Settings
HOST = "0.0.0.0"  # Listen on all network interfaces
PORT = 6000

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
