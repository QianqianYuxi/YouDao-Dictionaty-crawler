import sys,os
import requests
import re
from bs4 import BeautifulSoup
from time import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
headers={#进行伪装
    "User-Agent":
             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55"
    }#伪装
#所需变量
trans=[]#存储翻译信息
lang=0#语言模式
kw=0#关键字
soup=0#解析的网页信息
def GetTransInfo(kw,lang):#获取翻译网页信息
    url='https://dict.youdao.com/result?word='+kw +'&lang='+lang#指定url
    r=requests.get(url,headers=headers)
    r.raise_for_status()
    r.encoding='utf-8'
    return r.text
def transinfo(soup,trans):#根据模式提取对应翻译信息
    global lang#声明全局变量
    if lang=='en':
        trans.append(soup.body.find_all('li',{'class':'word-exp'}))#英译中
        trans.append(soup.body.find_all('li',{'class':'word-exp-ce mcols-layout'}))#中译英
    elif lang=='ja':
        trans.append(soup.body.find_all('div',{'class':'each-page active'}))#日译中
    elif lang=='fr':
        trans.append(soup.body.find_all('p',{'class':'pos'})) #法译中
        trans.append(soup.body.find_all('li',{'class':'each-word'})) #中译法
    elif lang=='ko':
        trans.append(soup.body.find_all('ul',{'class':'tran-cont'}))#韩译中
        trans.append(soup.body.find_all('li',{'class':'mcols'}))#中译韩
    outputarea.clear()#清除之前输出内容
    outputarea.append("翻译：")
    for telm in trans:#依次读取trans列表中爬取的页面列表信息
        for s in telm:#将页面列表信息依次输出
            outputarea.append(s.text)
    trans.clear()#清空字典中内容,用于后续存放其他翻译信息
    outputarea.append("(若没有翻译内容，请点击中间的网络释义以获取网络翻译)\n")
def parserLinks(html):
    global soup
    soup=BeautifulSoup(html,"html.parser")#用bs解析网页信息
    transinfo(soup,trans)#依据翻译语言提取翻译信息并输出 
def InterTrans():#获取网络释义
    global soup#声明全局变量
    if soup!=0:
        outputarea.clear()#清除之前输出内容
        trans.append(soup.body.find_all('p',{'class':'trans-content'}))#翻译
        trans.append(soup.body.find_all('li',{'class':'mcols-layout'}))#网络释义＋例句
        outputarea.append("网络释义+例句:")
        for telm in trans:#依次读取trans列表中爬取的页面列表信息
            for s in telm:#将页面列表信息依次输出 
                outputarea.append(s.text)
        trans.clear()#清空字典中内容,用于后续存放其他翻译信息 
def CataSentence():#获取双语例句
    global soup#声明全局变量
    if soup!=0:
        outputarea.clear()#清除之前输出内容
        outputarea.append("双语例句:")
        trans.append(soup.body.find_all('div',{'class':'catalogue_sentence'}))#双语例句
        for telm in trans:#依次读取trans列表中爬取的页面列表信息
            for s in telm:#将页面列表信息依次输出
                outputarea.append(s.text) 
        trans.clear()#清空字典中内容,用于后续存放其他翻译信息
def BaiKe():#获取百科
    global soup#声明全局变量
    if soup!=0:
        outputarea.clear()#清除之前输出内容
        outputarea.append("百科:") 
        trans.append(soup.body.find_all('div',{'class':'baike dict-module'}))#百科
        for telm in trans:#依次读取trans列表中爬取的页面列表信息
            for s in telm:#将页面列表信息依次输出
                outputarea.append(s.text)
        trans.clear()#清空字典中内容,用于后续存放其他翻译信息
def en():#判断选择的模式
    global lang
    chatText.clear()    #清除输入框内容
    outputarea.clear()#清除之前输出内容
    chatText.setFocus() #将光标重新移动到输入框
    outputarea.append("现在翻译模式：英汉互译\n")
    lang='en'
def ja():#判断选择的模式
    global lang
    chatText.clear()    #清除输入框内容
    outputarea.clear()#清除之前输出内容
    chatText.setFocus() #将光标重新移动到输入框
    outputarea.append("现在翻译模式：日汉互译\n")
    lang='ja'
def fr():#判断选择的模式
    global lang
    chatText.clear()    #清除输入框内容
    outputarea.clear()#清除之前输出内容
    chatText.setFocus() #将光标重新移动到输入框
    outputarea.append("现在翻译模式：法汉互译\n")
    lang='fr'
