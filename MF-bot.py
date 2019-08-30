# -*- coding: utf-8 -*-
from multi_fandom.start import *
import multi_fandom.start as start
from multi_fandom.elite import *
from multi_fandom.complicated_commands import *
from multi_fandom.boss_commands import *
from multi_fandom.standart_commands import *
import multi_fandom.standart_commands as standart_commands
from multi_fandom.reactions import *
from multi_fandom.other import *
import multi_fandom.log as l

# Печаем переменные из всех файлов, чтобы было понятно, что не зря импортируем все эти модули
print(start_work)
print(elite_work)
print(complicated_commands_work)
print(boss_commands_work)
print(standart_commands_work)
print(reactions_work)
print(other_work)

log = l.Loger(l.LOG_TO_CONSOLE)
try:
    #  telebot.logger.setLevel("DEBUG")  # Иногда помогает, но обычно не нужна
    bot.polling()  # Запуск бота
    start.log = log
    standart_commands.log = log
except Exception as e:
    print(e)
input()  # Чтобы при запуске с консоли при вылете можно было узнать причину
# TODO провокацио-голосовашки и оск-голосовашки
# TODO голосовашки, адапт-голосовашки и мульти-голосовашки ломаются, когда на них жмакает чел со смайликом в нике
# TODO Пусть бот пишет в консоли, какая функция и когда вызвана
# TODO Антифлуд механизм
