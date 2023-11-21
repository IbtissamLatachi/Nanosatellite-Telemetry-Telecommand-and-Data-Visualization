from django.http import JsonResponse
import socket
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt 
def obc_view(request):
    if request.method == 'POST':
        try:
            # Parse the request data
            request_data = json.loads(request.body)
            text_to_send = request_data.get('request', 'command')

            # Create a socket object
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Define the server address and port
            server_address = ('localhost', 2847)

            print(f"Connecting to {server_address}...")

            try:
                # Connect to the server
                client_socket.connect(server_address)

                print("Connected to the server.")

                # Generate random data
                num_10 = "10"
                random_num = "1"
                #random_text = ''.join(random.choice(string.ascii_letters) for _ in range(10))

                # Combine the data into a string
                data_to_send = f"{num_10},{random_num},{text_to_send}"

                # Send the data to the server
                client_socket.send(data_to_send.encode('utf-8'))

                # Receive acknowledgment from the server
                acknowledgment = client_socket.recv(1024)
                print(f"Server Acknowledgment: {acknowledgment.decode('utf-8')}")

                # Close the client socket
                client_socket.close()

                return JsonResponse({'message': 'Data sent successfully'})
            except Exception as e:
                return JsonResponse({'error': f'Error connecting to the server: {str(e)}'}, status=500)
        except Exception as e:
            return JsonResponse({'error': f'Error parsing request data: {str(e)}'}, status=400)
    else:
        return JsonResponse({'error': 'POST request required.'}, status=400)
