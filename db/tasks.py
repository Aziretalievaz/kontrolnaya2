from db.database import get_db
from db.queries import GET_ALL_TASKS, GET_TASK_BY_ID, INSERT_TASK
from db.queries import UPDATE_TASK_STATUS, GET_TASKS_WITH_USER, GET_TASKS_STATS


def get_tasks(user_id: int):
    conn = get_db()
    rows = conn.execute(GET_ALL_TASKS, (user_id, )).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_task(task_id: int):
    conn = get_db()
    row = conn.execute(GET_TASK_BY_ID, (task_id, )).fetchone()
    conn.close()
    return dict(row) if row else None


def create_task(user_id: int, title: str):
    conn = get_db()
    conn.execute(INSERT_TASK, (user_id, title))
    conn.commit()
    conn.close()


def complete_task(task_id: int, user_id: int):
    conn = get_db()
    conn.execute(UPDATE_TASK_STATUS, (task_id, user_id))
    conn.commit()
    conn.close()


def get_tasks_with_user(telegram_id: int):
    conn = get_db()
    rows = conn.execute(GET_TASKS_WITH_USER, (telegram_id, )).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_tasks_stats(user_id: int):
    conn = get_db()
    row = conn.execute(GET_TASKS_STATS, (user_id, )).fetchone()
    conn.close()
    return dict(row) if row else None