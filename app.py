from __future__ import annotations
import json,keyring,streamlit as st
from attachments import build_user_content
from providers import PROVIDER_PRESETS,ModelInfo,chat,discover_models
from storage import *
st.set_page_config(page_title='PeaBox AI Workbench v4',page_icon='🟣',layout='wide');init_db()
st.markdown('<style>.block-container{padding-top:1.4rem}.stChatMessage{border-radius:14px}.pb{padding:14px 18px;border:1px solid #30364d;border-radius:16px;background:linear-gradient(120deg,#171b26,#24163c)}</style>',unsafe_allow_html=True)
if 'config' not in st.session_state:st.session_state.config=load_config()
if 'conversation_id' not in st.session_state:
 cs=list_conversations();st.session_state.conversation_id=cs[0]['id'] if cs else new_conversation()
if 'models' not in st.session_state:st.session_state.models={}
def pkey(p):return keyring.get_password('PeaBoxStreamlitLLM',p) or ''
config=st.session_state.config;enabled=[p for p in PROVIDER_PRESETS if config.get('providers',{}).get(p,{}).get('enabled',True)]
with st.sidebar:
 st.title('🟣 PeaBox AI');st.caption('LLM Workbench v4')
 if st.button('＋ New chat',type='primary',use_container_width=True):st.session_state.conversation_id=new_conversation();st.rerun()
 search=st.text_input('Search conversations',placeholder='Search...');archived=st.toggle('Show archived',False);cs=list_conversations(search,archived)
 for c in cs:
  icon='📌 ' if c.get('pinned') else ''
  if st.button(icon+c['title'][:32],key=f"c{c['id']}",use_container_width=True):st.session_state.conversation_id=c['id'];st.rerun()
 st.divider();st.page_link('pages/1_Settings.py',label='Settings & API Vault',icon='⚙️')
 st.caption('Provider credentials are managed on the dedicated Settings page.')
if not enabled:st.error('No providers are enabled. Open Settings & API Vault.');st.stop()
default=config.get('app',{}).get('default_provider',enabled[0]);provider=st.selectbox('Provider',enabled,index=enabled.index(default) if default in enabled else 0);cfg=config.setdefault('providers',{}).setdefault(provider,{});preset=PROVIDER_PRESETS[provider]
if provider!='SSH Ollama':cfg.setdefault('base_url',preset.get('base_url',''))
head1,head2=st.columns([3,2])
with head1:st.markdown('<div class="pb"><h2>PeaBox AI Workbench</h2><span>Local, remote and cloud models in one focused workspace.</span></div>',unsafe_allow_html=True)
with head2:
 if st.button('Discover / refresh models',use_container_width=True):
  try:st.session_state.models[provider]={m.id:m for m in discover_models(provider,cfg,pkey(provider))};st.success(f"Found {len(st.session_state.models[provider])} models")
  except Exception as e:st.error(str(e))
model_map=st.session_state.models.get(provider,{})
if not model_map and cfg.get('default_model'):model_map={cfg['default_model']:ModelInfo(cfg['default_model'])}
model_name=st.selectbox('Model',list(model_map),disabled=not model_map);info=model_map.get(model_name,ModelInfo(model_name));caps=info.capabilities
chat_tab,context_tab,controls_tab,manage_tab=st.tabs(['Chat','Attachments','Generation','Manage'])
with context_tab:
 uploaded=st.file_uploader('Reference files',accept_multiple_files=True,type=['txt','md','csv','json','xml','html','py','ps1','js','ts','yaml','yml','log','pdf','docx','xlsx','xlsm','pptx','png','jpg','jpeg','webp']);st.caption('Up to 100,000 extracted characters per request. Images require a vision-capable model.')
with controls_tab:
 use_defaults=st.toggle('Use model defaults',True);reasoning=st.selectbox('Reasoning / thinking',['Default','Off','Low','Medium','High','Max'] if 'thinking' in caps else ['Default']);temperature=st.slider('Temperature',0.0,2.0,float(info.parameters.get('temperature',.6)),.05,disabled=use_defaults);top_p=st.slider('Top P',0.0,1.0,float(info.parameters.get('top_p',.95)),.01,disabled=use_defaults);top_k=st.number_input('Top K',0,500,int(float(info.parameters.get('top_k',20))),disabled=use_defaults);repeat_penalty=st.number_input('Repeat penalty',0.0,2.0,float(info.parameters.get('repeat_penalty',1.0)),.05,disabled=use_defaults);num_ctx=st.number_input('Context tokens',1024,262144,int(float(info.parameters.get('num_ctx',8192))),1024,disabled=use_defaults);max_tokens=st.number_input('Maximum output tokens',256,32768,4096,256,disabled=use_defaults)
with manage_tab:
 conv=next((x for x in list_conversations() if x['id']==st.session_state.conversation_id),None)
 newtitle=st.text_input('Conversation title',conv['title'] if conv else 'New chat')
 a,b,c,d=st.columns(4)
 if a.button('Rename'):update_conversation(st.session_state.conversation_id,title=newtitle);st.rerun()
 if b.button('Pin / unpin'):update_conversation(st.session_state.conversation_id,pinned=0 if conv and conv.get('pinned') else 1);st.rerun()
 if c.button('Archive'):update_conversation(st.session_state.conversation_id,archived=1);st.session_state.conversation_id=new_conversation();st.rerun()
 if d.button('Delete'):delete_conversation(st.session_state.conversation_id);st.session_state.conversation_id=new_conversation();st.rerun()
 data=export_conversation(st.session_state.conversation_id);st.download_button('Export conversation as JSON',json.dumps(data,indent=2),file_name='peabox-conversation.json',mime='application/json')
with chat_tab:
 messages=load_messages(st.session_state.conversation_id)
 for item in messages:
  with st.chat_message(item['role']):st.markdown(item['content']);
  if item.get('thinking') and config.get('app',{}).get('show_thinking',True):
   with st.expander('Thinking trace'):st.text(item['thinking'])
 prompt=st.chat_input('Ask, create, analyse or compare...',disabled=not bool(model_name))
 if prompt:
  try:
   combined,images=build_user_content(prompt,uploaded,'vision' in caps);prior=[{'role':m['role'],'content':m['content']} for m in messages];sys=config.get('app',{}).get('system_prompt','')
   outgoing=([{'role':'system','content':sys}] if sys else [])+prior+[{'role':'user','content':combined}];settings=dict(cfg);settings.update(use_defaults=use_defaults,reasoning=reasoning,temperature=temperature,top_p=top_p,top_k=int(top_k),repeat_penalty=repeat_penalty,num_ctx=int(num_ctx),max_tokens=int(max_tokens));add_message(st.session_state.conversation_id,'user',prompt)
   if not messages:update_conversation(st.session_state.conversation_id,title=prompt[:60].replace('\n',' '),provider=provider,model=model_name)
   with st.chat_message('assistant'):
    with st.spinner(f'Running {model_name}...'):answer,thinking=chat(provider,model_name,outgoing,images,settings,pkey(provider))
    st.markdown(answer)
   add_message(st.session_state.conversation_id,'assistant',answer,thinking);st.rerun()
  except Exception as e:st.error(f'Request failed: {e}')
