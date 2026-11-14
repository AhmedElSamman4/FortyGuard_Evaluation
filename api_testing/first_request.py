
import os
import json
from pyexpat import features
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

# ==========================================
# 1. Configuration
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

API_KEY = os.getenv("FORTYGUARD_API_KEY")

if not API_KEY:
    raise ValueError("API Key not found. Check your .env file.")

BASE_URL = "https://api.fortyguard.com/v1"

HEADERS = {
    "api-key": API_KEY,
    "Content-Type": "application/json"
}

# Choose: "submit" or "poll"
MODE = "poll"

# Used only when MODE = "poll"
ACTIVITY_ID = "78aa1720-0920-49c6-97a1-93cc667601c7"

# ==========================================
# 2. Heatmap Payload
# ==========================================

payload = {
    "polygon_aoi": {
        "type": "Polygon",
        "coordinates": [[
            [-74.0170, 40.7051],
            [-74.0031, 40.7051],
            [-74.0031, 40.7180],
            [-74.0170, 40.7180],
            [-74.0170, 40.7051]
        ]]
    },
    "date_time": {
        "start_date": "2024-07-15",
        "filter_type": 3
    },
    "granularity": 100,
    "analytic_type": "tcm"
}

# ==========================================
# 3. Submit or Reuse Activity ID
# ==========================================

if MODE == "submit":

    print("Submitting Heatmap request...")

    try:
        response = requests.post(
            f"{BASE_URL}/heatmap",
            headers=HEADERS,
            json=payload,
            timeout=60
        )

        print("HTTP Status:", response.status_code)
        response.raise_for_status()

        submission = response.json()
        print("Submission response:", submission)

        activity_id = submission.get(
            "data", {}
        ).get("activity_id")

        if not activity_id:
            raise ValueError("No activity_id in response.")

    except (requests.RequestException, ValueError) as error:
        print("Submission error:", error)
        raise SystemExit(1)

elif MODE == "poll":

    activity_id = ACTIVITY_ID

else:
    raise ValueError("MODE must be 'submit' or 'poll'.")

print("Activity ID:", activity_id)

# ==========================================
# 4. Poll Activity Status
# ==========================================

status_url = f"{BASE_URL}/status/{activity_id}"

max_attempts = 120
poll_interval = 5

print("\nWaiting for Heatmap processing...")

for attempt in range(max_attempts):

    try:
        response = requests.get(
            status_url,
            headers=HEADERS,
            timeout=30
        )

        if response.status_code == 404:
            print("Activity not available yet. Retrying...")
            time.sleep(poll_interval)
            continue

        response.raise_for_status()

        status_data = response.json()
        result = status_data.get("data", {})

        current_status = str(
            result.get("status", "")
        ).lower()

        print(f"Attempt {attempt + 1}: {current_status}")

        if current_status == "completed":

            print("\nHeatmap completed successfully!")

            output_path = (
                Path(__file__).parent / "heatmap_result.json"
            )

            with open(output_path, "w", encoding="utf-8") as file:
                json.dump(
                    result,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            print("Result saved to:", output_path)
            print("Available result fields:", list(result.keys()))
            break

        elif current_status == "failed":

            print("Heatmap generation failed.")
            print("Response:", status_data)
            break

        elif current_status == "processing":

            time.sleep(poll_interval)

        else:

            print("Unexpected status response:", status_data)
            break

    except requests.RequestException as error:
        print("Polling error:", error)
        break

else:
    print("Polling timed out.")
    print("Activity ID:", activity_id)



