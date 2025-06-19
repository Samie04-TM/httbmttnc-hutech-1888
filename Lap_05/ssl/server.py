import socket
import ssl
import threading

# Thông tin server
server_address = ('localhost', 12345)

# Danh sách các client đã kết nối
clients = []

def handle_client(client_socket):
    """
    Xử lý kết nối từ một client cụ thể.
    Nhận dữ liệu từ client và gửi lại cho tất cả các client khác.
    """
    # Thêm client vào danh sách
    clients.append(client_socket)
    print(f"Đã kết nối với: {client_socket.getpeername()}")

    try:
        # Nhận và gửi dữ liệu
        while True:
            data = client_socket.recv(1024)
            if not data:
                # Nếu không nhận được dữ liệu, client đã đóng kết nối
                print(f"Client {client_socket.getpeername()} đã ngắt kết nối.")
                break
            
            # Giải mã dữ liệu và in ra
            print(f"Nhận từ {client_socket.getpeername()}: {data.decode('utf-8')}")

            # Gửi dữ liệu đến tất cả các client khác (trừ client gửi)
            for client in clients:
                if client != client_socket:
                    try:
                        client.send(data)
                    except Exception as e:
                        # Xử lý lỗi nếu không gửi được dữ liệu đến một client nào đó
                        print(f"Lỗi gửi dữ liệu đến client {client.getpeername()}: {e}")
                        # Nếu client gặp lỗi, loại bỏ nó khỏi danh sách
                        if client in clients:
                            clients.remove(client)
    except Exception as e:
        # Xử lý lỗi chung trong quá trình xử lý client
        print(f"Lỗi trong quá trình xử lý client {client_socket.getpeername()}: {e}")
    finally:
        # Đảm bảo client_socket bị đóng và loại bỏ khỏi danh sách khi kết thúc
        print(f"Đã ngắt kết nối: {client_socket.getpeername()}")
        if client_socket in clients:
            clients.remove(client_socket)
        client_socket.close()

# Tạo socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5) # Lắng nghe tối đa 5 kết nối đang chờ

print("Server đang chờ kết nối...")

# Lắng nghe các kết nối đến và xử lý chúng
while True:
    client_socket, client_address = server_socket.accept()

    # Tạo SSL context
    # PROTOCOL_TLS_SERVER sử dụng phiên bản TLS an toàn nhất được hỗ trợ bởi hệ thống
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER) 
    
    # Tải chứng chỉ server và khóa riêng tư
    try:
        context.load_cert_chain(certfile="./certificates/server-cert.crt",
                                keyfile="./certificates/server-key.key")
    except FileNotFoundError:
        print("Lỗi: Không tìm thấy tệp chứng chỉ hoặc khóa. Hãy đảm bảo chúng ở đúng đường dẫn './certificates/'.")
        client_socket.close()
        continue
    except ssl.SSLError as e:
        print(f"Lỗi SSL khi tải chứng chỉ/khóa: {e}")
        client_socket.close()
        continue

    # Thiết lập kết nối SSL
    try:
        ssl_socket = context.wrap_socket(client_socket, server_side=True)
    except ssl.SSLError as e:
        print(f"Lỗi SSL khi wrap socket: {e}")
        client_socket.close()
        continue

    # Bắt đầu một luồng xử lý cho mỗi client mới
    client_thread = threading.Thread(target=handle_client, args=(ssl_socket,))
    client_thread.start()
