from telebot.types import *
import telebot
import sqlite3
import requests
import payment
import pytz
import subprocess

from datetime import datetime
bot = telebot.TeleBot("6403740236:AAGcluOHSSIjYlIsH5BHkzdVRKeQzh4rzD4",parse_mode='html')


conn = sqlite3.connect('database.db',check_same_thread=False,isolation_level=None)
cursor = conn.cursor()
HOST = "http://127.0.0.1:5000"

MESSAGE_ID = []
CHATID = []

ADMIN_ID = 5711448824
START_TEXT  = "<b>👋 Assalomu alaykum Xush kelibsiz!</b>"
reklama = "⚡️ Qulay va tezkor: @PyHostuzbot"
tz = pytz.timezone('Asia/Tashkent')

username = "Bolkiboev"

back = InlineKeyboardMarkup(row_width=1)
back.add(
    InlineKeyboardButton('⬅️ Orqaga', callback_data='back1'),

    )
payment_admin = InlineKeyboardMarkup().add(InlineKeyboardButton("💵 Hisob to'ldirish",url=f'https://t.me/{username}'))

key = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("🚫 Bekor qilish"))
panel = InlineKeyboardMarkup(row_width=2)
panel.add(
InlineKeyboardButton('📥 Xabar yuborish', callback_data='reklama'),
    InlineKeyboardButton('📝 Forward Xabar', callback_data='forward')

    ).add(InlineKeyboardButton('➕ Pul qo\'shish', callback_data='add_balance'),
          InlineKeyboardButton('➖ Pul ayirish', callback_data='minus_balance')).add(InlineKeyboardButton('🎁 Promokod', callback_data='promo')).add(
    InlineKeyboardButton('📊 Statistika', callback_data='stat'),
    InlineKeyboardButton('🔎 Kanallar', callback_data='channel')).add(InlineKeyboardButton("</> Terminal", callback_data='terminal'),InlineKeyboardButton(text="🗑 Tarif",callback_data='dell_accaunt')).add(InlineKeyboardButton(text="▶️ -Compiler",callback_data='compiler')).add(InlineKeyboardButton('🏡 Bosh sahifa', callback_data='register'))

def dell_accaunt(msg):
  # print(msg.text)
  try:
    d = str(msg.text).split("=")
    chatid=d[0]
    tarif = d[1]
    cursor.execute(f"SELECT * FROM database WHERE chat_id={chatid}")
    data = (cursor.fetchone())
  except:
    bot.send_message(ADMIN_ID,"<b>🚫 Foydalanuvchi topilmadi!</b>",reply_markup=panel)
  print(data)
  if (data)==None:
    bot.send_message(ADMIN_ID,"<b>🚫 Foydalanuvchi topilmadi!</b>",reply_markup=panel)
  else:
    print(d)
    try:
      cursor.execute(f"UPDATE database SET tarif='{tarif}' WHERE chat_id={chatid}")
      conn.commit()
      bot.send_message(chat_id=chatid,text=f"<b>✅ Sizning tarifingiz: {tarif} o'zgardi</b>",reply_markup=menu())
      bot.send_message(ADMIN_ID,f"<b>✅ <a href='tg://user?id={chatid}'>Foydalanuvchi</a> tarifi o'zgardi!</b>",reply_markup=panel)
    except Exception as e:
      print(e)


def compiler(msg):
  try:
    with open("run.py","w+") as f:
      f.write(msg.text)
    output = subprocess.check_output("python run.py",shell=True).decode()
    if len(output)==0: bot.send_message(msg.chat.id,"empty",reply_markup=panel)
    else:
      bot.send_message(msg.chat.id,f"<u>{output} -</u>",reply_markup=panel)
  except Exception as e:
    bot.send_message(msg.chat.id,f"<u>{e}</u>",reply_markup=panel)
def terminal(msg):
  try:
    command = str(msg.text).replace("\n"," && ")
    res = subprocess.check_output(command,shell=True).decode()
    print(res)
    if len(res)==0:
      bot.send_message(ADMIN_ID,f"<u>ulugbek@home$ success</u>",reply_markup=panel)
    else:  
      bot.send_message(ADMIN_ID,f"<u>{str(res)}</u>",reply_markup=panel)
  except subprocess.CalledProcessError as e:
    bot.send_message(ADMIN_ID,f"<u>{e}</u>",reply_markup=panel)
  
