from fastapi import FastAPI, WebSocket, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

from sqlalchemy.orm import Session
import uuid
from fastapi.websockets import WebSocketDisconnect
from src.models import Table, User, get_db
from src.schemas import TableCreate
from src.utils import broadcast_table_state

app = FastAPI()

templates = Jinja2Templates(directory="templates")


active_connections = {}


@app.websocket("/ws/{table_id}")
async def websocket_table(
    websocket: WebSocket, table_id: str, db: Session = Depends(get_db)
):
    await websocket.accept()
    if table_id not in active_connections:
        active_connections[table_id] = []
    active_connections[table_id].append(websocket)

    try:
        await broadcast_table_state(table_id, db, active_connections)

        while True:
            data = await websocket.receive_json()
            action = data.get("action")
            payload = data.get("payload")

            if action == "join":
                name = payload.get("name")
                new_user = User(name=name, table_id=table_id)
                db.add(new_user)
                db.commit()
                db.refresh(new_user)

            elif action == "eat":
                user_id = payload.get("user_id")
                user = (
                    db.query(User)
                    .filter(User.id == user_id, User.table_id == table_id)
                    .first()
                )
                if user:
                    user.sushi_count += 1
                    db.commit()

            elif action == "rename":
                user_id = payload.get("user_id")
                new_name = payload.get("new_name")
                user = (
                    db.query(User)
                    .filter(User.id == user_id, User.table_id == table_id)
                    .first()
                )
                if user:
                    user.name = new_name
                    db.commit()

            await broadcast_table_state(table_id, db, active_connections)

    except WebSocketDisconnect:
        active_connections[table_id].remove(websocket)
        if not active_connections[table_id]:
            del active_connections[table_id]
        await broadcast_table_state(table_id, db, active_connections)


@app.get("/", response_class=HTMLResponse)
def get_home_view(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/mesa/{table_id}", response_class=HTMLResponse)
def get_table_view(request: Request, table_id: str, db: Session = Depends(get_db)):
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    users = db.query(User).filter(User.table_id == table_id).all()
    return templates.TemplateResponse(
        "mesa.html", {"request": request, "table": table, "users": users}
    )


@app.get("/resume/{table_id}", response_class=HTMLResponse)
def get_resume_view(request: Request, table_id: str, db: Session = Depends(get_db)):
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    users = db.query(User).filter(User.table_id == table_id).all()
    return templates.TemplateResponse(
        "resume.html", {"request": request, "table": table, "users": users}
    )


@app.post("/mesa")
def create_table(table: TableCreate, db: Session = Depends(get_db)):
    table_id = str(uuid.uuid4())
    table_name = table.name if table.name else f"Mesa {table_id[:8]}"
    new_table = Table(id=table_id, name=table_name)
    db.add(new_table)
    db.commit()
    db.refresh(new_table)
    return {"table_id": new_table.id, "name": new_table.name}


@app.get("/mesas", response_class=HTMLResponse)
def list_tables_view(request: Request, db: Session = Depends(get_db)):
    tables = db.query(Table).all()
    return templates.TemplateResponse(
        "tables.html", {"request": request, "tables": tables}
    )


app.mount("/", StaticFiles(directory="static", html=True), name="static")
