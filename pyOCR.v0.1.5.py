#coding=utf-8
# 基于百度OpenAI平台之OCR开放平台的OCR程序

#导入相应的库
from tkinter import *    #界面库
from tkinter.ttk import *    #界面库
import tkinter.messagebox as msg
from PIL import ImageGrab  #图形库
import time
import ctypes
import pyautogui
import requests
import base64
from hashlib import md5
import json
import os

# 此处定义程序图标
base64_ico="""
AAABAAEAAAAAAAEAIAB9AwAAFgAAAIlQTkcNChoKAAAADUlIRFIAAAEAAAABAAgCAAAA0xA/MQAA
AAlwSFlzAAAOxAAADsQBlSsOGwAAAy9JREFUeJzt3LFtAzEQAMF/wI0pcQ1uQoFix44VqAnX4ESl
0U08QRA7UwBxeGlx2Z1jjAOqPlYPACsJgDQBkCYA0gRAmgBIEwBpAiBNAKQJgDQBkCYA0gRAmgBI
EwBpAiBNAKQJgDQBkCYA0gRAmgBIEwBpAiBNAKQJgDQBkCYA0qYE8Hi9Zzw7w/N+Wz3CYvEfywYg
TQCkCYA0AZAmANIEQJoASBMAaQIgTQCkCYA0AZAmANIEQJoASBMAaQIgTQCkCYA0AZAmANIEQJoA
SBMAaQIgTQCkCYA0AZAmANJ2CsAl5xlmfNWNLk7vFABcTgCkCYA0AZAmANIEQJoASBMAaQIgTQCk
CYA0AZAmANIEQJoASBMAaQIgTQCkCYA0AZAmANIEQJoASBMAaQIgTQCkCYA0AZB2jjFWz7DS3/fX
6hEW+/z5XT3CSjYAaQIgTQCkCYA0AZAmANIEQJoASBMAaQIgTQCkCYA0AZAmANIEQJoASBMAaQIg
TQCkCYA0AZAmANIEQJoASBMAaQIgTQCkCYC0+nHcSWbc3I1fsZ3EBiBNAKQJgDQBkCYA0gRAmgBI
EwBpAiBNAKQJgDQBkCYA0gRAmgBIEwBpAiBNAKQJgDQBkCYA0gRAmgBIEwBpAiBNAKQJgDQBkCYA
0gRAmgBIEwBpAiBNAKQJgDQBkCYA0gRAmgBIEwBpAiBNAKQJgDQBkCYA0gRAmgBIEwBpAiBNAKQJ
gDQBkCYA0gRAmgBIEwBpAiBNAKSdY4zLH3283pe/eRzH836b8SyX2+gPYAOQJgDSBECaAEgTAGkC
IE0ApAmANAGQJgDSBECaAEgTAGkCIE0ApAmANAGQJgDSBECaAEgTAGkCIE0ApAmANAGQJgDSBECa
AEjbKYAZJ1cd3J10yHYXOwUAlxMAaQIgTQCkCYA0AZAmANIEQJoASBMAaQIgTQCkCYA0AZAmANIE
QJoASBMAaQIgTQCkCYA0AZAmANIEQJoASBMAaQIgTQCknWOM1TPAMjYAaQIgTQCkCYA0AZAmANIE
QJoASBMAaQIgTQCkCYA0AZAmANIEQJoASBMAaQIgTQCkCYA0AZD2D50oLePCJ4SPAAAAAElFTkSu
QmCC"""
outf = open('pyOCR.ico','wb')
rb_ico = base64.b64decode(base64_ico)
outf.write(rb_ico)
outf.close()

# 代理设置（update on 2022-11-21）
proxies={
'http': 'http://127.0.0.1:7890',
'https': 'http://127.0.0.1:7890'
}


###########################
# 与OCR API调用有关的代码 #
###########################
# 获取 access_token
# client_id 为官网获取的AK， client_secret 为官网获取的SK
def get_token():
    AK = 'xYNYNSTd5S77hhrCt7qFMo59'
    SK = 'O7uBzaGU3QLkWNcIBtCZgjCSvECYBua4'
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(AK,SK)
    #response = requests.get(host)
    response = requests.get(host, proxies=proxies)
    if response:
        rp = response.json()
        return rp['access_token']

# 通用文字识别（高精度版）
def ocr(imgpath):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    # 二进制方式打开图片文件
    f = open(imgpath, 'rb')
    img = base64.b64encode(f.read())
    params = {"image":img}
    access_token = get_token()
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    #response = requests.post(request_url, data=params, headers=headers)
    response = requests.post(request_url, proxies=proxies, data=params, headers=headers)
    if response:
        return response.json()

# 文字识别（结果打印到控制台）
def pic2text_cli():
    res_obj = ocr('pyOCR_temp1.png')
    res_txt = ''
    try:
        for obj in res_obj['words_result']:
            res_txt += '{}\n'.format(obj['words'])
        print(res_txt)
    except:
        print('Error:{}'.format(res_obj))

