import requests,bs4,json,re,os,urllib.parse
URL="https://www.cardrush-op.jp/product-group/142/0/photo?img=160&num=100"
headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/123 Safari/537.36"}
r=requests.get(URL,headers=headers,timeout=25);print("shop",r.status_code,len(r.content),flush=True);r.raise_for_status()
soup=bs4.BeautifulSoup(r.text,"html.parser")
terms=[("seated",["椅子","座りナミ"]),("maids",["リリス","ボニー"])]
results=[]
for key,words in terms:
  matches=soup.find_all(string=lambda v:v and all(w in str(v) for w in words))
  print("matches",key,len(matches),flush=True)
  for node in matches[:10]:
    parent=node.parent
    for level in range(5):
      images=parent.find_all("img")
      if images:
        for img in images[:5]:
          src=img.get("data-src") or img.get("data-original") or img.get("src")
          if src and not src.startswith("data:"):
            print("candidate",key,src,flush=True)
            results.append((key,urllib.parse.urljoin(URL,src)))
        break
      if not parent.parent:break
      parent=parent.parent
for key,_ in terms:
  urls=[url for k,url in results if k==key]
  seen=set()
  for url in urls:
    if url in seen:continue
    seen.add(url)
    try:
      resp=requests.get(url,headers=headers,timeout=20)
      typ=resp.headers.get("content-type","").lower()
      if resp.ok and "image" in typ and len(resp.content)>4000:
        os.makedirs("cards",exist_ok=True)
        from PIL import Image
        import io
        im=Image.open(io.BytesIO(resp.content)).convert("RGB")
        im.thumbnail((500,730))
        path="cards/274.webp" if key=="seated" else "cards/275.webp"
        im.save(path,"WEBP",quality=84)
        print("SELECTED",key,url,im.size,flush=True)
        break
    except Exception as e: print("candidate error",str(e)[:120],flush=True)
