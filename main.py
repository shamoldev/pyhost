import telebot
from telebot.types import *
import sqlite3
from config import *
import payment
from datetime import *
from flask import Flask, request, jsonify

app = Flask(__name__)

bot = telebot.TeleBot("6403740236:AAGcluOHSSIjYlIsH5BHkzdVRKeQzh4rzD4",
                      parse_mode='html')


@app.route('/', methods=['POST', 'GET'])
def webhook():
  if request.method == 'POST':
    data = request.get_json()
    bot.process_new_updates([telebot.types.Update.de_json(data)])
    return "OK"
  else:
    return "Hello, this is your Telegram bot's webhook!"



@bot.message_handler(commands=['cron'])
def crone(msg):
  hozir = datetime.now(tz)
  yil = hozir.year
  oy = hozir.month - 1
  kun = hozir.day
  now = f"2023-{oy}-{kun}"
  cursor.execute("SELECT sistem_time,chat_id FROM database WHERE sistem_time LIKE '%2023%'")
  for i in (cursor.fetchall()):
    if i[0]==now:
      cursor.execute(f"UPDATE database SET tarif='Oddiy' WHERE chat_id={i[1]}")
      cursor.execute(
        f"UPDATE database SET sistem_time='0' WHERE chat_id={i[1]}")
      conn.commit()
      bot.send_message(i[1],"<b>🗓 Sizning tarifingiz vaqti tugadi!</b>",reply_markup=menu())
      for h in range(7):
        requests.get(f"http://127.0.0.1:5000/?chat_id={i[1]}&id={h}")
  bot.send_message(ADMIN_ID,"<b>✅ Qidiruv yakunlandi!</b>")
  return f"Ok"


conn = sqlite3.connect('database.db',
                       check_same_thread=False,
                       isolation_level=None)
cursor = conn.cursor()

cursor.execute(
  "CREATE TABLE IF NOT EXISTS database(id INTEGER PRIMARY KEY,chat_id INTIGER UNIQUE,tarif TEXT,balance INT,register_time TEXT,sistem_time TEXT,crone INT)"
)

conn.commit()


@bot.message_handler(commands=['start'])
def welcome(msg):
  cursor.execute(
          f"UPDATE database SET sistem_time = '2023-10-18' WHERE chat_id = {ADMIN_ID}"
        )
  conn.commit()
  try:
    if os.path.exists("database.db-journal"):
      os.remove("database.db-journal")
    hozir = datetime.now(tz)
    yil = hozir.year
    oy = hozir.month
    kun = hozir.day
    dtime = f"{yil}-{oy:02d}-{kun:02d}"

    cursor.execute(
      "INSERT INTO database(chat_id,tarif,balance,register_time,sistem_time,crone) VALUES (?,?,?,?,?,?)",
      (msg.chat.id, 'Oddiy', 0, dtime, "0", 0))
    conn.commit()
    bot.send_message(
      ADMIN_ID,
      f"<b>👤 Yangi <a href='tg://user?id={msg.chat.id}'>{msg.from_user.first_name}</a> qo'shildi!</b>",
      parse_mode='html')
  except sqlite3.IntegrityError:
    pass
  if (join(msg.chat.id)):
    bot.send_message(msg.chat.id,
                     START_TEXT,
                     parse_mode='html',
                     reply_markup=menu())


@bot.message_handler(content_types='text')
def custom(msg):
  text = msg.text
  cid = msg.chat.id
  if (join(cid)):
    pass
  if msg.text == '/panel' and msg.chat.id == ADMIN_ID:
    bot.send_message(msg.chat.id,
                     "Admin panelga Xush-kelibsiz!",
                     reply_markup=panel)
  if msg.text == '🚫 Bekor qilish':
    bot.delete_message(msg.chat.id, msg.id)
    a = bot.send_message(msg.chat.id, "🏡",
                         reply_markup=ReplyKeyboardRemove()).message_id
    bot.delete_message(msg.chat.id, a)


