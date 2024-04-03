from typing import List
from fastapi import FastAPI, HTTPException
import requests
from collections import deque

app = FastAPI()


WINDOW_SIZE = 10
TEST_SERVER_URL = "http://20.244.56.144/test/rand" # test diffrent api endpoints


number_window = deque()

@app.get("/numbers/{number_id}", response_model=dict)
async def get_numbers(number_id: str):
    try:

        response = requests.get(TEST_SERVER_URL.format(number_id=number_id))
        response.raise_for_status()
        numbers = response.json()
    except (requests.exceptions.RequestException, ValueError):
        raise HTTPException(status_code=503, detail="Failed to fetch numbers from the test server.")


    for number in numbers:
        if number not in number_window:
            number_window.append(number)
            if len(number_window) > WINDOW_SIZE:
                number_window.popleft()


    avg = sum(number_window) / len(number_window) if number_window else 0


    response_data = {
        "numbers": numbers,
        "windowPrevState": list(number_window)[:-len(numbers)],
        "windowCurrState": list(number_window),
        "avg": avg
    }

    return response_data