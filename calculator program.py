import tkinter,tkinter.font
import math
screen=tkinter.Tk()
screen.minsize(700,400)
screen.maxsize(700,400)
s=["0","1","2","3","4","5","6","7","8","9","+","-","X","/","=",".","AC","C","SIN","COS","TAN","DEG","RAD"]
b=[None]*23
for run in range(0,len(s)):
    w,h=2,2
    if run in (18,19,20):
        w=3
    if run in (21,22):
        w,h=4,2
    b[run]=tkinter.Button(screen,text=s[run],width=w,height=h,font=tkinter.font.Font(size=15,weight="bold"),command=lambda run=run:display(s[run]))
trigmode="DEG"
def initialize():
    global isnum1,isnum2,exp,px,py,err,s,b,trigmode
    isnum1=isnum2=""
    exp=""
    px,py=200,60
    tkinter.Text(screen,height=2,width=60).place(x=200,y=50)
    tkinter.Label(screen,text=trigmode).place(x=220,y=20)
    err=False
    for run in range(0,len(s)):
        if not s[run].isdigit() and s[run] not in ["-","C","AC",".","SIN","COS","TAN","DEG","RAD"]:
            b[run]["state"]="disabled"
def ver():
    global exp,b,s
    if ((len(exp)>=3 and exp[-2]==" ") and exp[-1].isdigit()==False and exp[-3].isdigit()==True) or exp=="":
        for run in range(0,len(b)):
            if not s[run].isdigit() and s[run]!="-" and s[run]!="C" and s[run]!="AC" and s[run] not in ["SIN","COS","TAN","DEG","RAD"]:
                b[run]["state"]="disabled"
            else:
                b[run]["state"]="active"
    elif ((len(exp)>=3 and exp[-2]==" ")and exp[-3].isdigit()==False and exp[-1]=="-") or exp=="-":
        for run in range(0,len(b)):
            if not s[run].isdigit() and s[run] not in ["C","AC","SIN","COS","TAN","DEG","RAD"]:
                b[run]["state"]="disabled"
            else:
                b[run]["state"]="active"
    elif len(exp)>=1 and exp[-1]==".":
        for run in range(0,len(b)):
            if not s[run].isdigit() and s[run] not in ["C","AC","DEG","RAD"]:
                b[run]["state"]="disabled"
            else:
                b[run]["state"]="active"
    else:
        for run in range(0,len(b)):
            b[run]["state"]="active"
    if (exp!="" and exp[-1].isdigit() and len(exp.split())!=3):
        for run in range(18,21):
            b[run]["state"]="disabled"
    if exp[-4:-1] in ["SIN","COS","TAN"]:
        for run in range(0,len(b)):
            if s[run] in ["+","X","/","SIN","COS","TAN"]:
                b[run]["state"]="disabled"
    if (exp[-5:-2] in ["SIN","COS","TAN"] and exp[-1]=="-"):
        for run in range(0,len(b)):
            if s[run] in ["+","X","/","SIN","COS","TAN","-"]:
                b[run]["state"]="disabled"
    if exp!="" and "." in exp.split()[-1]:
        b[15]["state"]="disabled"
    else:
        b[15]["state"]="active"
