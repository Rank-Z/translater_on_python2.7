# -*- coding: UTF-8 -*-
from urllib2 import  urlopen
from HTMLParser import HTMLParser
import wx

class Scraper(HTMLParser):
    def __init__(self):
        self.in_ul=False
        self.in_li=False
        self.first=True
        self.txt1=''
        self.counter=0
        HTMLParser.__init__(self)

    def handle_starttag(self,tag,attrs):
        if tag=='ul'and attrs==[]and self.getpos()[0]<200 :
            self.in_ul=True
        if tag=='li'and attrs==[]:
            self.li=True

    def handle_data(self,data):
        if self.in_ul and self.in_ul:
            if '  'and '\n' not in data and data!=' ;':
                if self.first:
                    self.txt1+=data.decode('utf-8').encode('gbk')
                    self.counter+=1
                    self.first=False
                else:
                    self.txt1=self.txt1+"\r\n".decode('utf-8').encode('gbk')+data.decode('utf-8').encode('gbk')
                    self.counter+=1

    def handle_endtag(self, tag):
        if tag=='ul':
            self.in_ul=False
        if tag=='li':
            self.in_li=False

    def clear(self):
        self.in_ul = False
        self.in_li = False
        self.first = True
        self.txt1 = ''


def main():
    app=wx.App()
    win=wx.Frame(None,title="Translater",size=(300,75))

    word=wx.TextCtrl(win,pos=(0,0),size=(300,25))
    result=wx.TextCtrl(win,pos=(0,25),size=(300,400),style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_NO_VSCROLL)


    def change_size(event):
        if word.GetValue()== '':
            result.SetValue('')
            win.SetSize((300,75))
        else:
            scarper = Scraper()
            html=urlopen('http://dict.youdao.com/w/%s/#keyfrom=dict2.top'%(word.GetValue().encode('utf-8'))).read()
            scarper.feed(html)
            win.SetSize((300,75+scarper.counter*18))
            result.SetValue(scarper.txt1)

    word.Bind(wx.EVT_KEY_UP,change_size)
    win.SetTransparent(180)
    win.Show()
    app.MainLoop()


if __name__=='__main__':main()