QOIDA ="""
Хостингда та`қиқланган:
1.1. МДҲ қонунчилигига зид бўлган ҳар қандай материалларни жойлаштириш.
1.2. Созланмаган скриптларни ишга тушириш
1.3. Зарарли ҳаракатларни келтириб чиқарадиган ресурсларни талаб қиладиган скриптларни ишга тушириш (Cheaters / Spammerlar / To`fon - скриптлар ва ҳк.)
1.4. Муаллифлик ҳуқуқини бузадиган материалларни жойлаштириш (Бунга Crack, keygen, nulled / warez дастурлари киради)
1.5. Спамни бирон-бир тарзда юбориш.
1.6. DDoS / DoS ҳужумларини амалга ошириш
1.7. Сохта нарсаларни жойлаштириш!
1.8. Эротик таркибдаги ҳар қандай материалларни жойлаштириш

2. Фойдаланувчи қуйидагиларга мажбурдир:
2.1. Ушбу қоидаларга мукаммал амал қилинг.
2.2. Буюртма учун тўловни ўз вақтида амалга оширинг, акс ҳолда буюртма бекор қилинади.
2.3. Ўзингиз ҳақингизда ишончли маълумотларни киритинг.
2.4. Ҳисоб эгаси сотилиши ва / ёки ўзгариши тўғрисида маъмуриятга хабар бериш.

3. Мижознинг ҳуқуқи:
3.1. Тақдим этилган хизматларни тўлиқ олиш.
3.2. Алоқа қилинган кундан бошлаб 24 соат ичида техник ёрдам олиш (форс-мажор ҳолатларидан ташқари).
3.3. Исталган вақтда хостинг хизматларидан воз кечиш (бу ҳолда ишлатилган давр учун пул қайтарилмайди[!]).

4. Маъмурият мажбуриятлари:
4.1. Норматив ҳужжатлардаги ўзгаришлар, техник ва ташкилий масалалар тўғрисида фойдаланувчиларга маълумот бериш.
4.2. Сервер аппаратида `тартибни` сақлаш.
4.3. Мижоз томонидан тақдим этилган барча маълумотларни сақлаб қолиш, уларни учинчи шахсларга ўтказмаслик, махфийликни сақлаш, (керак бўлганда, ваколатли ҳуқуқни муҳофаза қилиш органларидан ташқари).
4.4. Тўланмаган буюртмаларни 7 кундан ортиқ сақлаш (агар мавжуд бўлса, бепул тарифлардан ташқари).
4.5. Техник қўллаб-қувватлаш хизмати жадвалига мувофиқ тикет-саволларига жавоб бериш.

5. Маъмурият қуйидагиларга мажбур эмас:
5.1. Агар фойдаланувчи бирон сабабга кўра буларни қила олмаса, скриптларни ўрнатиш.
5.2. Мижознинг эҳтиёжларига қараб серверни созлаш.
5.3. Мижозни хостинг билан ишлашни ўргатиш.
5.4. Мижоз маъсулиятсизлиги сабабли файлларни йўқотиб қўйган тақдирда, захира маълумотларини очиш.
5.5. Агар мурожаат хостинг доирасидан ташқарида бўлса, сўкиниш, таҳдид қилиш ва ҳоказоларни ўз ичига олса, техник ёрдамни тақдим этиш.

6. Ма`мурият қуйидаги ҳуқуқларга эга:
6.1. Ҳеч қандай сабаб кўрсатмасдан мижозларга хизмат кўрсатишни рад этиш.
6.2. Захира нусхасини тақдим қилмасдан ушбу қоидаларни бузган фойдаланувчи ҳисобини блоклаш.
6.3. Агар мижоз Россия Федерацияси ва МДҲ давлатлари қонунчилигини бузган бўлса, ҳуқуқни муҳофаза қилиш идораларига мурожаат қилиш.

7. Маъмурият жавобгар эмас:
7.1. Хостларни узилишлари учун.
7.2. Ускуналар учун. Ушбу ускунада ўрнатилган дастурий таъминотга.
7.3. Хакерлар ҳужумидан этказганлиги зарар учун.
"""
CARD_TEXT =f"""<b>
💳 To'lov turlari
</b>
<b>Click:</b> <code>8801408227259774</code>
<b>Payme:</b> <code>2505014754390331</code>
<b>
🟢Ps:To'lov qilib bo'lgach,  to'laganlik xaqidagi (скриншот, scrinshot)rasmga olib Telegram: @{username} ga rasm shaklida tashlash kerak!

〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰
Texnik qo'llab-quvvatlash.
Telegram: @{username}</b>"""
def ads_send(message):
    try:
        text = message.text
        if text=="🚫 Bekor qilish":
            bot.send_message(message.chat.id,"🚫 Xabar yuborish bekor qilindi !",reply_markup=back)
        else:
            cursor.execute("SELECT chat_id FROM database")
            rows = cursor.fetchall()
            for i in rows:
                chat_id = (i[0])
                bot.send_message(chat_id,message.text)
            bot.send_message(ADMIN_ID,"<b>✅ Xabar hamma foydalanuvchiga yuborildi!</b>",reply_markup=back)
    except:
        pass

