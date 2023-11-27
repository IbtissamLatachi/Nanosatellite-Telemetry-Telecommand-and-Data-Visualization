from django.http import JsonResponse
from pymongo import MongoClient
import datetime
from django.views.decorators.csrf import csrf_exempt
import os
import certifi

# Replace with your MongoDB connection details
client = MongoClient(
    "mongodb+srv://merradi:sonxoq-xubfi5-tyxPas@cluster0.uwxph0t.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=certifi.where(),
)
db = client.myDatabase
collection = db.dashboard_collection


@csrf_exempt
def parse_and_store_gpredict_data():
    desktop_path = os.path.expanduser("~/Desktop")
    file_path = os.path.join(desktop_path, "AO-73-passes.txt")

    if not os.path.exists(file_path):
        return JsonResponse({"error": "File not found"}, status=404)

    with open(file_path, "r") as file:
        # Skip the initial header lines
        next(file)  # Skip 'Upcoming passes for...'
        next(file)  # Skip 'Observer:'
        next(file)  # Skip 'LAT:...'
        next(file)  # Skip '---' line
        next(file)  # Skip column header line
        next(file)  # Skip '---' line (separator)

        for line in file:
            # Skip empty lines
            if not line.strip():
                continue

            # Parse each line for satellite pass data
            try:
                parts = line.split()
                aos = datetime.datetime.strptime(
                    parts[0] + " " + parts[1], "%Y/%m/%d %H:%M:%S"
                )
                tca = datetime.datetime.strptime(
                    parts[2] + " " + parts[3], "%Y/%m/%d %H:%M:%S"
                )
                los = datetime.datetime.strptime(
                    parts[4] + " " + parts[5], "%Y/%m/%d %H:%M:%S"
                )
                duration = parts[6]
                max_el, aos_az, los_az = (
                    float(parts[7]),
                    float(parts[8]),
                    float(parts[9]),
                )

                # Store in MongoDB
                collection.insert_one(
                    {
                        "aos": aos,
                        "tca": tca,
                        "los": los,
                        "duration": duration,
                        "max_el": max_el,
                        "aos_az": aos_az,
                        "los_az": los_az,
                    }
                )
            except Exception as e:
                print(f"Error parsing line: {line}. Error: {e}")

    return JsonResponse({"message": "File processed successfully"})


@csrf_exempt
def get_next_satellite_pass(request):
    parse_and_store_gpredict_data()
    now = datetime.datetime.now()
    next_pass = collection.find_one({"aos": {"$gt": now}}, sort=[("aos", 1)])

    if next_pass:
        next_pass["_id"] = str(next_pass["_id"])
        next_pass["aos"] = next_pass["aos"].isoformat()
        next_pass["los"] = next_pass["los"].isoformat()
        return JsonResponse(next_pass)
    else:
        return JsonResponse({"message": "No upcoming passes found"})