# 文字识别（返回字符串）
OriText = '空字符串'
isOriText = True
def pic2text():
    global OriText
    global isOriText
    isOriText = True
    res_obj = ocr('pyOCR_temp1.png')
    res_txt = ''
    try:
        for obj in res_obj['words_result']:
            res_txt += '{}\n'.format(obj['words'])
        OriText = res_txt
        return res_txt
    except:
        return 'Error:{}'.format(res_obj)


########################
#   百度翻译 API接口   #
########################
# For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
# Generate salt and sign
def make_md5(s, encoding='utf-8'):return md5(s.encode(encoding)).hexdigest()
def translate(query):
    # Set your own appid/appkey.
    appid = '20201212000645063'
    appkey = 'HEhjErB3C9EQzQdtZklq'
    # Set url
    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path
    # It is recommend to use a random num as `salt` to enhance security. But I think is unnecessary.
    salt = 65500 
    sign = make_md5(appid + query + str(salt) + appkey)
    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': 'auto', 'to': 'auto', 'salt': salt, 'sign': sign}
    # Send request
    #r = requests.post(url, params=payload, headers=headers)
    r = requests.post(url, proxies=proxies, params=payload, headers=headers)
    try:
        result = r.json()
    except:
        return "Error:request result={}".format(r)
    # Get result
    try:
        trans_res = result['trans_result']
        res = "" # translated text
        for p in trans_res:
            res += p["dst"]
            res += "\n"
        return res
    except:
        return "Error:{}".format(json.dumps(result, indent=4, ensure_ascii=False))




########################
# 基于tkinter的GUI界面 #
########################
pos_arr = []  # 存储鼠标位置
click_num = 0 # 监听共按下了几次鼠标，当按下2次鼠标后结束监听。

# 调用PyAutoGUI进行屏幕截图
def screen_capture(filename):
    global   pos_arr
    global click_num
    x1 = pos_arr[0]
    y1 = pos_arr[1]+30
    x2 = pos_arr[2]
    y2 = pos_arr[3]+30
    if(x1>x2): x1,x2 = x2,x1
    if(y1>y2): y1,y2 = y2,y1
    img = pyautogui.screenshot(filename,region=(x1,y1,x2-x1,y2-y1))
# 定义在展示截图后，鼠标点击动作的响应函数
def callback(event):
    global   pos_arr
    global click_num
    pos_arr.append(event.x)
    pos_arr.append(event.y)
    click_num += 1
    if(click_num>1):
        screen_capture('pyOCR_temp1.png')
        ocr_res = pic2text()
        global text_Box
        text_Box.config(state=NORMAL)
        text_Box.delete('0.0',END)
        text_Box.insert('0.0',ocr_res)
        os.system('del pyOCR_temp.gif')
        os.system('del pyOCR_temp1.png')
        top1.destroy()
# 使用这个函数展示截图
def show_screenshoot():
    global   pos_arr
    global click_num
    pos_arr   = []
    click_num = 0
    global top1
    top1=Toplevel()
    top1.title("通过两次单击选择截图区域")
    top1.state("zoomed")
    img_gif   = PhotoImage(file = 'pyOCR_temp.gif')
    label_img = Label(top1, image = img_gif)
    label_img.bind('<Button-1>',callback)
    label_img.bind('<Button-2>',callback)
    label_img.bind('<Button-3>',callback)
    label_img.pack(expand=1)
    top1.mainloop()
# 截取全屏并展示
def ScreenShootAllGraph():
    root.wm_withdraw()
    time.sleep(0.5)
    img = pyautogui.screenshot('pyOCR_temp.gif')
    root.wm_deiconify()
    show_screenshoot()
# 从剪贴板图片里获取图片并识别
def ocr_from_clipboard():
    img = ImageGrab.grabclipboard()
    global text_Box
    text_Box.config(state=NORMAL)
    try:
        img.save('pyOCR_temp1.png',format='png')
        ocr_res = pic2text()
        text_Box.delete('0.0',END)
        text_Box.insert('0.0',ocr_res)
    except:
        text_Box.delete('0.0',END)
        text_Box.insert('0.0',"剪贴板中没有图片！\n请先截图或按下键盘上的PrintScreen键。")
        global OriText
        global isOriText
        OriText   = "剪贴板中没有图片！\n请先截图或按下键盘上的PrintScreen键。"
        isOriText = True
# 清空文本框
def clear_text_Box():
    global text_Box
    global OriText
    text_Box.config(state=NORMAL)
    OriText = '空字符串'
    text_Box.delete('0.0',END)

