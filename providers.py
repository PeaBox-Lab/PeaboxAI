from __future__ import annotations
import json,subprocess,requests
from dataclasses import dataclass,field
from openai import OpenAI
from anthropic import Anthropic
@dataclass
class ModelInfo:id:str;capabilities:set[str]=field(default_factory=set);parameters:dict=field(default_factory=dict);details:dict=field(default_factory=dict)
PROVIDER_PRESETS={'SSH Ollama':{'kind':'ssh_ollama'},'Direct Ollama':{'kind':'direct_ollama','base_url':'http://localhost:11434'},'LiteLLM':{'kind':'openai_compatible','base_url':'http://localhost:4000/v1'},'LM Studio':{'kind':'openai_compatible','base_url':'http://localhost:1234/v1'},'Open WebUI':{'kind':'openai_compatible','base_url':'http://localhost:3000/api'},'OpenAI':{'kind':'openai_compatible','base_url':'https://api.openai.com/v1'},'Anthropic':{'kind':'anthropic','base_url':'https://api.anthropic.com'},'Google Gemini':{'kind':'openai_compatible','base_url':'https://generativelanguage.googleapis.com/v1beta/openai/'},'OpenRouter':{'kind':'openai_compatible','base_url':'https://openrouter.ai/api/v1'},'Groq':{'kind':'openai_compatible','base_url':'https://api.groq.com/openai/v1'},'Mistral':{'kind':'openai_compatible','base_url':'https://api.mistral.ai/v1'},'Together AI':{'kind':'openai_compatible','base_url':'https://api.together.xyz/v1'},'Custom OpenAI-compatible':{'kind':'openai_compatible','base_url':''}}
def _parse_parameters(text):
 r={}
 for line in (text or '').splitlines():
  p=line.strip().split(None,1)
  if len(p)==2 and p[0] not in r:r[p[0]]=p[1].strip().strip('"')
 return r
def _ssh_base(s):
 if not s.get('key_path') or not s.get('host'):raise ValueError('Configure SSH host and private-key path in Settings.')
 return ['ssh','-i',s['key_path'],'-p',str(s.get('port',22)),'-o','BatchMode=yes','-o','ConnectTimeout=15',f"{s.get('user','opc')}@{s['host']}"]
def _ssh_json(s,e,p=None,timeout=120):
 remote=f'curl -sS --fail-with-body http://127.0.0.1:11434{e}'+(" -H 'Content-Type: application/json' --data-binary @-" if p is not None else '')
 x=subprocess.run(_ssh_base(s)+[remote],input=json.dumps(p) if p is not None else None,capture_output=True,text=True,timeout=timeout)
 if x.returncode:raise RuntimeError(x.stderr.strip() or x.stdout.strip() or 'SSH request failed')
 return json.loads(x.stdout)
def _http_json(base,e,p=None,key='',timeout=120):
 h={'Content-Type':'application/json'}
 if key:h['Authorization']=f'Bearer {key}'
 r=requests.get(base.rstrip('/')+e,headers=h,timeout=timeout) if p is None else requests.post(base.rstrip('/')+e,headers=h,json=p,timeout=timeout);r.raise_for_status();return r.json()
def infer_cloud_capabilities(provider,model):
 v=model.lower();c={'chat','attachments_text'}
 if any(x in v for x in ('gpt-4o','gpt-5','claude','gemini','vision','vl')):c.add('vision')
 if any(x in v for x in ('o1','o3','o4','gpt-5','claude','gemini-2.5','gemini-3','reason','deepseek-r1')):c.add('thinking')
 return c
def discover_models(provider,s,key=''):
 kind=PROVIDER_PRESETS[provider]['kind']
 if kind in {'ssh_ollama','direct_ollama'}:
  call=(lambda e,p=None:_ssh_json(s,e,p)) if kind=='ssh_ollama' else (lambda e,p=None:_http_json(s['base_url'],e,p,key));out=[]
  for item in call('/api/tags').get('models',[]):
   n=item.get('name') or item.get('model');d=call('/api/show',{'model':n});out.append(ModelInfo(n,set(d.get('capabilities',[])),_parse_parameters(d.get('parameters','')),d.get('details',{})))
  return out
 if kind=='anthropic':return [ModelInfo(x.id,infer_cloud_capabilities(provider,x.id)) for x in Anthropic(api_key=key).models.list(limit=100).data]
 return [ModelInfo(x.id,infer_cloud_capabilities(provider,x.id)) for x in OpenAI(api_key=key or 'not-required',base_url=s['base_url']).models.list().data]
def test_connection(provider,s,key=''):return len(discover_models(provider,s,key))
def chat(provider,model,messages,images,s,key=''):
 kind=PROVIDER_PRESETS[provider]['kind']
 if kind in {'ssh_ollama','direct_ollama'}:
  outgoing=[dict(m) for m in messages]
  if images:outgoing[-1]['images']=[x['base64'] for x in images]
  p={'model':model,'messages':outgoing,'stream':False};reason=s.get('reasoning','Default')
  if reason!='Default':p['think']=False if reason=='Off' else reason.lower()
  if not s.get('use_defaults',True):p['options']={k:s[k] for k in ('temperature','top_p','top_k','repeat_penalty','num_ctx')}
  d=_ssh_json(s,'/api/chat',p,1800) if kind=='ssh_ollama' else _http_json(s['base_url'],'/api/chat',p,key,1800);m=d.get('message',{});return m.get('content',''),m.get('thinking','')
 if kind=='anthropic':
  converted=[{'role':m['role'],'content':m['content']} for m in messages if m['role']!='system']
  if images:converted[-1]['content']=[{'type':'text','text':messages[-1]['content']}]+[{'type':'image','source':{'type':'base64','media_type':i['media_type'],'data':i['base64']}} for i in images]
  kw={'model':model,'messages':converted,'max_tokens':s.get('max_tokens',4096)}
  if not s.get('use_defaults',True):kw.update(temperature=s['temperature'],top_p=s['top_p'])
  r=Anthropic(api_key=key).messages.create(**kw);return '\n'.join(b.text for b in r.content if getattr(b,'type','')=='text'),''
 converted=[dict(m) for m in messages]
 if images:converted[-1]['content']=[{'type':'text','text':messages[-1]['content']}]+[{'type':'image_url','image_url':{'url':f"data:{i['media_type']};base64,{i['base64']}"}} for i in images]
 kw={'model':model,'messages':converted}
 if not s.get('use_defaults',True):kw.update(temperature=s['temperature'],top_p=s['top_p'],max_tokens=s.get('max_tokens',4096))
 if s.get('reasoning') in {'Low','Medium','High'}:kw['reasoning_effort']=s['reasoning'].lower()
 r=OpenAI(api_key=key or 'not-required',base_url=s['base_url']).chat.completions.create(**kw);return r.choices[0].message.content or '',''
