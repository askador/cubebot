import io
import zipfile
from pathlib import Path
from telebot import TeleBot

BOT_TOKEN="1173133322:AAF7x3n3VRtNbA4UPBkhbVf_FY3IdejB3j8"
ISSUE_CHAT=-1001534253038

bot = TeleBot(BOT_TOKEN)
LOGS_PATH = Path(f'/home/askador/CubeBot/logs_{bot.get_me().username}')
ZIP_FILE_PATH = LOGS_PATH.joinpath('logs.zip')

def create_zip_file():
    in_memory = io.BytesIO()
    logs_files = LOGS_PATH.glob('*.log')
    with zipfile.ZipFile(in_memory, mode="w") as zip_obj:
        for log_file in logs_files:
            zip_obj.write(log_file)

    with open(ZIP_FILE_PATH, 'wb') as f:
        f.write(in_memory.getvalue())
        


def send_logs_archive():
    create_zip_file()
    bot.send_document(ISSUE_CHAT, open(ZIP_FILE_PATH, 'rb'))


def main():
    send_logs_archive()

main()