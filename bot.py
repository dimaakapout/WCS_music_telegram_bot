import numpy as np
import pandas as pd
import telebot

playlist = pd.read_excel('database.xlsx')

def get_track_dataframe(bpm):
    '''
    Возвращает отсортированный по 'bpm' DataFrame.
    
    Args:
        bpm - string, ex."90-100"
    Output:
        pd.DataFrame
    '''
    
    if bpm == '70-80':
        tracks = playlist[playlist['bpm'] == 70]
        
    elif bpm == '80-90':
        tracks = playlist[playlist['bpm'] == 80]
        
    elif bpm == '90-100':
        tracks = playlist[playlist['bpm'] == 90]
        
    elif bpm == '100-110':
        tracks = playlist[playlist['bpm'] == 100]
        
    elif bpm == '110-120':
        tracks = playlist[playlist['bpm'] == 110]
        
    elif bpm == 'Меньше 80':
        tracks = playlist[playlist['bpm'] < 80]
        
    elif bpm == '80-100':
        tracks = playlist[(playlist['bpm'] >= 80) & (playlist['bpm'] < 100)]
    
    elif bpm == 'Больше 100':
        tracks = playlist[playlist['bpm'] >= 100]
         
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

start_message = '''
Привет, *{0}* \u270c\ufe0f! 
Этот бот умеет подбирать WCS музыку
*по скорости* и *жанру*. 
Следуй моим инструкциям''' + '''
и удачного сампо \u270c\ufe0f!
'''

help_message = '''
*Подписывайся на канал* 

==>   @WCSmusicSAMPO   <==

*Есть идеи как улучшить бота?!*

Пиши на ...@mail.ru
'''

TOKEN = '1350Cw'

SALUTATION_ROW = ('/start', '/help')

FIRST_ROW_BPM_CHOICE = ('70-80', '80-90', '90-100', '100-110')
SECOND_ROW_BPM_CHOICE = ('Меньше 80',"80-100", "Больше 100" )

FIRST_ROW_GENRE_CHOICE = ('pop', 'romantic', 'blues')
SECOND_ROW_GENRE_CHOICE = ('Случайно','disco')

TEXT_BPM = FIRST_ROW_BPM_CHOICE + SECOND_ROW_BPM_CHOICE
TEXT_GENRE = FIRST_ROW_GENRE_CHOICE + SECOND_ROW_GENRE_CHOICE


    
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

bot = telebot.TeleBot(TOKEN) #не забывать перезапускать для обновления бота


## START
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'start_message')#, parse_mode='Markdown')
    bot.send_message(message.chat.id, 'Выбери скорость', reply_markup=keyboardChoiceBpm) 

    
## HELP
@bot.message_handler(commands=['help'])  
def help_command(message):

    bot.send_message(message.chat.id, help_message, parse_mode='Markdown', reply_markup=keyboardChoiceBpm)

# MAIN
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    
    if message.text in TEXT_BPM:
        global select_bpm
        select_bpm = message.text
        bot.send_message(message.chat.id, 'Выбери скорость', reply_markup=keyboardChoiceGenre) 
        
    if message.text in TEXT_GENRE:
        itunes = get_track_list(message.text, get_track_dataframe(select_bpm))
        bot.send_message(message.chat.id, 'лови', reply_markup=keyboardChoiceBpm) 
        for i in itunes:
            bot.send_audio(message.from_user.id, i)
    
    if message.text == 'секретик':
        sticers = bot.get_sticker_set('Hot_Cherry')
        sticer_id = sticers.stickers[1].file_id
        bot.send_sticker(message.chat.id, sticer_id)

bot.polling(none_stop=True, interval=0)