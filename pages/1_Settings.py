import keyring,streamlit as st
from providers import PROVIDER_PRESETS,discover_models
from storage import load_config,save_config,APP_DIR
st.set_page_config(page_title='Settings | PeaBox AI',page_icon='⚙️',layout='wide')
st.title('Settings & API Vault');st.caption('Connections are configured here, away from the chat workspace. API keys remain in Windows Credential Manager.')
config=load_config();providers=config.setdefault('providers',{})
def getkey(p):return keyring.get_password('PeaBoxStreamlitLLM',p) or ''
def savekey(p,v):
 if v:keyring.set_password('PeaBoxStreamlitLLM',p,v)
t1,t2,t3=st.tabs(['Providers & APIs','Workbench defaults','Storage & privacy'])
with t1:
 provider=st.selectbox('Provider',list(PROVIDER_PRESETS));preset=PROVIDER_PRESETS[provider];cfg=providers.setdefault(provider,{})
 c1,c2=st.columns([1,1])
 with c1:
  st.subheader('Connection')
  if provider=='SSH Ollama':
   cfg['host']=st.text_input('VM host / IP',cfg.get('host',''));cfg['user']=st.text_input('SSH user',cfg.get('user','opc'));cfg['port']=st.number_input('SSH port',1,65535,int(cfg.get('port',22)));cfg['key_path']=st.text_input('Private-key path',cfg.get('key_path',''))
  else:
   cfg['base_url']=st.text_input('Base URL',cfg.get('base_url',preset.get('base_url','')))
   if provider!='Direct Ollama':newkey=st.text_input('API key',type='password',placeholder='Leave blank to retain saved key')
   else:newkey=''
  cfg['enabled']=st.toggle('Enabled',cfg.get('enabled',True));cfg['default_model']=st.text_input('Preferred model',cfg.get('default_model',''))
  if st.button('Save provider',type='primary'):savekey(provider,newkey);save_config(config);st.success('Provider configuration saved.')
 with c2:
  st.subheader('Connection test & discovery')
  if st.button('Test and discover models'):
   try:
    with st.spinner('Connecting...'):models=discover_models(provider,cfg,getkey(provider))
    st.success(f'Connection successful. {len(models)} model(s) found.');st.code('\n'.join(x.id for x in models) or 'No models returned')
   except Exception as e:st.error(str(e))
with t2:
 app=config.setdefault('app',{});app['default_provider']=st.selectbox('Default provider',list(PROVIDER_PRESETS),index=list(PROVIDER_PRESETS).index(app.get('default_provider','Direct Ollama')) if app.get('default_provider','Direct Ollama') in PROVIDER_PRESETS else 0);app['system_prompt']=st.text_area('Default system prompt',app.get('system_prompt','You are a helpful, accurate assistant.'),height=160);app['show_thinking']=st.toggle('Show thinking traces',app.get('show_thinking',True));app['confirm_delete']=st.toggle('Confirm destructive actions',app.get('confirm_delete',True));
 if st.button('Save workbench defaults'):save_config(config);st.success('Defaults saved.')
with t3:
 st.code(str(APP_DIR));st.markdown('- Conversation history: `workbench.db`\n- Non-secret configuration: `config.json`\n- API keys: Windows Credential Manager via `keyring`\n\nCloud prompts and attachments leave this computer. SSH Ollama keeps port 11434 private.')
