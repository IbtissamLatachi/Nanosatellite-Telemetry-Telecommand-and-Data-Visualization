from django.http import JsonResponse
import socket
import json
import logging
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# Configure logging
logger = logging.getLogger(__name__)


@csrf_exempt
def eps_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Unsupported request method."}, status=405)

    try:
        # Parse the request data
        request_data = json.loads(request.body)
        text_to_send = request_data.get("command", "default command")

        # Validate the input data
        if not text_to_send:
            return JsonResponse({"error": "Invalid request data."}, status=400)

        # Define the server address from Django settings
        server_address = (settings.SERVER_HOST, settings.SERVER_PORT)

        logger.info(f"Connecting to {server_address}...")

        # Using a context manager for socket operations
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(server_address)
            logger.info("Connected to the server.")

            # Send a tuple with [10, 4, {text_to_send}]
            formatted_data = f"{10},{4},{text_to_send}"
            client_socket.send(formatted_data.encode("utf-8"))

            # Wait for and receive acknowledgment from the server
            acknowledgment = client_socket.recv(1024)
            logger.info(f"Server Acknowledgment: {acknowledgment.decode('utf-8')}")

            # Return the server's acknowledgment to the frontend
            return JsonResponse({"message": acknowledgment.decode("utf-8")})
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing request data: {str(e)}")
        return JsonResponse({"error": "Invalid JSON data."}, status=400)
    except socket.error as e:
        logger.error(f"Socket error: {str(e)}")
        return JsonResponse({"error": "Error connecting to the server."}, status=500)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({"error": "An unexpected error occurred."}, status=500)
