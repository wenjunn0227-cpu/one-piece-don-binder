import fitz, json, os
from PIL import Image
from io import BytesIO
doc=fitz.open("Card List.pdf")
os.makedirs("cards",exist_ok=True)
out=[]
for pi,page in enumerate(doc):
    objects=[]
    for entry in page.get_images(full=True):
        xref=entry[0]
        for rect in page.get_image_rects(xref):
            if 100<=rect.width<=160 and 165<=rect.height<=215 and rect.y0>=120:
                objects.append((rect.y0,rect.x0,xref))
    objects.sort()
    seen=set()
    for pos,(y,x,xref) in enumerate(objects,1):
        ident=f"{pi*9+pos:03}"
        try:
            pix=fitz.Pixmap(doc,xref)
            if pix.n>4: pix=fitz.Pixmap(fitz.csRGB,pix)
            img=Image.open(BytesIO(pix.tobytes("png"))).convert("RGB")
            img.thumbnail((500,700))
            path=f"cards/{ident}.webp"
            img.save(path,"WEBP",quality=82,method=5)
            out.append({"id":pi*9+pos,"pdfPage":pi+1,"pos":pos,"image":path})
        except Exception as e:
            print("error",pi+1,pos,e)
    print(f"PDF page {pi+1}: {len(objects)} image cards")
with open("catalog.json","w",encoding="utf-8") as f:
    json.dump({"sourcePages":len(doc),"count":len(out),"cards":out},f,ensure_ascii=False)
print("TOTAL",len(out))