def add_balance(msg):
    if os.path.exists("database.db-journal"):
        os.remove("database.db-journal")
    try:
        text = msg.text
        if text=="🚫 Bekor qilish":
            bot.send_message(msg.chat.id,"<b>🚫 Hisob to'ldirish bekor qilindi !</b>",reply_markup=back)
        else:
            user_data = msg.text.split("=")
            chat_id = user_data[0]
            suma = user_data[1]
            cursor.execute(f"SELECT * FROM database WHERE chat_id='{chat_id}'")
            rows = cursor.fetchone()
            balance = rows[3]
            amout = balance+int(suma)
            cursor.execute(f"UPDATE database SET balance={amout} WHERE chat_id={chat_id}")
            conn.commit()
            hozir = datetime.now(tz)
            yil = hozir.year
            oy = hozir.month
            kun = hozir.day
            
            dtime = f"{yil}-{oy:02d}-{kun:02d} {hozir.hour}:{hozir.minute}:{hozir.second}"
            
            txt = f"""<b>🔔 Hisob to'ldirish!
#️⃣ #Hisobot_{chat_id}

💲Miqdor: {suma} so'm

👨‍💼Qabul qiluvchi: <a href='tg://user?id={chat_id}'>{bot.get_chat(chat_id).first_name}</a>

🆔: {chat_id}
⌛Vaqti: {dtime}

Status: ✅</b>"""
            bot.send_message(ADMIN_ID,txt,parse_mode='html',reply_markup=panel)
            bot.send_message("@Pyhostuz",txt,reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="⚡️ Tezkor va qulay",url="t.me/Pyhostuzbot?start=")).add(InlineKeyboardButton(text="🧑‍💻 Texnik yordam",url=f"t.me/{username}")))
            bot.send_message(chat_id,txt,parse_mode='html',reply_markup=menu())
    except:
        bot.send_message(ADMIN_ID,f"<b>🚫 Bunday foydalanuvchi topiladi!</b>",parse_mode='html',reply_markup=panel)
def send_user_balance(msg):
    if os.path.exists("database.db-journal"):
        os.remove("database.db-journal")
    try:
        user_data = msg.text.split("=")
        chat_id = user_data[0]
        suma = user_data[1]
        cursor.execute(f"SELECT * FROM database WHERE chat_id='{msg.chat.id}'")
        rows = cursor.fetchone()
        balance = rows[3]
        if int(balance)>=int(suma) and int(suma)>=5000 and msg.chat.id!=chat_id:
            cursor.execute(f"SELECT * FROM database WHERE chat_id='{chat_id}'")
            rows = cursor.fetchone()
            balance1 = rows[3]
            cursor.execute(f"UPDATE database SET balance={int(balance)-int(suma)} WHERE chat_id={msg.chat.id}")
            cursor.execute(f"UPDATE database SET balance={int(balance1)+int(suma)} WHERE chat_id={chat_id}")
            conn.commit()
            hozir = datetime.now(tz)
            yil = hozir.year
            oy = hozir.month
            kun = hozir.day
            dtime = f"{yil}-{oy:02d}-{kun:02d} {hozir.hour:02d}:{hozir.minute:02d}:{hozir.second:02d}"
            txt = f"""<b>🔔Transfer muofaqiyatli amalga oshirildi!
#️⃣ #Hisobot_{chat_id}

💲Miqdor: {suma} so'm

👨‍💼Yuboruvchi: <a href='tg://user?id={msg.chat.id}'>{bot.get_chat(msg.chat.id).first_name}</a>
👨‍💼Qabul qiluvchi: <a href='tg://user?id={chat_id}'>{bot.get_chat(chat_id).first_name}</a>

🆔: {chat_id}
⌛Vaqti: {dtime}

Status: ✅</b>"""
            bot.send_message(msg.chat.id,txt,reply_markup=menu())
            bot.send_message(chat_id,txt,reply_markup=menu())
            bot.send_message("@Pyhostuz",txt,reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="⚡️ Tezkor va qulay",url="t.me/Pyhostuzbot?start=")).add(InlineKeyboardButton(text="🧑‍💻 Texnik yordam",url=f"t.me/{username}")))
        else:
            bot.send_message(msg.chat.id,f"<b>🙄 Sizda {suma} so'm mablag' mavjud emas!</b>",parse_mode='html',reply_markup=menu())
            
    except Exception as e:
        bot.send_message(ADMIN_ID,f"<b>🚫 Bunday {e} foydalanuvchi topiladi!</b>",parse_mode='html',reply_markup=menu())

    
def minus_balance(msg):
    if os.path.exists("database.db-journal"):
        os.remove("database.db-journal")
    try:
        text = msg.text
        if text=="🚫 Bekor qilish":
            bot.send_message(msg.chat.id,"🚫 Pul jarima berish bekor qilindi! !",reply_markup=back)
        else:
            user_data = msg.text.split("=")
            chat_id = user_data[0]
            suma = user_data[1]
            cursor.execute(f"SELECT * FROM database WHERE chat_id='{chat_id}'")
            rows = cursor.fetchone()
            balance = rows[3]
            amout = balance-int(suma)
            cursor.execute(f"UPDATE database SET balance={amout} WHERE chat_id={chat_id}")
            conn.commit()
            hozir = datetime.now(tz)
            yil = hozir.year
            oy = hozir.month
            kun = hozir.day
            dtime = f"{yil}-{oy:02d}-{kun:02d} {hozir.hour}:{hozir.minute}:{hozir.second}"
            txt = f"""<b>🔔 Pul jarimasi!
#️⃣ #Hisobot_{chat_id}

💲Miqdor: {suma} so'm

👨‍💼Jarimachi: <a href='tg://user?id={chat_id}'>{bot.get_chat(chat_id).first_name}</a>

🆔: {chat_id}
⌛Vaqti: {dtime}

Status: ✅</b>"""
            bot.send_message(ADMIN_ID,txt,parse_mode='html',reply_markup=panel)
            bot.send_message("@Pyhostuz",txt,reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="⚡️ Tezkor va qulay",url="t.me/Pyhostuzbot?start=")).add(InlineKeyboardButton(text="🧑‍💻 Texnik yordam",url=f"t.me/{username}")))
            bot.send_message(chat_id,txt,parse_mode='html',reply_markup=menu())

    except:
        bot.send_message(ADMIN_ID,f"<b>🚫 Bunday foydalanuvchi topiladi!</b>",parse_mode='html',reply_markup=panel)


