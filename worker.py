import redis
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

print("Worker started processing queue...")

seats_available = 1000
seats_booked = 0

while True:
    booking_id = r.rpop("booking_queue")

    if booking_id:
        seats_booked += 1

        if seats_booked <= seats_available:
            # save booking result
            r.hset(f"booking:{booking_id}", mapping={
                "status": "CONFIRMED",
                "seat_number": seats_booked
            })
            print(f"Seat {seats_booked} confirmed - {booking_id}")
        else:
            # seats full
            r.hset(f"booking:{booking_id}", mapping={
                "status": "SEATS_FULL"
            })
            print(f"Seats full - {booking_id}")

        time.sleep(0.1)  # after processing one booking

    else:
        time.sleep(0.5)  # queue empty, wait