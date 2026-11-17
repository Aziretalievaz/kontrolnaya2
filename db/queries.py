

CREATE_USERS_TABLE = '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER NOT NULL UNIQUE,
        username TEXT
    )
'''


CREATE_TASKS_TABLE = '''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        is_completed BOOLEAN NOT NULL DEFAULT 0,

        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
'''


# CRUD



GET_USER_BY_TG_ID = 'SELECT * FROM users WHERE telegram_id = ?'

INSERT_USER = 'INSERT OR IGNORE INTO users (telegram_id, username) VALUES (?, ?)'




GET_ALL_TASKS = 'SELECT * FROM tasks WHERE user_id = ?'

GET_TASK_BY_ID = 'SELECT * FROM tasks WHERE id = ?'

INSERT_TASK = 'INSERT INTO tasks (user_id, title) VALUES (?, ?)'

UPDATE_TASK_STATUS = 'UPDATE tasks SET is_completed = 1 WHERE id = ? AND user_id = ?'


GET_TASKS_WITH_USER = '''
    SELECT t.id,
           t.title,
           t.is_completed,
           u.telegram_id
    FROM tasks AS t
    INNER JOIN users AS u
        ON u.id = t.user_id
    WHERE u.telegram_id = ?
    ORDER BY t.id
'''

GET_TASKS_STATS = '''
    SELECT user_id,
           COUNT(*) AS total,
           SUM(is_completed) AS completed,
           COUNT(*) - SUM(is_completed) AS not_completed
    FROM tasks
    WHERE user_id = ?
    GROUP BY user_id
'''