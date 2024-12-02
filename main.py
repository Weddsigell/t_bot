import os
import ptbot
from dotenv import load_dotenv
from pytimeparse2 import parse


def message_processing(chat_id, str):
    seconds = parse(str)
    if  seconds == None:
        return bot.send_message(chat_id, "Не понимаю на сколько ставить таймер!?")
    create_timer(chat_id, seconds)


def create_timer(chat_id, seconds):
    message_id = first_message(seconds, chat_id)
    bot.create_countdown(seconds, editing_message, chat_id=chat_id, time=seconds, message_id=message_id)
    bot.create_timer(seconds+0.3, time_is_up, chat_id=chat_id)


def first_message(seconds, chat_id):
    str = f"Осталось {seconds} секунд!\n{render_progressbar(seconds, 0)}"
    return bot.send_message(chat_id, str)


def editing_message(secs_left, chat_id, time, message_id):
    str = f"Осталось {secs_left} секунд!\n{render_progressbar(time, time - secs_left)}"
    bot.update_message(chat_id, message_id, str)


def time_is_up(chat_id):
    bot.send_message(chat_id, "Время вышло!")


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def main():
    load_dotenv()
    global bot
    tg_tоken = os.environ['TG_TOKEN']
    bot = ptbot.Bot(tg_tоken)
    bot.reply_on_message(message_processing)
    bot.run_bot()


if __name__ == '__main__':
    main()