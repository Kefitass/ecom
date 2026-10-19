import math
from PIL import Image, ImageDraw
S=4; W,H=1080*S,1920*S; CX,CY=W//2,H//2
BEIGE=(239,230,211); GREEN=(30,77,43); LW=34*S
OUT="/home/user/ecom/verdea-instagram/destacadas/"
def base():
    im=Image.new("RGB",(W,H),BEIGE); d=ImageDraw.Draw(im)
    r=390*S; d.ellipse([CX-r,CY-r,CX+r,CY+r],fill=GREEN)
    return im,d
def P(x,y): return (CX+x*S,CY+y*S)
def line(d,pts,w=LW): 
    pts=[P(*p) for p in pts]; d.line(pts,fill=BEIGE,width=w,joint="curve")
    for p in pts: d.ellipse([p[0]-w/2,p[1]-w/2,p[0]+w/2,p[1]+w/2],fill=BEIGE)
def rrect(d,x0,y0,x1,y1,r,fill=None,w=LW):
    d.rounded_rectangle([*P(x0,y0),*P(x1,y1)],radius=r*S,outline=BEIGE if not fill else None,fill=fill,width=w)
def save(im,name): im.resize((1080,1920),Image.LANCZOS).save(OUT+name+".png")

# Reseñas: estrella
im,d=base(); pts=[]
for i in range(10):
    a=-math.pi/2+i*math.pi/5; r=200 if i%2==0 else 85
    pts.append((r*math.cos(a),r*math.sin(a)+10))
d.polygon([P(*p) for p in pts],fill=BEIGE)
for x,y,s in [(-215,-150,28),(220,-160,22)]:
    d.ellipse([*P(x-s,y-s),*P(x+s,y+s)],fill=BEIGE)
save(im,"resenas")

# Modo de uso: gotero + gota
im,d=base()
rrect(d,-55,-230,55,-130,40,fill=BEIGE)           # perilla
rrect(d,-80,-140,80,-100,14,fill=BEIGE)           # collar
line(d,[(-35,-100),(-35,60),(0,110),(35,60),(35,-100)])  # tubo
# gota
g=[]
for i in range(60):
    t=i/59*2*math.pi
    x=70*math.sin(t)*(1-0.0)
    y=-math.cos(t)
    # forma de gota
    xx=60*math.sin(t)*(1+y)/2*1.9 if False else None
d.polygon([P(0,150),P(-62,250),P(62,250)],fill=BEIGE)
d.ellipse([*P(-65,205),*P(65,330)],fill=BEIGE)
save(im,"modo-de-uso")

# Pagos: tarjeta
im,d=base()
rrect(d,-230,-150,230,150,40)
d.rectangle([*P(-230+17,-80),*P(230-17,-25)],fill=BEIGE)
line(d,[(-150,70),(-40,70)]); line(d,[(80,70),(140,70)])
save(im,"pagos")

# Pedidos: caja
im,d=base()
top=[(0,-220),(200,-120),(0,-20),(-200,-120)]
line(d,top+[top[0]])
line(d,[(-200,-120),(-200,120),(0,220),(200,120),(200,-120)])
line(d,[(0,-20),(0,220)])
line(d,[(-100,-170),(100,-70)],w=26*S)
save(im,"pedidos")

# Envíos: camión
im,d=base()
rrect(d,-250,-140,60,90,24)
line(d,[(60,-60),(170,-60),(240,20),(240,90),(60,90)])
for x in (-150,150):
    d.ellipse([*P(x-62,90-62+30),*P(x+62,90+62+30)],fill=GREEN)
    d.ellipse([*P(x-55,65),*P(x+55,175)],outline=BEIGE,width=LW)
line(d,[(-330,-60),(-280,-60)]); line(d,[(-350,10),(-280,10)])
save(im,"envios")
