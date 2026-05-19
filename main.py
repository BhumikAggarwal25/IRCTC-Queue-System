from fastapi import FastAPI
import redis
import uuid 

app = FastAPI()
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.get("/")
def home():
    return {"message": "IRCTC Queue System Running"}

@app.post("/book")
def book_ticket(user_name: str):
    booking_id = str(uuid.uuid4())
    r.lpush("booking_queue", booking_id)
    position = r.llen("booking_queue")
    return {
        "booking_id": booking_id,
        "position": position,
        "message": f"You are #{position} in queue. Please wait."
    }

@app.get("/status/{booking_id}")
def check_status(booking_id: str):
    booking = r.hgetall(f"booking:{booking_id}")
    if booking:
        return {
            "booking_id": booking_id,
            "status": booking.get("status"),
            "seat_number": booking.get("seat_number", "N/A")
        }
    queue = r.lrange("booking_queue", 0, -1)
    if booking_id in queue:
        position = queue.index(booking_id) + 1
        return {
            "booking_id": booking_id,
            "status": "WAITING",
            "position": position
        }
    return {"status": "NOT_FOUND"} 