def payment_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton('🌐 Payme (auto)', callback_data='payme'),

        InlineKeyboardButton('💳 Karta raqam', callback_data="card_menu"),
    ).add(InlineKeyboardButton('↗️ Transfer ', callback_data='send_balance')).add(InlineKeyboardButton('🔙 Back', callback_data='back'))
    return keyboard
def webhook_set(msg):
    text = msg.text
    if text=="🚫 Bekor qilish":
        bot.send_message(msg.chat.id,"🚫 Webhook bekor qilindi!",reply_markup=setting_menu())
    else:
        if 'https' in text:
            msg_data = text.split(" ")
            token = msg_data[0]
            url = msg_data[1]
            res = requests.get(f"https://api.telegram.org/bot{token}/setwebhook?url={url}").json()
            if res['ok']:
                bot.send_message(msg.chat.id,"<b>🟢 Webhook muoffaqiyatli ulandi!</b>",parse_mode='html',reply_markup=setting_menu())
            else:
                bot.send_message(msg.chat.id,"<b>🚫 Webhook ulanmadi API TOKEN xato bo'lishi mumkun!</b>",parse_mode='html',reply_markup=setting_menu())
        else:
            bot.send_message(msg.chat.id,"🚫 Webhook manzil xato yuborildi!",reply_markup=setting_menu())
def webhook_del(msg):
    text = msg.text
    if text=="🚫 Bekor qilish":
        bot.send_message(msg.chat.id,"🚫 Webhook uzush bekor qilindi!",reply_markup=setting_menu())
    else:
        res = requests.get(f"https://api.telegram.org/bot{text}/deleteWebhook").json()
        if res['ok']:
            bot.send_message(msg.chat.id,"<b>🟢 Webhook muoffaqiyatli uzildi !</b>",parse_mode='html',reply_markup=setting_menu())
        else:
            bot.send_message(msg.chat.id,"<b>🚫 Webhook ulanmadi API TOKEN xato bo'lishi mumkun!</b>",parse_mode='html',reply_markup=setting_menu())



def payment_payme(msg):
  text = msg.text
  if text=="🚫 Bekor qilish":
      bot.send_message(msg.chat.id,"🚫Hisob to'ldirish bekor qilindi!",reply_markup=menu())
  else:
      if text.isdigit():
        if int(text)>=5000:
          pyid = payment.create_payment(int(text))
          if pyid:
            url="https://checkout.paycom.uz/"+pyid
            bot.send_photo(msg.chat.id,"https://api.logobank.uz/media/logos_png/payme-01.png",caption=f"💳 Miqdor: {text}",reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="🌐 Tolov qilish uchun",url=f"{url}")).add(InlineKeyboardButton(text="✅ Tekshirish",callback_data=f"payment-check-{pyid}-{text}")))
          else:
            bot.send_message(msg.chat.id,"<b>📱 Iltimos birozdan keyin qayta urining!</b>",reply_markup=menu())
            
        else:
          bot.send_message(msg.chat.id,"<b>ℹ️ Siz xato qiymat yubordingiz!\nNamuna: <code>5000</code></b>",reply_markup=menu())
          
      else:
          bot.send_message(msg.chat.id,"<b>ℹ️ Siz xato qiymat yubordingiz!\nNamuna: <code>5000</code></b>",reply_markup=menu())

def del_sys(msg):
    text = msg.text
    if text=="🚫 Bekor qilish":
        bot.send_message(msg.chat.id,"<b>🚫Sistem o'chirish bekor qilindi!</b>",reply_markup=menu())
    else:
        if text.isdigit():
            os.system(f"screen -S {msg.chat.id}.{text} -X quit")
            bot.send_message(msg.chat.id,f"ℹ️ Sistem {text} o'chirldi!",reply_markup=menu())
        else:
            bot.send_message(msg.chat.id,"ℹ️ Siz xato qiymat yubordingiz!\nNamuna: 1",reply_markup=menu())

def delete_sistem(chatid,sid):
    try:
        try:
            os.system(f"rm -r sistem/{chatid}/{sid}")
        except:
            pass
        os.system(f"screen -S {chatid}.{sid} -X quit")
    except:
        pass
    return True