initialize()
def display(c):
    global isnum1,isnum2,px,py,s,exp,err,b,trigmode
    if c in ["DEG","RAD"]:
        tkinter.Label(screen,text=trigmode,fg="white").place(x=220,y=20)
        trigmode=c
        tkinter.Label(screen,text=c).place(x=220,y=20)
        return
    if err or c=="AC":
        initialize()
        ver()
        return
    if c=="C":
        if exp=="":    
            return
        elif exp[-4:-1] in ["SIN","COS","TAN"]:
            for run in range(-2,-5,-1):
                tkinter.Label(screen,text=exp[run],bg="white",fg="white").place(x=px,y=py)
                px-=12
            exp=exp[:-4]
            if exp[-1]==" ":
                px-=12
                exp=exp[:-1]
        else:
            tkinter.Label(screen,text=exp[-1],bg="white",fg="white").place(x=px,y=py)
            if (len(exp)>=2 and exp[-2]==" "):
                exp=exp[:-2]
                px-=24
            else:
                exp=exp[:-1]
                px-=12
        ver()
        if exp[-4:-1] in ["SIN","COS","TAN"]:
            isnum1=exp[-4:-1]
        elif exp=="":
            isnum1=""
        else:
            isnum1=exp[-1]
        return
    if px>=660:
        return
    isnum2=c
    if (isnum1.isdigit()==isnum2.isdigit()==True) or exp=="" or (isnum1=="-" and len(exp.split())%2!=0) or isnum1=="." or (isnum2=="." and isnum1.isdigit()==True) or isnum1 in ["SIN","COS","TAN"]:
        px+=12
    else:
        px+=24
        exp+=" "
    exp+=c
    if len(exp.split())>3 or (len(exp.split())==2 and exp.split()[0][:3] in ["SIN","COS","TAN"]) or c=="=":
        calc(c)
        return
    if c in ["SIN","COS","TAN"]:
        exp+=trigmode[0]
    ver()
    isnum1=isnum2
    for run in range(0,len(c)):
        tkinter.Label(screen,text=c[run],bg="white").place(x=px,y=py)
        if run!=len(c)-1:
            px+=12
def calc(extra):
    global clickno,isnum1,isnum2,px,py,s,exp,err
    l=exp.split()
    for run in range(0,len(l)-1):
        mod=l[run].lstrip("-")
        if mod[:3] in ["SIN","COS","TAN"]:
            if mod[3]=="D":
                angle=(math.pi/180)*float(mod[4:])
            else:
                angle=float(mod[4:])
            sign=1
            if mod[:3]=="TAN" and ((angle/(math.pi/2))-1)%2==0:
                tkinter.Text(screen,height=2,width=30).place(x=200,y=50)
                tkinter.Label(screen,text="ERROR : TAN IS UNDEFINED. CLICK ANY BUTTON TO CONTINUE",bg="white").place(x=220,y=60)
                err=True
                return
            if l[run][0]=="-":
                sign=-1
            if "SIN" in l[run]:
                l[run]=math.sin(angle)*sign
            elif "COS" in l[run]:
                l[run]=math.cos(angle)*sign
            elif "TAN" in l[run]:
                l[run]=math.tan(angle)*sign
            if "e" in str(l[run]):
                l[run]=round(l[run])
            l[run]=str(l[run])
    if len(l)==2:
        res=float(l[0])
    else:
        num1,op,num2=float(l[0]),l[1],float(l[2])
        if l[1]=="+":
            res=num1+num2
        elif l[1]=="-":
            res=num1-num2
        elif l[1]=="X":
            res=num1*num2
        elif l[1]=="/":
            if num2==0:
                tkinter.Text(screen,height=2,width=30).place(x=200,y=50)
                tkinter.Label(screen,text="ERROR : CANNOT DIVIDE BY 0. CLICK ANY BUTTON TO CONTINUE",bg="white").place(x=220,y=60)
                err=True
                return
            res=num1/num2
    if res==int(res):
        res=int(res)
    l=str(res)
    initialize()
    if extra in ["SIN","COS","TAN"]:
        display(extra)
        for run in l:
            display(str(run))
    else:
        for run in l:
            display(str(run))
        if extra!="=":
            display(extra)
for run in range(1,10):
    q=run-1
    posy=240-int(q/3)*70
    posx=200+(q%3)*70
    b[run].place(x=posx,y=posy)
for run in range(13,9,-1):
    posx=410
    posy=100+(13-run)*70
    b[run].place(x=posx,y=posy)
b[0].place(x=200,y=310)
b[14].place(x=340,y=310)
b[15].place(x=270,y=310)
b[18].place(x=480,y=100)
b[19].place(x=480,y=170)
b[20].place(x=480,y=240)
b[16].place(x=550,y=100)
b[17].place(x=550,y=170)
b[21].place(x=100,y=100)
b[22].place(x=100,y=170)
screen.mainloop()
            













    

