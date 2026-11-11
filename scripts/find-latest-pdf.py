import requests,fitz,os,concurrent.futures
hosts=["onepiece-cardgame.com","www.onepiece-cardgame.com","asia-en.onepiece-cardgame.com","asia-tw.onepiece-cardgame.com","asia-th.onepiece-cardgame.com","asia-sg.onepiece-cardgame.com","asia-hk.onepiece-cardgame.com","asia-id.onepiece-cardgame.com"]
base=[f"https://{h}/pdf/don-cardlist.pdf" for h in hosts]
urls=[u+suffix for u in base for suffix in ["?v=261112","?v=260822",""]]
def fetch(url):
 try:
  r=requests.get(url,timeout=17,headers={"User-Agent":"Mozilla/5.0"},allow_redirects=True)
  if r.status_code!=200 or not r.content.startswith(b"%PDF"): return (url,0,None)
  doc=fitz.open(stream=r.content,filetype="pdf")
  n=len(doc); txt=doc[-1].get_text()
  good=("OP-17" in txt or "OP-16" in txt or "世界最強の戦士" in txt)
  print(f"PDF {url}: pages={n} final-page-has-OP16-17={good}",flush=True)
  return (url,n,r.content if n>=31 and good else None)
 except Exception as e:
  print(f"Skipping {url}: {str(e)[:80]}",flush=True)
  return (url,0,None)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
 found=list(pool.map(fetch,urls))
valid=[f for f in found if f[2]]
if valid:
 choice=max(valid,key=lambda x:x[1])
 with open("Card List.pdf","wb") as file:file.write(choice[2])
 print("Successfully installed newest catalog:",choice[0],choice[1],flush=True)
else:
 print("No official regional URL offers 31-page catalog; keeping original repository PDF intact.",flush=True)
