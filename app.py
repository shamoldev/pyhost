from flask import Flask, request, jsonify
import requests
import os
import sqlite3

conn = sqlite3.connect('database.db',check_same_thread=False)
sql = conn.cursor()
sql.execute('CREATE TABLE IF NOT EXISTS screen_list(chat_id TEXT,sistem TEXT,path TEXT,filename TEXT)')
conn.commit()
if not os.path.isdir(f"sistem"):
    os.mkdir(f"sistem")

app  = Flask(__name__)
@app.route('/crone', methods=['POST', 'GET'])
def screeen():
  sql.execute('SELECT * FROM screen_list')
  # a = sql.fetchall()
  for i in  sql.fetchall():
    #print(i)
    chatid = i[0]
    sistem = i[1]
    filename = i[3]
    if os.path.isfile(i[2]+filename):
      print('Mavjud',i)
    else:
      sql.execute(f"DELETE FROM screen_list WHERE chat_id='{chatid}' AND sistem='{sistem}'")
      conn.commit()
      print("O'chirlidi!",i)

    try:
      os.system(f"screen -S {chatid}.{sistem} -X quit")
    except:
      pass
    try:
      os.chdir(i[2])
    except:
      pass
    try:
      os.system(f"screen -S {chatid}.{sistem} -d -m python3 {filename}")
    except:
      pass
    os.chdir("../../../")

  return "Zb"
@app.route('/', methods=['POST', 'GET'])
def handle_request():
    if request.method == 'POST':
        data = request.json
        if 'url' in data and 'chat_id' in data and 'sistem' in data and 'file_name' in data:
            url = data['url']
            chat_id = data['chat_id']
            sysid = data['sistem']
            filename = data['file_name']

            file_content = requests.get(url).content
            if not os.path.isdir(f"./sistem/{chat_id}/"):
              os.mkdir(f"./sistem/{chat_id}/")
            if not os.path.isdir(f"./sistem/{chat_id}/{sysid}/"):
                os.mkdir(f"./sistem/{chat_id}/{sysid}/")
            with open(f"./sistem/{chat_id}/{sysid}/{filename}", "wb") as f:
                f.write(file_content)
            try:
              os.system(f"screen -S {chat_id}.{sysid} -X quit")
            except:
              pass
            os.chdir(f"./sistem/{chat_id}/{sysid}/")
            os.system(f"screen -dmS {chat_id}.{sysid} -d -m python3 {filename}")
            os.chdir("../../../")

            path= f"./sistem/{chat_id}/{sysid}/"
            sql.execute(f"INSERT INTO screen_list(chat_id,sistem,path,filename) VALUES('{chat_id}','{sysid}','{path}','{filename}')")
            conn.commit()
            response_data = {"status": "success", "url": url, "chat_id": chat_id, "file_name": filename, "sistem": sysid}
            return jsonify(response_data)
    if request.method == 'GET':
        chat_id = request.args.get('chat_id')
        all = request.args.get('del_all')
        size = request.args.get('size')
        if chat_id:
          sysid = request.args.get('id')
          os.system(f"screen -S {chat_id}.{sysid} -X quit")
          if  os.path.isdir(f"./sistem/{chat_id}/{sysid}"):
            os.system(f"rm -rf ./sistem/{chat_id}/{sysid}/")
            response_data = {"status": "success", "chat_id": chat_id, "sistem": sysid}

            conn.commit()
            return jsonify(response_data)
        elif size:
          try:
            size1=0
            for path, dirs, files in os.walk(f"sistem/{size}"):
  	          for f in files:
                    fp = os.path.join(path, f)
                    size1+= os.path.getsize(fp)
            
            size_mb = size1 / (1024 * 1024)+1
            return jsonify({'mb':f"{size_mb:4f}"})
          except:
            return jsonify({'mb':"1"})
        elif all:
            if  os.path.isdir(f"./sistem/{all}/"):
                try:
                    #os.system(f"screen -S {chat_id}.{i} -X quit")
                    os.system(f"rm -rf ./sistem/{all}/")
                except:
                    pass
            response_data = {"status": "success", "chat_id": all}
            return jsonify(response_data)
        else:
            return "Hello everyone"




if __name__ == '__main__':
    app.run(host='0.0.0.0')