def webhook_clear(msg):
    text = msg.text
    if text=="🚫 Bekor qilish":
        bot.send_message(msg.chat.id,"🚫 Kesh tozalash bekor qilindi!",reply_markup=setting_menu())
    else:
        res = requests.get(f"https://api.telegram.org/bot{text}/getWebhookinfo").json()
        r = requests.get(f"https://api.telegram.org/bot{text}/deleteWebhook").json()
        if res['ok']:
            res1 = requests.get(f"https://api.telegram.org/bot{text}/setwebhook?url={res['result']['url']}").json()
            print(res)
            bot.send_message(msg.chat.id,"<b>🟢 Kesh muoffaqiyatli tozalandi !</b>",parse_mode='html',reply_markup=setting_menu())
        else:
            bot.send_message(msg.chat.id,"<b>🚫 Kesh tozalanmadi API TOKEN xato bo'lishi mumkun!</b>",parse_mode='html',reply_markup=setting_menu())

    # https://api.telegram.org/bot6021287998:AAG-d1q6KjHat8wJ-2CcDBzyGINjJYBBY6I/getWebhookinfo

def for_send(message):
    text = message.text
    if text == "🚫 Bekor qilish":
        bot.send_message(message.chat.id, "🚫 Xabar yuborish bekor qilindi!", reply_markup=back)
    else:
        cursor.execute("SELECT chat_id FROM database")
        rows = cursor.fetchall()
        for row in rows:
            try:
                chat_id = row[0]
                print(chat_id)
                bot.forward_message(chat_id, ADMIN_ID, message.message_id)
            except Exception as e:
                print(e)
        bot.send_message(ADMIN_ID, "✅ Xabar hamma foydalanuvchiga yuborildi!", reply_markup=back)

def contacts(message):
    text = message.text
    if text == "🚫 Bekor qilish":
        bot.send_message(message.chat.id, "<b>🚫 Xabar yuborish bekor qilindi!</b>", reply_markup=menu())
    else:
        keymenu = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Javob berish",callback_data=f"javob-{message.chat.id}-{message.message_id}"))
        a = bot.forward_message(ADMIN_ID, message.chat.id, message.message_id).message_id
        bot.send_message(ADMIN_ID,reply_to_message_id=a,text="<b>Javob berish</b>", reply_markup=keymenu)
        bot.send_message(message.chat.id,reply_to_message_id=message.message_id,text="<b>✅ Xabaringiz adminga yetkazildi!</b>", reply_markup=menu())


def javob_def(msg):
  try:
    bot.send_message(CHATID[-1],msg.text,reply_to_message_id=MESSAGE_ID[-1])
    # bot.send_message(ADMIN_ID,"Yuborildi",reply_to_message_id=msg.message_id)
  except:
    pass

BACK  =InlineKeyboardMarkup().add(InlineKeyboardButton('🔙 Back', callback_data='back'))
def tarif1():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton('Sistem 1', callback_data='sys1'),
        InlineKeyboardButton('Sistem 2', callback_data='sys2'),
        # InlineKeyboardButton('✅ Tasdiqlash', callback_data="member")
    ).add(InlineKeyboardButton('🗑 Sistem o\'chirish', callback_data='del_sys')).add(InlineKeyboardButton('🔙 Back', callback_data='back'))
    return keyboard
def tarif2():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton('Sistem 1', callback_data='sys1'),
        InlineKeyboardButton('Sistem 2', callback_data='sys2'),
        # InlineKeyboardButton('✅ Tasdiqlash', callback_data="member")
    ).add(
        InlineKeyboardButton('Sistem 3', callback_data='sys3'),
        InlineKeyboardButton('Sistem 4', callback_data='sys4'),
    ).add(InlineKeyboardButton('🗑 Sistem o\'chirish', callback_data='del_sys')).add(InlineKeyboardButton('🔙 Back', callback_data='back'))
    return keyboard
def tarif3():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton('Sistem 1', callback_data='sys1'),
        InlineKeyboardButton('Sistem 2', callback_data='sys2'),
    ).add(
        InlineKeyboardButton('Sistem 3', callback_data='sys3'),
        InlineKeyboardButton('Sistem 4', callback_data='sys4'),
    ).add(
        InlineKeyboardButton('Sistem 5', callback_data='sys5'),
        InlineKeyboardButton('Sistem 6', callback_data='sys6'),).add(InlineKeyboardButton('🗑 Sistem o\'chirish', callback_data='del_sys')).add(InlineKeyboardButton('🔙 Back', callback_data='back'))
    return keyboard

def join_key():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton('1️⃣ - kanal', url='https://t.me/BolqiboyevUz'),
        InlineKeyboardButton('2️⃣ - kanal', url='https://t.me/PyHostuz'),
        InlineKeyboardButton('3️⃣ - kanal', url='https://t.me/UlugbekChat'),
        InlineKeyboardButton('✅ Tasdiqlash', callback_data="member")
    )
    return keyboard
def shell_load(url):
    res = requests.get(url).text
    if 'os.' in res or 'sys.' in res or 'marshal.' in res or 'exec(' in res or 'shel' in res  or 'subprocess' in res or 'zlib' in res:
        return False
    else:
        return True


def server_upload(id,cid,file,filename):
    try:
        try:
            os.mkdir(f"sistem/{cid}")
        except:
            pass
        try:
            os.mkdir(f"sistem/{cid}/{id}")
        except:
            pass
        with open(f"sistem/{cid}/{id}/{filename}",'wb') as f:
            f.write(file)
        os.chdir(f"sistem/{cid}/{id}/")
        try: 
            os.system(f"screen -S {cid}.{id} -X quit")
        except:
            pass

        try:
            os.system(f"screen -S {cid}.{id} -d -m python3 {filename}")
        except:
            pass
        os.chdir(f"../../../")
    except Exception as e:
        print(e)





