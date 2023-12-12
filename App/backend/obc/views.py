from django.http import JsonResponse
import socket
import json
import logging
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import pymongo
import certifi

# Configure logging
logger = logging.getLogger(__name__)


@csrf_exempt
def obc_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Unsupported request method."}, status=405)

    try:
        client = pymongo.MongoClient(
            "",
            tlsCAFile=certifi.where(),
        )
        db = client.myDatabase
        collection = db.obc_collection

        # logger.info("Testing logger in obc_view")

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

            formatted_data = f"{10},{1},{text_to_send}"
            client_socket.send(formatted_data.encode("utf-8"))

            # Wait for and receive acknowledgment from the server
            acknowledgment = client_socket.recv(1024)
            # logger.info(f"Server Acknowledgment: {acknowledgment.decode('utf-8')}")

            # Convert the acknowledgment to a Python dictionary
            try:
                acknowledgment_data = json.loads(acknowledgment.decode("utf-8"))
            except json.JSONDecodeError:
                return JsonResponse(
                    {"error": "Invalid acknowledgment format."}, status=500
                )

            # Insert the acknowledgment data into MongoDB
            result = collection.insert_one(acknowledgment_data)

            # Return the server's acknowledgment to the frontend
            if result:
                return JsonResponse({"message": "Data inserted successfully"})
            else:
                return JsonResponse({"message": "Error during insertion"})

    except json.JSONDecodeError as e:
        logger.error(f"Error parsing request data: {str(e)}")
        return JsonResponse({"error": "Invalid JSON data."}, status=400)
    except socket.error as e:
        logger.error(f"Socket error: {str(e)}")
        return JsonResponse({"error": "Error connecting to the server."}, status=500)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({"error": "An unexpected error occurred."}, status=500)


@csrf_exempt
def fetch_obc_housekeeping_data(request):
    if request.method != "GET":
        return JsonResponse({"error": "Unsupported request method."}, status=405)

    client = pymongo.MongoClient(
        "mongodb+srv://merradi:sonxoq-xubfi5-tyxPas@cluster0.uwxph0t.mongodb.net/?retryWrites=true&w=majority",
        tlsCAFile=certifi.where(),
    )
    db = client.myDatabase
    collection = db.obc_collection

    # Fetch OBC housekeeping telemetry data
    documents = collection.find({"telemetry": {"$exists": True}})

    # Prepare the dataset
    telemetry_data = [
        {
            "timestamp": doc["telemetry"]["Timestamp"],
            "cpu_load": doc["telemetry"]["CPU_Load"],
            "memory_usage": doc["telemetry"]["Memory_Usage"],
            "temperature": doc["telemetry"]["Temperature_Celsius"],
            "power_status": doc["telemetry"]["Power_Status"],
            "active_processes": doc["telemetry"]["Active_Processes"],
        }
        for doc in documents
    ]

    return JsonResponse({"housekeeping_data": telemetry_data})


@csrf_exempt
def fetch_obc_telemetry_command_data(request):
    if request.method != "GET":
        return JsonResponse({"error": "Unsupported request method."}, status=405)

    client = pymongo.MongoClient(
        "mongodb+srv://merradi:sonxoq-xubfi5-tyxPas@cluster0.uwxph0t.mongodb.net/?retryWrites=true&w=majority",
        tlsCAFile=certifi.where(),
    )
    db = client.myDatabase
    collection = db.obc_collection

    # Fetch OBC telemetry command data
    documents = collection.find({"telemetry_command_data": {"$exists": True}})

    # Prepare the dataset
    command_data = [
        {
            "timestamp": doc["telemetry_command_data"]["Timestamp"],
            "last_command": doc["telemetry_command_data"]["Last_Command"],
            "command_success_rate": doc["telemetry_command_data"][
                "Command_Success_Rate"
            ],
            "recent_errors": doc["telemetry_command_data"]["Recent_Errors"],
        }
        for doc in documents
    ]

    return JsonResponse({"command_data": command_data})