def ko():#判断选择的模式
    global lang
    chatText.clear()    #清除输入框内容
    outputarea.clear()#清除之前输出内容
    chatText.setFocus() #将光标重新移动到输入框
    outputarea.append("现在翻译模式：韩汉互译\n")
    lang='ko'
def showResult():   #显示对话信息
    #label包含提示字符和从 time 库获取
    #的时间日期，将其显示字体颜色设置为蓝色
    global lang
    if lang==0:
        outputarea.append("请先选择顶端翻译模式\n")
    else:
        kw=chatText.toPlainText()    #提取输入框字符信息
        saveMsg(kw+" "+lang) #保存对话信息
        html=GetTransInfo(kw,lang)
        parserLinks(html) 
def cancelMsg():    #清除输入框内容
    chatText.clear()
def saveMsg(txt):	#保存输入内容
    file = open('save.txt', 'a')
    file.write(txt + '\n')
    file.close()
def getMsg():   #读取历史信息并显示到输出框
    if os.path.exists('save.txt'):
        message = '历史查词记录:'
        outputarea.clear()
        outputarea.append(message)
        file = open('save.txt', 'r')
        txt = file.read() + '\n'
        outputarea.append(txt)
        file.close()
    else:
        outputarea.append('No Record\n')
chatapp = QApplication(sys.argv)
chatwidget = QWidget()
chatText = QTextEdit(chatwidget)    #信息输入
chatText.setMaximumSize(QSize(800,100)) #设置文本框大小
outputarea = QTextEdit(chatwidget)  #信息显示
outputarea.setReadOnly(True)
outputarea.setFont(QFont('SimSun', 12)) #设置输出文本的字体
outputarea.setMaximumSize(QSize(800, 200))
btnSend = QPushButton('查询', chatwidget)#查询翻译信息相关内容选择
btnInterTrans=QPushButton('网络释义+短语', chatwidget)
btnCataSentence=QPushButton('双语例句', chatwidget)
btnBaiKe=QPushButton('百科', chatwidget)
btnCancel = QPushButton('取消', chatwidget)
btnHistory = QPushButton('历史记录', chatwidget)
btnen = QPushButton('英汉互译', chatwidget)#翻译模式选择
btnja = QPushButton('日汉互译', chatwidget)
btnfr = QPushButton('法汉互译', chatwidget)
btnko = QPushButton('韩汉互译', chatwidget)
btnSend.clicked.connect(showResult)     #按钮都以click为信号
btnInterTrans.clicked.connect(InterTrans)     #连接不同的处理函数
btnCataSentence.clicked.connect(CataSentence)
btnBaiKe.clicked.connect(BaiKe)
btnCancel.clicked.connect(cancelMsg)
btnen.clicked.connect(en)
btnja.clicked.connect(ja)
btnfr.clicked.connect(fr)
btnko.clicked.connect(ko)
btnHistory.clicked.connect(getMsg)
ResultLabel=QLabel("查找结果：")
cxbox = QHBoxLayout()    #横向布局，负责中间查找按钮布局
#将‘发送’和‘取消’按钮排在左边，再加入一个弹簧分隔符，
#将‘历史消息’按钮排在最右边
cxbox.addWidget(btnSend)
cxbox.addWidget(btnCancel)
cxbox.addStretch(1)
cxbox.addWidget(btnInterTrans)
cxbox.addWidget(btnCataSentence)
cxbox.addWidget(btnBaiKe)
cxbox.addStretch(1)
cxbox.addWidget(btnHistory)
mdbox=QHBoxLayout()    #横向布局，负责上方模式按钮布局
mdbox.addWidget(btnen)
mdbox.addWidget(btnja)
mdbox.addWidget(btnfr)
mdbox.addWidget(btnko)
vbox = QVBoxLayout()    #纵向布局
#依次添加显示区、输入区和按钮子布局(由上到下)
vbox.addLayout(mdbox)
vbox.addWidget(chatText)
vbox.addLayout(cxbox)
vbox.addWidget(outputarea)
chatwidget.setLayout(vbox)
chatwidget.setGeometry(0, 0, 800, 400)
chatwidget.setWindowTitle('词典')
screen = QDesktopWidget().screenGeometry()
size = chatwidget.geometry()
chatwidget.move((screen.width() - size.width()) // 2, \
                    (screen.height() - size.height()) // 2)
chatwidget.show()
sys.exit(chatapp.exec_())
