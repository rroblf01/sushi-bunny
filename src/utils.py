from .models import User, Table


def get_table_state(table_id, db):
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        return None
    users = db.query(User).filter(User.table_id == table_id).all()
    return {
        "table": {"id": table.id, "name": table.name},
        "users": [
            {"id": user.id, "name": user.name, "sushi_count": user.sushi_count}
            for user in users
        ],
    }


async def broadcast_table_state(table_id, db, active_connections):
    table_state = get_table_state(table_id, db)
    if table_id in active_connections:
        for connection in active_connections[table_id]:
            await connection.send_json(table_state)