# 合并文本（删除换行符）
def merge_text():
    global isOriText
    global   OriText
    #print(isOriText)
    if(isOriText):
        #text_in_box = text_Box.get('0.0',END)
        text_in_box = text_Box.get('0.0',END)
        temp_text = text_in_box.replace("-\n","")
        temp_text = temp_text.replace("\n"," ")
        OriText = temp_text
        #if(text_in_box != OriText):OriText = text_in_box
        #print(text_in_box)
        #translate_text = translate(OriText)
        text_Box.delete('0.0',END)
        text_Box.insert('0.0',temp_text)
        #text_Box.config(state=DISABLED)
    else:
        pass
        #text_Box.config(state=NORMAL)
        #text_Box.delete('0.0',END)
        #text_Box.insert('0.0',OriText)
    #if(isOriText):isOriText = False
    #else:         isOriText = True

# 文字翻译
def trans_text_Box():
    global isOriText
    global   OriText
    #print(isOriText)
    if(isOriText):
        #text_in_box = text_Box.get('0.0',END)
        text_in_box = text_Box.get('0.0',END)
        if(text_in_box != OriText):OriText = text_in_box
        #print(text_in_box)
        translate_text = translate(OriText)
        text_Box.delete('0.0',END)
        text_Box.insert('0.0',translate_text)
        text_Box.config(state=DISABLED)
    else:
        text_Box.config(state=NORMAL)
        text_Box.delete('0.0',END)
        text_Box.insert('0.0',OriText)
    if(isOriText):isOriText = False
    else:         isOriText = True
# 程序信息
def show_about():
    about = msg.showinfo("关于", "pyOCR v0.1.5(2022.4.13)\n\n作者:\t张皖豫(1738296705@qq.com)\n技术支持:\t百度开放平台\n函数库:\ttkinter, PIL, time, ctypes, pyautogui, requests, base64, hashlib, json, os")

if(__name__=='__main__'):
    # 初始化tkinter
    #global root
    root = Tk()
    #告诉操作系统使用程序自身的dpi适配
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    #获取屏幕的缩放因子
    ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)
    #设置程序缩放
    root.tk.call('tk', 'scaling', ScaleFactor/64)

    root.title("pyOCR v0.1.5 - 基于ttk的修改版")
    root.geometry('600x400')  #窗口大小：宽*高
    root.iconbitmap('pyOCR.ico')   # 更改窗口图标
    #root.resizable(width=False, height=False) #设置宽高不可变
    root.resizable(width=True, height=True) #设置宽高可变
     
    """ 定义一些组件的样式 """
    style = Style()
    style.configure("CLS.TButton", background="#faffe6",foreground="#ff0000")
    style.configure("ABT.TButton", background="#ccffff",foreground="#003c65")

    #l1 = ttk.Label(text="Test", style="BW.TLabel")
    #l2 = ttk.Label(text="Test", style="BW.TLabel")

   
    """定义一组按钮，沿左上对齐"""
    frame1 = Frame(root)
    #frame1.grid(row=0,column=0,sticky='w')
    frame1.pack(side='top',fill=X)
    
    """ 全屏截图并识别 """
    btn_ScreenAllShot = Button(frame1,text="截图",command=ScreenShootAllGraph)
    #btn_ScreenAllShot.place(width=50,height=30,x=5,y=5)
    btn_ScreenAllShot.pack(side='left')
 
    """ 剪贴板图片识别 """
    btn_OCRFromClipboard = Button(frame1,text="识别剪贴板",command=ocr_from_clipboard)
    #btn_OCRFromClipboard.place(width=100,height=30,x=65,y=5)
    btn_OCRFromClipboard.pack(side='left')
    """ 翻译 """
    btn_TextTrans = Button(frame1,text="原文/翻译",command=trans_text_Box)
    #btn_TextCls.place(width=50,height=30,x=175,y=5)
    btn_TextTrans.pack(side='left')
 
    """ 合并文字为同一段 """
    btn_TextTrans = Button(frame1,text="合并文字",command=merge_text)
    #btn_TextCls.place(width=50,height=30,x=175,y=5)
    btn_TextTrans.pack(side='left')
 


    """ 清空文本框 """
    btn_TextCls = Button(frame1,text="清空文本框",command=clear_text_Box,style='CLS.TButton')
    #btn_TextCls.place(width=100,height=30,x=235,y=5)
    btn_TextCls.pack(side='left')

    """ 关于 """
    btn_About = Button(frame1,text="关于",command=show_about,style='ABT.TButton')
    #btn_About.place(width=50,height=30,x=525,y=5)
    btn_About.pack(side='right')
    
    """定义第二行的控件，沿左上对齐"""
    frame2 = Frame(root)
    #frame2.grid(row=1,column=0,sticky='w')
    frame2.pack(side='top',fill='both')
    
    """ 文本框 """
    global text_Box
    text_Box = Text(frame2,height=16,width=58,font=('consolas',11,'normal'))
    text_Box.pack(side='left',fill=Y)
    #text_Box.place(width=580,height=350,x=0,y=40)
    scroll = Scrollbar(frame2)
    scroll.pack(side='left',fill=Y)
    scroll.config(command=text_Box.yview)
    text_Box.config(yscrollcommand=scroll.set)
    



    root.mainloop()


 
