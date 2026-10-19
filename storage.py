from __future__ import annotations
import json, sqlite3
from datetime import datetime
from pathlib import Path
APP_DIR=Path.home()/'.peabox_streamlit_llm'; APP_DIR.mkdir(parents=True,exist_ok=True)
DB_PATH=APP_DIR/'workbench.db'; CONFIG_PATH=APP_DIR/'config.json'
def connect():
 c=sqlite3.connect(DB_PATH); c.row_factory=sqlite3.Row; c.execute('PRAGMA foreign_keys=ON'); return c
def init_db():
 with connect() as c:
  c.execute("CREATE TABLE IF NOT EXISTS conversations(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,provider TEXT,model TEXT,created_at TEXT NOT NULL,updated_at TEXT NOT NULL)")
  c.execute("CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY AUTOINCREMENT,conversation_id INTEGER NOT NULL,role TEXT NOT NULL,content TEXT NOT NULL,thinking TEXT DEFAULT '',created_at TEXT NOT NULL,FOREIGN KEY(conversation_id) REFERENCES conversations(id) ON DELETE CASCADE)")
  cols={x['name'] for x in c.execute('PRAGMA table_info(conversations)')}
  for name,ddl in [('pinned','INTEGER DEFAULT 0'),('archived','INTEGER DEFAULT 0'),('system_prompt',"TEXT DEFAULT ''")]:
   if name not in cols: c.execute(f'ALTER TABLE conversations ADD COLUMN {name} {ddl}')
def now(): return datetime.now().isoformat(timespec='seconds')
def new_conversation(title='New chat'):
 t=now()
 with connect() as c: return c.execute('INSERT INTO conversations(title,created_at,updated_at) VALUES(?,?,?)',(title,t,t)).lastrowid
def list_conversations(search='',archived=False):
 q='SELECT * FROM conversations WHERE archived=?'; a=[int(archived)]
 if search: q+=' AND title LIKE ?'; a.append(f'%{search}%')
 q+=' ORDER BY pinned DESC,updated_at DESC'
 with connect() as c:return [dict(x) for x in c.execute(q,a)]
def load_messages(cid):
 with connect() as c:return [dict(x) for x in c.execute('SELECT role,content,thinking,created_at FROM messages WHERE conversation_id=? ORDER BY id',(cid,))]
def add_message(cid,role,content,thinking=''):
 t=now()
 with connect() as c:c.execute('INSERT INTO messages(conversation_id,role,content,thinking,created_at) VALUES(?,?,?,?,?)',(cid,role,content,thinking,t));c.execute('UPDATE conversations SET updated_at=? WHERE id=?',(t,cid))
def update_conversation(cid,**values):
 allowed={'title','provider','model','pinned','archived','system_prompt'}; values={k:v for k,v in values.items() if k in allowed and v is not None}
 if not values:return
 with connect() as c:c.execute('UPDATE conversations SET '+','.join(f'{k}=?' for k in values)+' WHERE id=?',list(values.values())+[cid])
def delete_conversation(cid):
 with connect() as c:c.execute('DELETE FROM conversations WHERE id=?',(cid,))
def export_conversation(cid):
 with connect() as c:
  conv=dict(c.execute('SELECT * FROM conversations WHERE id=?',(cid,)).fetchone()); msgs=[dict(x) for x in c.execute('SELECT role,content,thinking,created_at FROM messages WHERE conversation_id=? ORDER BY id',(cid,))]
 return {'conversation':conv,'messages':msgs}
def load_config():
 try:return json.loads(CONFIG_PATH.read_text('utf-8')) if CONFIG_PATH.exists() else {}
 except Exception:return {}
def save_config(config):CONFIG_PATH.write_text(json.dumps(config,indent=2),'utf-8')
