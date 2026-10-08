import os,json,time,random,re,gzip,base64
import requests
from flask import Flask,jsonify,request
app=Flask(__name__)
JEV_ENDPOINT="https://ai-gateway.vercel.sh/typesafe/v1/systemone"
CHAT_ENDPOINT="https://ai-gateway.vercel.sh/v1/chat/completions"
JEV_MODEL="typesafe-ai/jev"
FALLBACK_MODEL="openai/gpt-5.6-sol"
CASES=json.loads(gzip.decompress(base64.b64decode("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")))
CASE_BY_ID={c["hard_id"]:c for c in CASES}
CLASSES=["marketing_optout","refund_return","technical_support","delivery_order","sales_promotion"]
DEFINITIONS={"marketing_optout":"客戶明確要求停止促銷、行銷郵件、簡訊、推播或其他 promotional communication","refund_return":"客戶主要要求退款、退貨或撤回交易，而不是單純排除故障","technical_support":"客戶主要反映產品故障、設定、操作、帳號或 troubleshooting 問題，並希望獲得解決","delivery_order":"客戶主要詢問配送延遲、包裹、地址修改、物流或訂單狀態","sales_promotion":"客戶主要詢問產品、價格、庫存、折扣、活動、方案或購買建議"}
INSTRUCTION="Task: Route the customer message to exactly one destination. Use the option descriptions to determine the best match. If multiple issues are mentioned, choose the destination corresponding to the customer's primary requested action."
def headers():
 k=os.environ.get("AI_GATEWAY_API_KEY")
 if not k: raise RuntimeError("AI_GATEWAY_API_KEY is not configured")
 return {"Authorization":"Bearer "+k,"Content-Type":"application/json"}
def run_jev(c):
 p={"model":JEV_MODEL,"state":"Customer message: "+c["customer_message"],"questions":{"route":{"type":"choice","instructions":INSTRUCTION,"criteria":DEFINITIONS}}}
 t=time.perf_counter();r=requests.post(JEV_ENDPOINT,headers=headers(),json=p,timeout=60);lat=(time.perf_counter()-t)*1000;r.raise_for_status();d=r.json();a=d.get("answers",{}).get("route",{})
 return {"ok":True,"model":JEV_MODEL,"hard_id":c["hard_id"],"gold_class":c["gold_class"],"top1":a.get("choice") or a.get("value"),"q":a.get("confidence"),"probabilities":a.get("probabilities") or {},"latency_ms":round(lat,1),"usage":d.get("usage",{}),"generation_id":d.get("id") or d.get("generation_id")}
def parse_label(txt):
 t=(txt or "").strip().lower()
 for k in CLASSES:
  if t==k or re.search(r"\b"+re.escape(k)+r"\b",t): return k
def run_fallback(c):
 defs="\n".join(f"- {k}: {v}" for k,v in DEFINITIONS.items());prompt=INSTRUCTION+"\n\nDestinations:\n"+defs+"\n\nCustomer message:\n"+c["customer_message"]+"\n\nReturn exactly one label from: "+", ".join(CLASSES)+". Do not explain."
 p={"model":FALLBACK_MODEL,"messages":[{"role":"user","content":prompt}],"temperature":0,"max_tokens":40}
 t=time.perf_counter();r=requests.post(CHAT_ENDPOINT,headers=headers(),json=p,timeout=90);lat=(time.perf_counter()-t)*1000;r.raise_for_status();d=r.json();txt=((d.get("choices") or [{}])[0].get("message") or {}).get("content","")
 return {"ok":True,"model":FALLBACK_MODEL,"hard_id":c["hard_id"],"gold_class":c["gold_class"],"top1":parse_label(txt),"raw_text":txt,"latency_ms":round(lat,1),"usage":d.get("usage",{}),"generation_id":d.get("id")}
@app.get("/")
def home(): return jsonify({"ok":True,"service":"JEV Pilot 2 runner","cases":len(CASES)})
@app.get("/api/pilot2")
def pilot2():
 mode=request.args.get("mode","all");hid=request.args.get("id")
 if hid:
  c=CASE_BY_ID.get(hid)
  if not c:return jsonify({"ok":False,"error":"unknown id"}),400
  try:return jsonify(run_jev(c) if mode=="jev" else run_fallback(c) if mode=="fallback" else {"ok":False,"error":"bad mode"})
  except Exception as e:return jsonify({"ok":False,"hard_id":hid,"mode":mode,"error":str(e)}),502
 if mode!="all":return jsonify({"ok":False,"error":"use mode=all"}),400
 jobs=[]
 for c in CASES:jobs += [("jev",c,1),("jev",c,2),("fallback",c,1)]
 random.Random(20261008).shuffle(jobs);out=[];started=time.time()
 for m,c,rep in jobs:
  try:
   x=run_jev(c) if m=="jev" else run_fallback(c);x["mode"]=m;x["repeat"]=rep;out.append(x)
  except Exception as e:out.append({"ok":False,"mode":m,"repeat":rep,"hard_id":c["hard_id"],"gold_class":c["gold_class"],"error":str(e)})
 return jsonify({"ok":all(x.get("ok") for x in out),"planned_calls":120,"results":out,"elapsed_s":round(time.time()-started,2),"fallback_model":FALLBACK_MODEL,"jev_model":JEV_MODEL})
