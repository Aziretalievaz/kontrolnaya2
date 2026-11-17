from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from db.users import get_user, create_user
from db.tasks import get_tasks, get_task, create_task
from db.tasks import complete_task, get_tasks_with_user, get_tasks_stats


router = Router()

class TaskStates(StatesGroup):
    waiting_title = State()
    waiting_task_number = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user = create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username or "Аноним"
    )

    await message.answer(
        f"Привет, {message.from_user.full_name}! Я твой личный трекер задач."
    )

    print(f"Пользователь {message.from_user.full_name} написал команду /start!")


@router.message(Command("add"))
async def cmd_add(message: Message, state: FSMContext):
    await state.set_state(TaskStates.waiting_title)
    await message.answer("Введите название задачи:")


@router.message(TaskStates.waiting_title)
async def save_task(message: Message, state: FSMContext):
    user = get_user(telegram_id=message.from_user.id)

    create_task(
        user_id=user["id"],
        title=message.text
    )

    await message.answer("Задача успешно добавлена!")

    await state.clear()

@router.message(Command("tasks"))
async def cmd_tasks(message: Message):
    tasks = get_tasks_with_user(
        telegram_id=message.from_user.id
    )

    if not tasks:
        await message.answer("У тебя пока нет задач.")
        return

    text = "Твои задачи:\n\n"

    for i, task in enumerate(tasks, 1):
        status = "ГОТОВО" if task["is_completed"] else "НЕ ВЫПОЛНЕНО"
        text += f"{i}. {status} {task['title']}\n"

    await message.answer(text)


@router.message(Command("done"))
async def cmd_done(message: Message, state: FSMContext):
    await state.set_state(TaskStates.waiting_task_number)
    await message.answer("Введите номер задачи, которую нужно выполнить:")


@router.message(TaskStates.waiting_task_number)
async def finish_task(message: Message, state: FSMContext):
    user = get_user(telegram_id=message.from_user.id)

    tasks = get_tasks_with_user(telegram_id=message.from_user.id)

    task_number = int(message.text)

    if task_number < 1 or task_number > len(tasks):
        await message.answer("Задача с таким номером не найдена.")
        await state.clear()
        return

    task = tasks[task_number - 1]

    complete_task(
        task_id=task["id"],
        user_id=user["id"]
    )

    await message.answer("Задача отмечена как выполненная.")
    await state.clear()


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    user = get_user(telegram_id=message.from_user.id)

    stats = get_tasks_stats(user_id=user["id"])

    if not stats:
        await message.answer("У тебя пока нет задач.")
        return

    await message.answer(
        f"Статистика твоих задач:\n\n"
        f"Всего задач: {stats['total']}\n"
        f"Выполнено: {stats['completed']}\n"
        f"Не выполнено: {stats['not_completed']}"
    )    