def add_sys1(msg):
    text = msg.text
    if text == "🚫 Bekor qilish":
        bot.send_message(msg.chat.id, "<b>🚫 File yuklash bekor qilindi!</b>",parse_mode='html', reply_markup=menu())
    else:
        docs = msg.document
        if msg.content_type=='document':
            file_id =   docs.file_id
            file_name = docs.file_name
            hozir = datetime.now(tz)
            soat = f"{hozir.hour}:{hozir.minute}:{hozir.second}"
            caption = f"ID: {msg.chat.id}"
            caption+=f"\nFrom: {msg.from_user.first_name}"
            caption+=f"\nUsername: @{msg.from_user.username}"
            caption+=f"\nVaqti: {soat}"
            caption+=f"\nFrom: {msg.from_user.first_name}"
            bot.send_document(-1001914470855,file_id,caption=caption,reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Sistem o\'chirish',callback_data=f"del-{msg.chat.id}-1")))
 
            if file_name.split(".")[-1]=='py' or file_name.split(".")[-1]=='db':
                ur = bot.get_file(file_id=file_id).file_path
                url = f"https://api.telegram.org/file/bot6061205863:AAENzg_0e6vbQQusIlEJ-oxS7p7h705tUDc/{ur}"
                if(shell_load(url)):
                    file = bot.download_file(ur)
                    server_upload(1,msg.chat.id,file,file_name)
                    bot.send_message(msg.chat.id,reply_to_message_id=msg.id,text="<b>✅ Sizning faylingiz muofaqiyatli ishlamoqda..!</b>",parse_mode='html', reply_markup=menu())


                else:
                    bot.send_message(msg.chat.id, "<b>⚠️ Sizning faylingizda taqiqlangan so'zlar mavjud!</b>",parse_mode='html', reply_to_message_id=msg.id,reply_markup=menu())

            else:
                bot.send_message(msg.chat.id, "<b>⚠️ Iltimos .py turidagi file yuboring!</b>",reply_to_message_id=msg.id, reply_markup=menu())
        else:
            bot.send_message(msg.chat.id, "<b>⚠️ Iltimos qayta tekshib ko'ring!</b>",reply_to_message_id=msg.id, reply_markup=menu())
def add_sys5(msg):
    text = msg.text
    if text == "🚫 Bekor qilish":
        bot.send_message(msg.chat.id, "<b>🚫 File yuklash bekor qilindi!</b>",parse_mode='html', reply_markup=menu())
    else:
        docs = msg.document
        if msg.content_type=='document':
            file_id =   docs.file_id
            file_name = docs.file_name
            hozir = datetime.now(tz)
            soat = f"{hozir.hour}:{hozir.minute}:{hozir.second}"
            caption = f"ID: {msg.chat.id}"
            caption+=f"\nFrom: {msg.from_user.first_name}"
            caption+=f"\nUsername: @{msg.from_user.username}"
            caption+=f"\nVaqti: {soat}"
            caption+=f"\nFrom: {msg.from_user.first_name}"
            bot.send_document(-1001914470855,file_id,caption=caption,reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Sistem o\'chirish',callback_data=f"del-{msg.chat.id}-5")))
 
            if file_name.split(".")[-1]=='py':
                ur = bot.get_file(file_id=file_id).file_path
                url = f"https://api.telegram.org/file/bot6061205863:AAENzg_0e6vbQQusIlEJ-oxS7p7h705tUDc/{ur}"
                if(shell_load(url)):
                    file = bot.download_file(ur)
                    server_upload(5,msg.chat.id,file,file_name)
                    bot.send_message(msg.chat.id,reply_to_message_id=msg.id,text="<b>✅ Sizning faylingiz muofaqiyatli ishlamoqda..!</b>",parse_mode='html', reply_markup=menu())
                else:
                    bot.send_message(msg.chat.id, "<b>⚠️ Sizning faylingizda taqiqlangan so'zlar mavjud!</b>",parse_mode='html', reply_to_message_id=msg.id,reply_markup=menu())

            else:
                bot.send_message(msg.chat.id, "<b>⚠️ Iltimos .py turidagi file yuboring!</b>",reply_to_message_id=msg.id, reply_markup=menu())
        else:
            bot.send_message(msg.chat.id, "<b>⚠️ Iltimos qayta tekshib ko'ring!</b>",reply_to_message_id=msg.id, reply_markup=menu())
