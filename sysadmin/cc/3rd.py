import json
import socket

# Define server address and port
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 5000

# Define function to send request to server
def send_request(request):
    # Create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server
    client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

    # Send request to server
    client_socket.send(json.dumps(request).encode('utf-8'))

    # Receive response from server
    response_data = client_socket.recv(1024).decode('utf-8')

    # Parse JSON response
    response = json.loads(response_data)

    # Close client socket
    client_socket.close()

    # Return response
    return response

# Define function to deploy new software
def deploy_new_software(computer_name, app_name, app_version, app_url):
    # Define request data
    request = {
        'type': 'deploy',
        'computer_name': computer_name,
        'app_name': app_name,
        'app_version': app_version,
        'app_url': app_url
    }

    # Send request to server
    response = send_request(request)

    # Return response
    return response

# Example usage to deploy new software on the client
computer_name = 'client_computer_name'
app_name = 'new_app'
app_version = '1.0.0'
app_url = 'https://example.com/new_app.exe'

response = deploy_new_software(computer_name, app_name, app_version, app_url)
print(response)
