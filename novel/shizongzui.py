# -*- coding=utf-8 -*-

from bs4 import BeautifulSoup
import requests,sys,os,re,time
import urllib3
urllib3.disable_warnings()

def timep():
    print(time.strftime("%Y-%m-%d %X", time.localtime()))
    
    
    
import sys
class Logger(object):
    def __init__(self, filename='default.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

class downloader(object):
    def __init__(self):
        print("init.")
        self.server = 'https://www.kanunu8.com/'
        self.target = 'https://www.kanunu8.com/zt/zt_10756.html'
        
        self.books={}   #存放书名和连接 
        self.book={}
        self.curent_path=os.getcwd()       

    
    def get_books(self):
        timep()
        print("get books start.")
        req = requests.get(url=self.target,verify=False) #获取链接的内容
        req.encoding = 'gb18030'
        #html = req.text    #获取html
        bf = BeautifulSoup(req.text,'html.parser') 
        div_bf=bf.find_all('td',class_='p10-24')[:6]
        a_bf=BeautifulSoup(str(div_bf),'html.parser')
        a = a_bf.find_all('a')
        for each in a:
            self.books[each.string] = self.server + each.get('href')     
        print(self.books)
        timep()
        print("get books end.")        
        return self.books
        
    def get_books_chapters(self,bookName,bookUrl): 
        book_chapters={}
        timep()
        print("get %s chapters.\n" % bookName)
        req = requests.get(url=bookUrl,verify=False)
        req.encoding = 'gb18030'
        bf = BeautifulSoup(req.text,'html.parser') 
        #chapter = bf.find('tbody','tr','td')
        timep()
        print(bookName)
        a=bf.find_all(href=re.compile("[0-9]+\.html"))[25:]
        for each in a:
            book_chapters[each.string] = bookUrl + each.get('href')  
        timep()            
        print("get %s chapters end.\n" % bookName)
        return book_chapters
            
    def get_content(self,chaptersName,chaptersUrl):
        timep()
        print("get %s content...%s\n" % (chaptersName,chaptersUrl))
        req = requests.get(url=chaptersUrl,verify=False)
        req.encoding = 'gb18030'
        bf = BeautifulSoup(req.text,'html.parser')
        div_bf = bf.find_all('p')
        contents = div_bf[0].text.replace('\xa0'*8,'\n\n')    #\xa0 是不间断空白符 &nbsp;
        #contents = div_bf[0].text
        #print(contents)
        return contents

    def write(self,bookName,chaptersName,contents):
        timep()
        print("write content into %s."%bookName)
        path=os.path.join(self.curent_path,bookName+'.txt')
        print(contents)
        print(path)
        wite_flag = True
        with open(path,'a',encoding='utf-8') as f:
            f.write(chaptersName + '\n')          
            f.writelines(contents)
            print(bookName,chaptersName)
            f.write('\n\n')
        timep()
        print("write content end.")
       
    def download_all_books(self):
        books=self.get_books()   
        for bookName,bookUrl in books.items():
            timep()
            print("start download %s." % bookName)
            book_chapters=self.get_books_chapters(bookName,bookUrl)
            for chaptersName,chaptersUrl in book_chapters.items():
                contents = self.get_content(chaptersName,chaptersUrl)
                self.write(bookName,chaptersName,contents)
                
    def download_one_book(self,bookName,bookUrl):
        book_chapters = self.get_books_chapters(bookName,bookUrl)
        for chaptersName,chaptersUrl in book_chapters.items():
            contents = self.get_content(chaptersName,chaptersUrl)
            self.write(bookName,chaptersName,contents)
    
if __name__ == "__main__":
    sys.stdout = Logger('download_stdout.log', sys.stdout)
    sys.stderr = Logger('download_stderr.log', sys.stderr)     # redirect std err, if necessary
    timep()
    print("start download 《十宗罪》.")
    dl=downloader()
    #dl.download_all_books()
    dl.download_one_book("《十宗罪前传》","https://www.kanunu8.com/book/4609/")
    

    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