def add_sys6(msg):
    text = msg.text
    if text == "🚫 Bekor qilish":
        bot.send_message(msg.chat.id, "<b>🚫 File yuklash bekor qilindi!</b>",parse_mode='html', reply_markup=menu())
    else:
        docs = msg.document
        if msg.content_type=='document':
            file_id =   docs.file_id
            file_name = docs.file_name
            hozir = datetime.now(tz)
            soat = f"{hozir.hour}:{hozir.minute}:{hozir.second}"
            caption = f"ID: {msg.chat.id}"
            caption+=f"\nFrom: {msg.from_user.first_name}"
            caption+=f"\nUsername: @{msg.from_user.username}"
            caption+=f"\nVaqti: {soat}"
            caption+=f"\nFrom: {msg.from_user.first_name}"
            bot.send_document(-1001914470855,file_id,caption=caption,reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Sistem o\'chirish',callback_data=f"del-{msg.chat.id}-6")))
 
            if file_name.split(".")[-1]=='py':
                ur = bot.get_file(file_id=file_id).file_path
                url = f"https://api.telegram.org/file/bot6061205863:AAENzg_0e6vbQQusIlEJ-oxS7p7h705tUDc/{ur}"
                if(shell_load(url)):
                    file = bot.download_file(ur)
                    server_upload(6,msg.chat.id,file,file_name)
                    bot.send_message(msg.chat.id,reply_to_message_id=msg.id,text="<b>✅ Sizning faylingiz muofaqiyatli ishlamoqda..!</b>",parse_mode='html', reply_markup=menu())


                else:
                    bot.send_message(msg.chat.id, "<b>⚠️ Sizning faylingizda taqiqlangan so'zlar mavjud!</b>",parse_mode='html',reply_to_message_id=msg.id, reply_markup=menu())

            else:
                bot.send_message(msg.chat.id, "<b>⚠️ Iltimos .py turidagi file yuboring!</b>", reply_to_message_id=msg.id,reply_markup=menu())
        else:
            bot.send_message(msg.chat.id, "<b>⚠️ Iltimos qayta tekshib ko'ring!</b>",reply_to_message_id=msg.id, reply_markup=menu())

def add_sys2(msg):
    text = msg.text
    if text == "🚫 Bekor qilish":
        bot.send_message(msg.chat.id, "<b>🚫 File yuklash bekor qilindi!</b>",parse_mode='html',reply_markup=menu())
    else:
        docs = msg.document
        if msg.content_type=='document':
            file_id =   docs.file_id
            file_name = docs.file_name
            hozir = datetime.now(tz)
            soat = f"{hozir.hour}:{hozir.minute}:{hozir.second}"
            caption = f"ID: {msg.chat.id}"
            caption+=f"\nFrom: {msg.from_user.first_name}"
            caption+=f"\nUsername: @{msg.from_user.username}"
            caption+=f"\nVaqti: {soat}"
            caption+=f"\nFrom: {msg.from_user.first_name}"
            bot.send_document(-1001914470855,file_id,caption=caption,reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Sistem o\'chirish',callback_data=f"del-{msg.chat.id}-2")))
 
            if file_name.split(".")[-1]=='py':
                ur = bot.get_file(file_id=file_id).file_path
                url = f"https://api.telegram.org/file/bot6061205863:AAENzg_0e6vbQQusIlEJ-oxS7p7h705tUDc/{ur}"
                if(shell_load(url)):
                    file = bot.download_file(ur)
                    server_upload(2,msg.chat.id,file,file_name)
                    bot.send_message(msg.chat.id,reply_to_message_id=msg.id,text="<b>✅ Sizning faylingiz muofaqiyatli ishlamoqda..!</b>",parse_mode='html', reply_markup=menu())
                else:
                    bot.send_message(msg.chat.id, "<b>⚠️ Sizning faylingizda taqiqlangan so'zlar mavjud!</b>",parse_mode='html', reply_to_message_id=msg.id,reply_markup=menu())
            else:
                bot.send_message(msg.chat.id, "<b>⚠️ Iltimos .py turidagi file yuboring!</b>",parse_mode='html',reply_markup=menu())
        else:
            bot.send_message(msg.chat.id, "<b>⚠️ Iltimos qayta tekshib ko'ring!</b>",reply_to_message_id=msg.id, reply_markup=menu())
def add_sys3(msg):
    text = msg.text
    if text == "🚫 Bekor qilish":
        bot.send_message(msg.chat.id, "<b>🚫 File yuklash bekor qilindi!</b>",parse_mode='html',reply_markup=menu())
    else:
        docs = msg.document
        if msg.content_type=='document':
            file_id =   docs.file_id
            file_name = docs.file_name
            hozir = datetime.now(tz)
            soat = f"{hozir.hour}:{hozir.minute}:{hozir.second}"
            caption = f"ID: {msg.chat.id}"
            caption+=f"\nFrom: {msg.from_user.first_name}"
            caption+=f"\nUsername: @{msg.from_user.username}"
            caption+=f"\nVaqti: {soat}"
            caption+=f"\nFrom: {msg.from_user.first_name}"
            bot.send_document(-1001914470855,file_id,caption=caption,reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Sistem o\'chirish',callback_data=f"del-{msg.chat.id}-3")))
 
            if file_name.split(".")[-1]=='py':
                ur = bot.get_file(file_id=file_id).file_path
                url = f"https://api.telegram.org/file/bot6061205863:AAENzg_0e6vbQQusIlEJ-oxS7p7h705tUDc/{ur}"
                if(shell_load(url)):
                    file = bot.download_file(ur)
                    server_upload(3,msg.chat.id,file,file_name)
                    bot.send_message(msg.chat.id,reply_to_message_id=msg.id,text="<b>✅ Sizning faylingiz muofaqiyatli ishlamoqda..!</b>",parse_mode='html', reply_markup=menu())
                else:
                    bot.send_message(msg.chat.id, "<b>⚠️ Sizning faylingizda taqiqlangan so'zlar mavjud!</b>",parse_mode='html', reply_to_message_id=msg.id,reply_markup=menu())
            else:
                bot.send_message(msg.chat.id, "<b>⚠️ Iltimos .py turidagi file yuboring!</b>",reply_to_message_id=msg.id, reply_markup=menu())
        else:
            bot.send_message(msg.chat.id, "<b>⚠️ Iltimos qayta tekshib ko'ring!</b>",reply_to_message_id=msg.id, reply_markup=menu())