@bot.message_handler(content_types=['document'])
def send_docs(msg):
  bot.forward_message(ADMIN_ID, msg.chat.id, msg.id)
  #caption=f"Yuklandi: {msg.chat.from_user.first_name}")


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
  try:
    user_id = call.message.chat.id
    data = call.data
    if data == 'member':
      bot.delete_message(user_id, call.message.id)
      if join(user_id):
        bot.send_message(user_id,
                         START_TEXT,
                         parse_mode='html',
                         reply_markup=menu())
      else:
        bot.answer_callback_query(call.id,
                                  "🚫 Siz kanallar obuna bo'lmadingi!",
                                  show_alert=True)
    # print(call)
    if data == 'back' or data == "register":
      bot.edit_message_text(chat_id=user_id,
                            text=START_TEXT,
                            message_id=call.message.id,
                            parse_mode='html',
                            reply_markup=menu())

    elif data == 'filemanager':
      cursor.execute(f"SELECT * FROM database WHERE chat_id='{user_id}'")
      rows = cursor.fetchone()
      tarif = rows[2]
      balance = rows[3]
      if tarif == 'Oddiy':
        bot.edit_message_text(
          text=f"<b>🥺 Kechirasiz sizning tarifingiz {tarif} !</b>",
          chat_id=user_id,
          message_id=call.message.id,
          parse_mode='html',
          reply_markup=add_trafic())
      elif tarif == "Ortacha":
        bot.edit_message_text(
          text=f"<b>📂 File manager tarifingiz O'rtacha !</b>",
          chat_id=user_id,
          message_id=call.message.id,
          parse_mode='html',
          reply_markup=tarif1())
      elif tarif == "Yuqori":
        bot.edit_message_text(
          text=f"<b>📂 File manager tarifingiz {tarif} !</b>",
          chat_id=user_id,
          message_id=call.message.id,
          parse_mode='html',
          reply_markup=tarif2())
      elif tarif == "Maximal":
        bot.edit_message_text(
          text=f"<b>📂 File manager tarifingiz {tarif} !</b>",
          chat_id=user_id,
          message_id=call.message.id,
          parse_mode='html',
          reply_markup=tarif3())

    elif data == 'add_sys1':
      cursor.execute(f"SELECT * FROM database WHERE chat_id='{user_id}'")
      rows = cursor.fetchone()
      tarif = rows[2]
      balance = rows[3]
      if balance >= 6000:
        hozir = datetime.now(tz)
        yil = hozir.year
        oy = hozir.month
        kun = hozir.day
        dtime = f"{yil}-{oy}-{kun:02d}"
        newbalance = balance - 6000
        #dtime = f"{yil}-{oy:02d}-{kun:02d}"
        cursor.execute(
          f"UPDATE database SET tarif = 'Ortacha' WHERE chat_id = {user_id}")
        cursor.execute(
          f"UPDATE database SET balance = {newbalance} WHERE chat_id = {user_id}"
        )
        cursor.execute(
          f"UPDATE database SET sistem_time = '{dtime}' WHERE chat_id = {user_id}"
        )
        conn.commit()
        bot.edit_message_text(
          f"<b>🥳 Sizning tarifingi: O'rtacha ga o'zgardi!</b>",
          chat_id=user_id,
          message_id=call.message.id,
          parse_mode='html',
          reply_markup=tarif1())
      else:
        txt = f"""
<b>🥺 Mablag' yetarli emas!

{reklama}
    </b>

                """
        bot.edit_message_text(txt,
                              chat_id=user_id,
                              message_id=call.message.id,
                              parse_mode='html',
                              reply_markup=BACK)

    elif data == 'add_sys2':

      cursor.execute(f"SELECT * FROM database WHERE chat_id='{user_id}'")
      rows = cursor.fetchone()
      tarif = rows[2]
      balance = rows[3]
      if balance >= 12000:
        #hozir = datetime.now(tz)
        newbalance = balance - 12000
        newtarif = 'Yuqori'
        hozir = datetime.now(tz)
        yil = hozir.year
        oy = hozir.month
        kun = hozir.day
        dtime = str(f"{yil}-{oy}-{kun:02d}")
        #print(dtime)
        cursor.execute(
          f"UPDATE database SET tarif = 'Yuqori' WHERE chat_id = {user_id}")
        cursor.execute(
          f"UPDATE database SET balance = {newbalance} WHERE chat_id = {user_id}"
        )
        cursor.execute(
          f"UPDATE database SET sistem_time = '{dtime}' WHERE chat_id = {user_id}"
        )
        conn.commit()
        bot.edit_message_text(
          f"<b>🥳 Sizning tarifingi: {newtarif} ga o'zgardi!</b>",
          chat_id=user_id,
          message_id=call.message.id,
          parse_mode='html',
          reply_markup=tarif2())
      else:
        txt = f"""
<b>🥺 Mablag' yetarli emas!


{reklama}
    </b>

                """
        bot.edit_message_text(txt,
                              chat_id=user_id,
                              message_id=call.message.id,
                              parse_mode='html',
                              reply_markup=BACK)

    elif data == 'add_sys3':

      cursor.execute(f"SELECT * FROM database WHERE chat_id='{user_id}'")
      rows = cursor.fetchone()
      tarif = rows[2]
      balance = rows[3]
      if balance >= 18000:
        #hozir = datetime.now(tz)
        newbalance = balance - 18000
        newtarif = 'Maximal'
        hozir = datetime.now(tz)
        yil = hozir.year
        oy = hozir.month
        kun = hozir.day
        dtime = str(f"{yil}-{oy}-{kun:02d}")
        #print(dtime)
        cursor.execute(
          f"UPDATE database SET tarif = 'Maximal' WHERE chat_id = {user_id}")
        cursor.execute(
          f"UPDATE database SET balance = {newbalance} WHERE chat_id = {user_id}"
        )
        cursor.execute(
          f"UPDATE database SET sistem_time = '{dtime}' WHERE chat_id = {user_id}"
        )
        conn.commit()
        bot.edit_message_text(
          f"<b>🥳 Sizning tarifingi: {newtarif} ga o'zgardi!</b>",
          chat_id=user_id,
          message_id=call.message.id,
          parse_mode='html',
          reply_markup=tarif3())
      else:
        txt = f"""
<b>🥺 Mablag' yetarli emas!

{reklama}
    </b>

                """
        bot.edit_message_text(txt,
                              chat_id=user_id,
                              message_id=call.message.id,
                              parse_mode='html',
                              reply_markup=BACK)

    elif data == 'docs':
      bot.edit_message_text(QOIDA,
                            chat_id=user_id,
                            message_id=call.message.id,
                            parse_mode='html',
                            reply_markup=BACK)
    elif data == 'setting':
      bot.edit_message_text("<b>👇 Kerakli sozlanmani tanlang!</b>",
                            chat_id=user_id,
                            message_id=call.message.id,
                            parse_mode='html',
                            reply_markup=setting_menu())
    elif data == 'shop':
      bot.edit_message_text("<b>Kerakli trafikni tanlang!</b>",
                            chat_id=user_id,
                            message_id=call.message.id,
                            parse_mode='html',
                            reply_markup=add_trafic())
    elif data == 'card_menu':
      bot.edit_message_text(CARD_TEXT,
                            chat_id=user_id,
                            message_id=call.message.id,
                            parse_mode='html',
                            reply_markup=BACK)

    elif data == 'profile':
      cursor.execute(f"SELECT * FROM database WHERE chat_id='{user_id}'")
      rows = cursor.fetchone()
      tarif = rows[2]
      balance = rows[3]
      userid = rows[0]
      dtime = rows[4]
      rtime = rows[5]
      crone = rows[6]
      if rtime != "0":
        sistem = rtime.split("-")
        kun = sistem[-1]
        oy = int(sistem[1]) + 1
        rtime = f"2023-{oy:02d}-{kun}"
      if tarif == 'Ortacha' or tarif == "Yuqori" or tarif == "Maximal":
        status = "✅"
      else:
        status = "❌"
      mbs = requests.get(f"{HOST}?size={user_id}").json()['mb']
      PROFILE = f"""<b>
🏠ID raqamingiz: {user_id}

🏷️Balansingiz: {balance} so'm

💾Disk : 1000Kb
🔑Ishlatildi: {mbs} MB

⏰Qilingan cronlar: {crone} ta

🔔Tarif: {tarif}
ℹ️ ID : {userid}

📅 Ro'yxatdan o'tilgan : {dtime}
📅 Sistem tugash sanasi : {rtime}

Tarifing holati: {status} </b>
            """
      # print(rows)
      bot.edit_message_text(PROFILE,
                            chat_id=user_id,
                            message_id=call.message.id,
                            parse_mode='html',
                            reply_markup=payment_menu())
    elif data == "webhook":
      bot.delete_message(chat_id=user_id, message_id=call.message.id)
      a = bot.send_message(
        chat_id=user_id,
        text=
        "<b>👇 Iltmos quydagi tartibda yuboring! </b>\n\n👉 <i><code>12345:absd https://manzil.uz</code></i>",
        parse_mode='html',
        reply_markup=key)
      bot.register_next_step_handler(a, webhook_set)
    elif data == "delwebhook":
      bot.delete_message(chat_id=user_id, message_id=call.message.id)
      a = bot.send_message(chat_id=user_id,
                           text="<b>👉 Iltmos API TOKEN yuboring!</b>",
                           parse_mode='html',
                           reply_markup=key)
      bot.register_next_step_handler(a, webhook_del)
    elif data == "clear_token":
      bot.delete_message(chat_id=user_id, message_id=call.message.id)
      a = bot.send_message(chat_id=user_id,
                           text="<b>👉 Iltmos API TOKEN yuboring!</b>",
                           parse_mode='html',
                           reply_markup=key)
      bot.register_next_step_handler(a, webhook_clear)
    elif data == 'sys1':
      bot.delete_message(chat_id=user_id, message_id=call.message.id)
      a = bot.send_message(
        chat_id=user_id,
        text="<b>📁 Sistem qilmoqchi bolgan file yuboring!\n</b>",
        parse_mode='html',
        reply_markup=key)
      bot.register_next_step_handler(a, add_sys1)
    elif data == 'sys2':
      bot.delete_message(chat_id=user_id, message_id=call.message.id)
      a = bot.send_message(
        chat_id=user_id,
        text="<b>📁 Sistem qilmoqchi bolgan file yuboring!\n</b>",
        parse_mode='html',
        reply_markup=key)
      bot.register_next_step_handler(a, add_sys2)
    elif data == 'sys3':
      bot.delete_message(chat_id=user_id, message_id=call.message.id)
      a = bot.send_message(
        chat_id=user_id,
        text="<b>📁 Sistem qilmoqchi bolgan file yuboring!\n</b>",
        parse_mode='html',
        reply_markup=key)
      bot.register_next_step_handler(a, add_sys3)
    elif data == 'payme':
      bot.delete_message(chat_id=user_id, message_id=call.message.id)
      a = bot.send_message(
        chat_id=user_id,
        text=
        "<b>💳 Hisob to'ldirmoqchi bo'lgan miqdorni kiriting!\n\nNamuna: <code>5000</code></b>",
        parse_mode='html',
        reply_markup=key)
      bot.register_next_step_handler(a, payment_payme)
      # bot.answer_callback_query(call.id,"⚙️ Bu bo'lim tamirda....",show_alert=True)
    elif data == 'sys4':
      bot.delete_message(chat_id=user_id, message_id=call.message.id)
      a = bot.send_message(
        chat_id=user_id,
        text="<b>📁 Sistem qilmoqchi bolgan file yuboring!\n</b>",
        parse_mode='html',
        reply_markup=key)
      bot.register_next_step_handler(a, add_sys4)
    elif data == 'sys5':
      bot.delete_message(chat_id=user_id, message_id=call.message.id)
      a = bot.send_message(
        chat_id=user_id,
        text="<b>📁 Sistem qilmoqchi bolgan file yuboring!\n</b>",
        parse_mode='html',
        reply_markup=key)
      bot.register_next_step_handler(a, add_sys5)
    elif data == 'sys6':
      bot.delete_message(chat_id=user_id, message_id=call.message.id)
      a = bot.send_message(
        chat_id=user_id,
        text="<b>📁 Sistem qilmoqchi bolgan file yuboring!\n</b>",
        parse_mode='html',
        reply_markup=key)
      bot.register_next_step_handler(a, add_sys6)
    elif data == 'del_sys':
      bot.delete_message(chat_id=user_id, message_id=call.message.id)
      a = bot.send_message(
        chat_id=user_id,
        text=
        "<b>🗑 O'chirmoqchi bolgan sistem id kiriting!</b>\n<i>Namuna : 1</i>",
        parse_mode='html',
        reply_markup=key)
      bot.register_next_step_handler(a, del_sys)
    elif data == 'add_balance':
      bot.delete_message(chat_id=user_id, message_id=call.message.id)
      a = bot.send_message(
        chat_id=user_id,
        text=
        f"<b>➕ Hisob to'ldirish quydagicha !\n\nNamuna : <code>{user_id}=5000</code></b>",
        parse_mode='html',
        reply_markup=key)
      bot.register_next_step_handler(a, add_balance)
    elif data == 'minus_balance':
      bot.delete_message(chat_id=user_id, message_id=call.message.id)
      a = bot.send_message(
        chat_id=user_id,
        text=
        f"<b>➖ Hisob Jarima quydagicha !\n\nNamuna : <code>{user_id}=5000</code></b>",
        parse_mode='html',
        reply_markup=key)
      bot.register_next_step_handler(a, minus_balance)
    elif data == 'send_balance':
      bot.delete_message(chat_id=user_id, message_id=call.message.id)
      a = bot.send_message(
        chat_id=user_id,
        text=
        f"<b>↗️ Pul yuborish uchun !\n\nNamuna : <code>{user_id}=5000</code></b>",
        parse_mode='html',
        reply_markup=key)
      bot.register_next_step_handler(a, send_user_balance)
    elif data == 'terminal':
      bot.delete_message(chat_id=user_id, message_id=call.message.id)
      a = bot.send_message(
        chat_id=user_id,
        text=
        f"<u>ulugbek@home$</u>",
        parse_mode='html',
        reply_markup=key)
      bot.register_next_step_handler(a, terminal)
    elif data == 'compiler':
      bot.delete_message(chat_id=user_id, message_id=call.message.id)
      a = bot.send_message(
        chat_id=user_id,
        text=
        f"<u>Python code..$</u>",
        parse_mode='html',
        reply_markup=key)
      bot.register_next_step_handler(a, compiler)
    elif "javob-" in data:
      a = (data.split("-"))
      chatid = a[1]
      mid = a[2]
      CHATID.append(chatid)
      MESSAGE_ID.append(mid)
      b  = bot.send_message(chat_id=user_id,
                   text=f"<b>❓ Savolingizni yozing!</b>",
                   parse_mode='html',
                   reply_markup=key)
      bot.register_next_step_handler(b, javob_def)
    elif data=='dell_accaunt':
      bot.delete_message(chat_id=user_id, message_id=call.message.id)
      a = bot.send_message(
        chat_id=user_id,
        text=
        f"<u>Namuna: {ADMIN_ID}=Oddiy\n\n<code>Ortacha\nYuqori\nMaximal</code></u>",
        parse_mode='html',
        reply_markup=key)
      bot.register_next_step_handler(a, dell_accaunt)
    elif data == 'contacts':
      bot.delete_message(chat_id=user_id, message_id=call.message.id)
      a = bot.send_message(chat_id=user_id,
                           text=f"<b>❓ Savolingizni yozing!</b>",
                           parse_mode='html',
                           reply_markup=key)
      bot.register_next_step_handler(a, contacts)
      # contacts
    # elif data=='add_crone':
    # bot.delete_message(chat_id=user_id,message_id=call.message.id)
    # a = bot.send_message(chat_id=user_id,text=f"<b>Cron qilinmoqchi bolgan havolani yuboring!</b>",parse_mode='html',reply_markup=key)
    # bot.register_next_step_handler(a,minus_balance)
    if "payment-check-" in data:
      payment_data = data.split("-")
      payid = payment_data[2]
      suma = payment_data[3]
      if payment.check_payment(payid):
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        cursor.execute(f"SELECT * FROM database WHERE chat_id='{user_id}'")
        rows = cursor.fetchone()
        balance = rows[3]
        newbalance = balance - int(suma)
        cursor.execute(
          f"UPDATE database SET balance = {newbalance} WHERE chat_id = {user_id}"
        )
        conn.commit()
        bot.send_message(chat_id=user_id,
                         text=f"<b>✅ Hisobingiz to'ldirildi!</b>",
                         parse_mode='html',
                         reply_markup=manu())
      else:
        bot.answer_callback_query(call.id,
                                  "🚫 Kechirasiz bu tolov bajarilmagan!",
                                  show_alert=True)

    if 'del-' in data:
      try:
        chatid = data.split("-")[1]
        sid = data.split("-")[2]
        cursor.execute(f"SELECT * FROM database WHERE chat_id='{chatid}'")
        rows = cursor.fetchone()
        tarif = rows[2]
        balance = rows[3]
        newbalance = balance - 5000
        cursor.execute(
          f"UPDATE database SET balance = {newbalance} WHERE chat_id = {chatid}"
        )
        # cursor.execute(f"UPDATE database SET sistem_time = '{dtime}' WHERE chat_id = {user_id}")
        conn.commit()
        delete_sistem(chatid, sid)
        bot.send_message(
          chat_id=chatid,
          text=
          "<b>😡 Siz shell yuklashga harakat qildingiz!\n\nMang naxuy: -5000 so'm</b>",
          parse_mode='html',
          reply_markup=key)
        bot.edit_message_caption("Sistema o'chirildi va Jarima berildi!",
                                 user_id, call.message.id)
      except Exception as e:
        bot.send_message(user_id, f"<b>Error {e}</b>", reply_markup=panel)

    try:
      callback_data = data
      if callback_data == 'stat' and user_id == ADMIN_ID:
        cursor.execute("SELECT COUNT(chat_id) FROM database")
        rows = cursor.fetchall()
        bot.edit_message_text(f"<b>📊 Bot obunachilari soni: {rows[0][0]}</b>",
                              user_id,
                              call.message.id,
                              reply_markup=back)
      if callback_data == 'back1' and user_id == ADMIN_ID:
        bot.edit_message_text(f"<b>Admin panelga xush kelibsiz! </b>",
                              user_id,
                              call.message.id,
                              reply_markup=panel)
      if callback_data == 'reklama' and user_id == ADMIN_ID:
        bot.delete_message(user_id, call.message.id)
        adver = bot.send_message(user_id,
                                 "<b>✍️ Xabar matnini kiritng !</b>",
                                 reply_markup=key)
        bot.register_next_step_handler(adver, ads_send)
      if callback_data == 'forward' and user_id == ADMIN_ID:
        bot.delete_message(user_id, call.message.id)
        adver = bot.send_message(user_id,
                                 "<b>✍️ Xabar matnini kiritng !</b>",
                                 reply_markup=key)
        bot.register_next_step_handler(adver, for_send)

    except Exception as e:
      bot.send_message(ADMIN_ID, f"<b>Error {e}</b>", reply_markup=panel)
  except Exception as e:
    bot.send_message(ADMIN_ID, f"<b>Error {e}</b>", reply_markup=panel)


print(bot.get_me())
bot.infinity_polling()
