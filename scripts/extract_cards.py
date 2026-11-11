import fitz, json, os
from PIL import Image
from io import BytesIO
doc=fitz.open("Card List.pdf")
os.makedirs("cards",exist_ok=True)
out=[]
for pi,page in enumerate(doc):
    zoom=1.6
    pix=page.get_pixmap(matrix=fitz.Matrix(zoom,zoom),alpha=False)
    pageimg=Image.frombytes("RGB",[pix.width,pix.height],pix.samples)
    count=0
    for pos in range(1,10):
        col=(pos-1)%3
        row=(pos-1)//3
        x0=(59.33+170.63*col)*zoom
        y0=(152.25+226.73*row)*zoom
        w=135.35*zoom
        h=188.99*zoom
        crop=pageimg.crop((round(x0),round(y0),round(x0+w),round(y0+h)))
        # DON!! footer: reliably dark even when the illustration is pale.
        footer=crop.crop((round(w*.12),round(h*.80),round(w*.88),round(h*.94)))
        px=list(footer.resize((60,20)).getdata())
        dark=sum(r<105 and g<105 and b<110 for r,g,b in px)/len(px)
        if dark<=.32: continue
        ident=f"{pi*9+pos:03}"
        path=f"cards/{ident}.webp"
        crop.save(path,"WEBP",quality=83,method=5)
        out.append({"id":pi*9+pos,"pdfPage":pi+1,"pos":pos,"image":path})
        count+=1
    print(f"PDF page {pi+1}: {count} valid card slots",flush=True)
with open("catalog.json","w",encoding="utf-8") as f:
    json.dump({"sourcePages":len(doc),"count":len(out),"cards":out},f,ensure_ascii=False)
print("TOTAL",len(out),flush=True)