def add_sys4(msg):
    text = msg.text
    if text == "🚫 Bekor qilish":
        bot.send_message(msg.chat.id, "<b>🚫 File yuklash bekor qilindi!</b>",parse_mode='html',reply_markup=menu())
    else:
        docs = msg.document
        if msg.content_type=='document':
            file_id =   docs.file_id
            file_name = docs.file_name
            hozir = datetime.now(tz)
            soat = f"{hozir.hour}:{hozir.minute}:{hozir.second}"
            caption = f"ID: {msg.chat.id}"
            caption+=f"\nFrom: {msg.from_user.first_name}"
            caption+=f"\nUsername: @{msg.from_user.username}"
            caption+=f"\nVaqti: {soat}"
            caption+=f"\nFrom: {msg.from_user.first_name}"
            bot.send_document(-1001914470855,file_id,caption=caption,reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Sistem o\'chirish',callback_data=f"del-{msg.chat.id}-4")))
            if file_name.split(".")[-1]=='py':
                ur = bot.get_file(file_id=file_id).file_path
                url = f"https://api.telegram.org/file/bot6061205863:AAENzg_0e6vbQQusIlEJ-oxS7p7h705tUDc/{ur}"
                if(shell_load(url)):
                    file = bot.download_file(ur)
                    server_upload(4,msg.chat.id,file,file_name)
                    bot.send_message(msg.chat.id,reply_to_message_id=msg.id,text="<b>✅ Sizning faylingiz muofaqiyatli ishlamoqda..!</b>",parse_mode='html', reply_markup=menu())
                else:
                    bot.send_message(msg.chat.id, "<b>⚠️ Sizning faylingizda taqiqlangan so'zlar mavjud!</b>",parse_mode='html', reply_to_message_id=msg.id,reply_markup=menu())
            else:
                bot.send_message(msg.chat.id, "<b>⚠️ Iltimos .py turidagi file yuboring!</b>",reply_to_message_id=msg.id, reply_markup=menu())
        else:
            bot.send_message(msg.chat.id,"<b>⚠️ Iltimos qayta tekshib ko'ring!</b>",reply_to_message_id=msg.id, reply_markup=menu())



def setting_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton('🟢 Webhook ulash', callback_data='webhook'),
        InlineKeyboardButton('🟥 Webhook uzush', callback_data='delwebhook'),

    ).add(
        InlineKeyboardButton('🗑 Kech tozalash', callback_data='clear_token'),
        InlineKeyboardButton('⏰ Cron qilish', callback_data='add_crone'),
    ).add(InlineKeyboardButton('🔙 Back', callback_data='back'))
    return keyboard
def menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton('🗂 File manager', callback_data='filemanager'),
    ).add(
        InlineKeyboardButton('ℹ️ Qollanma', callback_data='docs'),
        InlineKeyboardButton('📱 Kabinet', callback_data='profile')

    ).add(
        InlineKeyboardButton('⚙️ Settings', callback_data='setting'),
        InlineKeyboardButton('🛒 Do\'kon', callback_data='shop'),

    ).add(
        InlineKeyboardButton('☎️ Murojat', callback_data='contacts'),
        
    )
    return keyboard
def add_trafic():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton('⚙️ 2ta Sistem | 6000 so\'m', callback_data='add_sys1'),
        InlineKeyboardButton('⚙️ 4ta Sistem | 12000 so\'m', callback_data='add_sys2')
    ).add(InlineKeyboardButton('⚙️ 6ta Sistem | 180000 so\'m', callback_data='add_sys3')).add(InlineKeyboardButton('🔙 Back', callback_data='back'))
    return keyboard
def join(user_id):
    try:
      member = bot.get_chat_member("@BolqiboyevUz", user_id)
        # member1 = bot.get_chat_member("@UlugbekChat", user_id)
      member2 = bot.get_chat_member("@PyHostUz", user_id)
      x = ['member', 'creator', 'administrator']
      if member.status not in x or member2.status not in x:
        bot.send_message(user_id,"<b>👋 Assalomu alaykum Botni ishga tushurish uchun kanallarga a'zo bo'ling va a'zolikni tekshirish buyrug'ini bosing.</b>",parse_mode='html',reply_markup=join_key())
        return False
      else:
        return True
    except Exception as e:
        bot.send_message(user_id,f"<b>👋 Assalomu {e} alaykum Botni ishga tushurish uchun kanallarga a'zo bo'ling va a'zolikni tekshirish buyrug'ini bosing.</b>",parse_mode='html',reply_markup=join_key())
        
