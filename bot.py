import numpy as np
import pandas as pd
import telebot
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent # '/root/bot/bot.py'
print(BASE_DIR) # Обязательная строчка, иначе ошибка АтрибутЕррор
BASE_DIR = BASE_DIR._str

playlist = pd.read_excel(BASE_DIR + '/src/database.xlsx')

def get_track_dataframe(bpm):
    '''
    Возвращает отсортированный по 'bpm' DataFrame.
    
    Args:
        bpm - string, ex."90-100"
    Output:
        pd.DataFrame
    '''
    
    if bpm == '70-80':
        tracks = playlist[(playlist['bpm'] >= 70) & (playlist['bpm'] < 80)]
        
    elif bpm == '80-90':
        tracks = playlist[(playlist['bpm'] >= 80) & (playlist['bpm'] < 90)]
        
    elif bpm == '90-100':
        tracks = playlist[(playlist['bpm'] >= 90) & (playlist['bpm'] < 100)]
        
    elif bpm == '100-110':
        tracks = playlist[(playlist['bpm'] >= 100) & (playlist['bpm'] < 110)]
        
    elif bpm == '110-120':
        tracks = playlist[(playlist['bpm'] >= 110) & (playlist['bpm'] < 120)]
        
    elif bpm == 'Меньше 80': # Устаревшая команда
        tracks = playlist[playlist['bpm'] < 80]
        
    elif bpm == '80-100':
        tracks = playlist[(playlist['bpm'] >= 80) & (playlist['bpm'] < 100)]
    
    elif bpm == '100-120':
        tracks = playlist[(playlist['bpm'] >= 100) & (playlist['bpm'] < 120)]
    
    elif bpm == '120+':
        tracks = playlist[playlist['bpm'] >= 120]
         
    else:
        print('ERROR') #РАЗОБРАТЬ СЛУЧАЙ ЕСЛИ ПОЛЬЗОВАТЕЛЬ ВВОДИТ ЧТО ТО ДРУГОЕ
        return False  
    
    return tracks

def get_track_list(genre, tracks):
    '''
    Возвращает список ссылок на музыклальные композиции.
    По умолчанию - 10 случайных композиций, если их меньше,
    чем 10, вернет сколько есть.
    
    Args:
        genre - string, ex."romantic"
    Output:
        np.ndarray
    '''
    # Lambda-функция учитывает случай, если база не может выдать более 10 треков
    func = lambda n: tracks.sample(10) if n>=10 else tracks.sample(n)
    
    if genre in FIRST_ROW_GENRE_CHOICE:
        tracks = tracks[tracks['genre'] == genre]   
        n = tracks.shape[0]
        tracks = func(n) 
    
        return tracks['link'].values
    
    if genre == 'Случайно':
        
        n = tracks.shape[0]
        tracks = func(n)
        return func(n)['link'].values
    
    if genre == 'disco':
        tracks = tracks[tracks['disco'] == 1]
        n = tracks.shape[0]
        tracks = func(n) 
    
        return tracks['link'].values
 
with open(BASE_DIR + '/sms.txt', encoding='utf-8')as f: # Читаем сообщения бота
    start, help_message = f.read().split('|') # | для разделения сообщений 

with open(BASE_DIR + '/token.txt') as f:
    TOKEN = f.read()

SALUTATION_ROW = ('/start', '/help')

FIRST_ROW_BPM_CHOICE = ('70-80', '80-90', '90-100', '100-110')
SECOND_ROW_BPM_CHOICE = ('110-120','80-100', '100-120', '120+' )

FIRST_ROW_GENRE_CHOICE = ('pop', 'romantic', 'blues')
SECOND_ROW_GENRE_CHOICE = ('Случайно','disco')

TEXT_BPM = FIRST_ROW_BPM_CHOICE + SECOND_ROW_BPM_CHOICE
TEXT_GENRE = FIRST_ROW_GENRE_CHOICE + SECOND_ROW_GENRE_CHOICE


# Инициализация клавиатуры    
keyboardChoiceBpm = telebot.types.ReplyKeyboardMarkup(True)
keyboardChoiceBpm.row(*FIRST_ROW_BPM_CHOICE)
keyboardChoiceBpm.row(*SECOND_ROW_BPM_CHOICE)
keyboardChoiceBpm.row(*SALUTATION_ROW)

keyboardChoiceGenre = telebot.types.ReplyKeyboardMarkup(True)
keyboardChoiceGenre.row(*FIRST_ROW_GENRE_CHOICE)
keyboardChoiceGenre.row(*SECOND_ROW_GENRE_CHOICE)
keyboardChoiceGenre.row(*SALUTATION_ROW) 

itunes = playlist.sample(10)['link'].values #Заглушка
select_bpm = '80-90'

bot = telebot.TeleBot(TOKEN) 

  
## START 
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, start.format(message.chat.first_name, '\u270c\ufe0f'),
                     parse_mode='Markdown')
    bot.send_message(message.chat.id, '`ВЫБЕРИ СКОРОСТЬ`',
                     parse_mode='Markdown',
                     reply_markup=keyboardChoiceBpm) 

    
## HELP
@bot.message_handler(commands=['help'])  
def help_command(message):

    bot.send_message(message.chat.id, help_message, 
                     parse_mode='Markdown')

# MAIN
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    
    if message.text in TEXT_BPM:
        global select_bpm
        select_bpm = message.text
        bot.send_message(message.chat.id, r'`ВЫБЕРИ ЖАНР`',
                         parse_mode='Markdown',
                         reply_markup=keyboardChoiceGenre) 
        
    if message.text in TEXT_GENRE:
        itunes = get_track_list(message.text, get_track_dataframe(select_bpm))
        bot.send_message(message.chat.id, 'Лови',
                         reply_markup=keyboardChoiceBpm) 
        for i in itunes:
            bot.send_audio(message.from_user.id, i)
        
bot.polling(none_stop=True, interval=0)
