import time
import random
import requests

API_URL = "http://127.0.0.1:5000/sensor"

print("=== BIOSLEEP BIOSENSOR ===")
print("Sending sensor data to BioSleep Platform...\n")

while True:
    temperature = round(random.uniform(30, 45), 1)
    microbial_index = random.randint(10, 100)

    if microbial_index < 40:
        status = "NORMAL"
    elif microbial_index < 75:
        status = "WARNING"
    else:
        status = "CRITICAL"

    data = {
        "temperature": temperature,
        "microbial_index": microbial_index,
        "dna_status": status
    }

    print("--------------------------------")
    print(f"Temperature     : {temperature} C")
    print(f"Microbial Index : {microbial_index}")
    print(f"DNA Status      : {status}")

    if status == "CRITICAL":
        print("ALERT: CRITICAL GENETIC MUTATION DETECTED!")

    try:
        response = requests.post(API_URL, json=data)
        print("Platform        : DATA SENT")
    except requests.exceptions.RequestException:
        print("Platform        : CONNECTION FAILED")

    time.sleep(3)
