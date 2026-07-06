from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime

app = FastAPI(
    title="API hệ thống Đặt vé xem phim online",
    version="1.0.0"
)


class TicketsSchema(BaseModel):
    movie_name: str = Field(...)
    room_code: str = Field(...)
    quantity: int = Field(..., ge=1, le=10)


tickets_db = [
    {
        "id": 1,
        "movie_name": "Doctor Strange 3",
        "room_code": "IMAX-01",
        "quantity": 2,
        "status": "confirmed",
        "created_at": "2026-07-01T19:00:00Z"
    },
    {
        "id": 2,
        "movie_name": "Avatar 3",
        "room_code": "PREMIUM-02",
        "quantity": 1,
        "status": "confirmed",
        "created_at": "2026-07-01T20:15:00Z"
    }
]


@app.get("/tickets", tags=["tickets"])
def get_all_list():
    return {
        "statusCode": 200,
        "message": "Lấy danh sách vé thành công!",
        "data": tickets_db,
        "error": None,
        "timestamp": datetime.now().isoformat(),
        "path": "/tickets"
    }


@app.post("/tickets", tags=["tickets"])
def create_ticket(ticket: TicketsSchema):

    # Kiểm tra trùng phim và phòng chiếu
    for tick in tickets_db:
        if (
            tick["movie_name"] == ticket.movie_name
            and tick["room_code"] == ticket.room_code
        ):
            raise HTTPException(
                status_code=400,
                detail="Lỗi: Vé xem phim tại phòng chiếu này đã được đặt!"
            )

    # Sinh ID mới
    id_tick = len(tickets_db) + 1

    new_ticket = ticket.model_dump()
    new_ticket["id"] = id_tick
    new_ticket["status"] = "confirmed"
    new_ticket["created_at"] = datetime.now().isoformat()

    tickets_db.append(new_ticket)

    return {
        "statusCode": 201,
        "message": "Đặt vé thành công!",
        "data": new_ticket,
        "error": None,
        "timestamp": datetime.now().isoformat(),
        "path": "/tickets"
    }


@app.delete("/tickets/{ticket_id}", tags=["tickets"])
def delete_ticket(ticket_id: int):

    for item in tickets_db:
        if item["id"] == ticket_id:
            tickets_db.remove(item)
            return {
                "statusCode": 200,
                "message": "Hủy vé thành công!",
                "data": None,
                "error": None,
                "timestamp": datetime.now().isoformat(),
                "path": f"/tickets/{ticket_id}"
            }

    raise HTTPException(
        status_code=404,
        detail="Lỗi: Không tìm thấy mã vé yêu cầu!"
    )