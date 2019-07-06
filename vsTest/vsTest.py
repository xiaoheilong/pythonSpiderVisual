import requests
import json
import gzip
from io import BytesIO
import ssl
import http.cookiejar
import urllib
from bs4 import BeautifulSoup
from urllib import request

#from lxml import etree
import os
from selenium import webdriver
import time
import re
import importlib
import sys
from PIL import Image, ImageEnhance
import pytesseract
import arcpy, envipy
envipy.Initialize(arcpy) 
from arcpy import env
from PIL  import Image, ImageDraw

from fileNameStruct import fNameStruct

importlib.reload(sys)
#from mysqldb import ConnectMysql
#import pymysql
ssl._create_default_https_context = ssl._create_unverified_context
# ��ֵ��  
threshold = 140  
table = []  
for i in range(256):  
    if i < threshold:  
        table.append(0)  
    else:  
        table.append(1)  
  
#���ڶ�������  
#����ʶ�����ĸ�� ���øñ��������  
rep={'O': '0',
           'I': '1',
           'L': '1',
           'Z': '7',
           'A': '4',
           '&': '4',
           'S': '8',
           'Q': '0',
           'T': '7',
           'Y': '7',
           '}': '7',
           'J': '7',
           'F': '7',
           'E': '6',
           ']': '0',
           '?': '7',
           'B': '8',
           '@': '6',
           'G': '0',
           'H': '3',
           '$': '3',
           'C': '0',
           '(': '0',
           '[': '5',
           'X': '7',
           '`': '',
           '\\': '',
           ' ': '',
           '\n': '',
           '-': '',
           '+': '',
           '*': '',
           '.': '',
           ';': ''
           }


# ��ֵ����
t2val = {}


def getMainHtml(url):
    #url = "http://www.yunarm.com/admin"
    raw = {
        "username": 'ysjgly7',
        "password": 'password',
        "captcha": 'ntup',
        "remember": '1',
    }
    data = json.dumps(raw)
    headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8',
               'Connection': 'keep-alive',
               'Cookie': 'Hm_lvt_bfc6c23974fbad0bbfed25f88a973fb0=1555064760,1555983875; 03d59d43a62f5a8ded3cb0608aadd4bb=825b8fc8dd9c271aaa0c1382835e8b4c; 0_2c7212d2692a557659446c4633af6e31=78e33c11c99295f68deaa9d48d60b9af; Hm_lvt_affb9cbd1fdfa7253bd71c8e51455851=1559114611,1561619040; Hm_lpvt_affb9cbd1fdfa7253bd71c8e51455851=1561619042',
               'Host': 'www.yunarm.com',
               'Origin': 'https://www.yunarm.com',
               'Referer': 'https://www.yunarm.com/api/index/login',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest'
               }
    login_data = urllib.request.Request(
        url,  headers=headers, data=data.encode(encoding='UTF8'))  # .
    cj = http.cookiejar.CookieJar()  # ��ȡCookiejar���󣨴��ڱ�����cookie��Ϣ��
    # �Զ���opener,����opener��CookieJar�����
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cj))
    # ��װopener,�˺����urlopen()ʱ����ʹ�ð�װ����opener����
    urllib.request.install_opener(opener)
    # opener.open(url,login_data).read().encode(encoding='UTF8')
    page = request.urlopen(login_data).read()
    # print(page)
    buff = BytesIO(page)

    f = gzip.GzipFile(fileobj=buff)

    res = f.read().decode('utf-8')

    # print(res)
    return res


def clickElement(driver , element):
    print("clickElement!")
    driver.find_element_by_id(element).click()



def throughAllPageByElement(element):
    print(element)

def recongnizePicText(name , flagStr):        
    #��ͼƬ  
    im = Image.open(name)  
    #ת�����Ҷ�ͼ
    imgry = im.convert('L')
    #��ǿ�Աȶ�
    sharpness =ImageEnhance.Contrast(imgry)#�Աȶ���ǿ
    sharp_img = sharpness.enhance(2.0)
    #����ͼ��
    #imgry.save('g'+name)  
    #��ֵ����������ֵ�ָ��thresholdΪ�ָ�� 
    #out = imgry.point(table,'1')  
    twoValue(sharp_img, 100)
    #out.save('b'+name)  
    #������
    clearNoise(sharp_img , 3, 2) 
    saveImage(flagStr + name , sharp_img.size)
    #ʶ��  
    imageStr = flagStr  + name
    recognizeImag  = Image.open(imageStr)
    text = pytesseract.image_to_string(recognizeImag)  
    '''
    text = text.strip(' ') 
    text = text.upper(); 
    for r in rep:  
        text = text.replace(r,rep[r])  
    '''
    return text 


def downloadUrlImage(img_url, savePath):
    api_token = "fklasjfljasdlkfjlasjflasjfljhasdljflsdjflkjsadljfljsda"
    header = {"Authorization": "Bearer " + api_token} # ����http header�����������Ҫ����Ŀ�������token��������Ȩ��һ�ַ�ʽ
    r = requests.get(img_url, verify=False, stream=True)
    print(r.status_code) # ����״̬��
    if r.status_code == 200:
        open(savePath, 'wb').write(r.content) # ������д��ͼƬ
        print("download urlPicture done!")
    del r

def get_snap(driver, savePath):  # ��Ŀ����ҳ���н���������ص���ȫ��
    driver.save_screenshot(savePath)
    page_snap_obj=Image.open(savePath)
    return page_snap_obj

###
###��ֵ��ֵ
###
def twoValue(image, G):
    for y in range(0, image.size[1]):
        for x in range(0, image.size[0]):
            g = image.getpixel((x, y))
            if g > G:
                t2val[(x, y)] = 1
            else:
                t2val[(x, y)] = 0



def saveImage(filename, size):
    image = Image.new("1", size)
    draw = ImageDraw.Draw(image)

    for x in range(0, size[0]):
        for y in range(0, size[1]):
            draw.point((x, y), t2val[(x, y)])
    image.save(filename)

# ����һ����A��RGBֵ������Χ��8�����RBGֵ�Ƚϣ��趨һ��ֵN��0 <N <8������A��RGBֵ����Χ8�����RGB�����С��Nʱ���˵�Ϊ���
# G: Integer ͼ���ֵ����ֵ
# N: Integer ������ 0 <N <8
# Z: Integer �������
# ���
#  0������ɹ�
#  1������ʧ��

def clearNoise(image, N, Z):
    for i in range(0, Z):
        t2val[(0, 0)] = 1
        t2val[(image.size[0] - 1, image.size[1] - 1)] = 1

        for x in range(1, image.size[0] - 1):
            for y in range(1, image.size[1] - 1):
                nearDots = 0
                L = t2val[(x, y)]
                if L == t2val[(x - 1, y - 1)]:
                    nearDots += 1
                if L == t2val[(x - 1, y)]:
                    nearDots += 1
                if L == t2val[(x - 1, y + 1)]:
                    nearDots += 1
                if L == t2val[(x, y - 1)]:
                    nearDots += 1
                if L == t2val[(x, y + 1)]:
                    nearDots += 1
                if L == t2val[(x + 1, y - 1)]:
                    nearDots += 1
                if L == t2val[(x + 1, y)]:
                    nearDots += 1
                if L == t2val[(x + 1, y + 1)]:
                    nearDots += 1

                if nearDots < N:
                    t2val[(x, y)] = 1






def  capTurePicByName(driver , elementName , savePath):
    img = driver.find_element_by_id(elementName)
    #time.sleep(2)
    location = img.location
    print('location: ')
    print(location)
    size = img.size
    left = location['x']
    top = location['y']
    right = left + size['width']
    bottom = top + size['height']

    page_snap_obj = get_snap(driver , savePath)
    image_obj = page_snap_obj.crop((left, top, right, bottom))
    return image_obj 

def batchGreyPic(dealFolder , saveFolder):#批量灰度处理图片
    fileNames = os.listdir(dealFolder)
    for file in fileNames:
        newDir = dealFolder + '/' + file 
        if os.path.isfile(newDir): 
            if os.path.splitext(newDir)[1] == ".png": 
                 im = Image.open(newDir)  
                 imgry = im.convert('L')
                 sharpness =ImageEnhance.Contrast(imgry)
                 sharp_img = sharpness.enhance(2.0)
                 twoValue(sharp_img, 100)
                 clearNoise(sharp_img , 3, 2) 
                 saveImage(saveFolder + '/' + file , sharp_img.size)
        else:
            batchGreyPic(newDir)  
            
def batchConvertTiffPic(workspace , saveSpace, picFormatStr):#批量转tiff文件
    env.workspace = workspace
    rasters = arcpy.ListRasters("*", picFormatStr)
    for raster in rasters:
        inraster = raster
        outraster= saveSpace + raster.strip("." + picFormatStr) + ".tif"
        arcpy.ConvertRaster_envi(inraster, outraster, "TIFF", "")
    print("All png convert to tiff!") 

def getFilenameStruct(str , splitString):
    result = fNameStruct(str , splitString)
    return result


def  getCaptureCodePic(driver ,captchName, picOrigalname ,  counts):
    for index in  range(counts):
        clickElement(driver  ,captchName)
        cropImage = capTurePicByName(driver , captchName , "html_full.png")
        fileStruct = getFilenameStruct(picOrigalname , ".")
        picString= fileStruct.bfName + "_" +  str(index) + "." + fileStruct.ltname
        if os.path.exists(picString):
            print("the file is exist!")
            os.remove(picString)
        cropImage.save(picString)
        time.sleep(4)





def openBrower(html):
    '''
    driver = webdriver.Chrome()
    driver.get(html)
    driver.find_element_by_name('username').send_keys('ysjgly7')
    driver.find_element_by_name('password').send_keys('c1QoSD')
    #tokenStr = driver.find_element_by_id('captcha').get_attribute("src")
    #print('tokenStr' + tokenStr)
    #os.remove("./verifyPic.png")
    #downloadUrlImage(tokenStr , "verifyPic.png")
    '''
    #getCaptureCodePic(driver , 'captcha' , './trainData/html_crop.png' , 1000)
    #batchGreyPic('./trainData' , './grepTrainData')
    batchConvertTiffPic("./grepTrainData" , "./grepTrainTiff" , "png")
    '''
    cropImage = capTurePicByName(driver , 'captcha' , "html_full.png")
    if os.path.exists("./trainData/html_crop.png"):
        print("the file is exist!")
    else:
        cropImage.save("./trainData/html_crop.png")
    '''
    #certText = recongnizePicText("bhtml_crop.png" , "T")
    #recognizeImag  = Image.open("Tbhtml_crop.png")
    #certText = pytesseract.image_to_string(recognizeImag,lang="eng",config="-psm 7") ###config="-psm 7"

    #print('certText :' + certText)
    #time.sleep(2000)
def main():
    url = "http://www.yunarm.com/admin"
    openBrower(url)


if __name__ == '__main__':
    main()

#brower  = webdriver.Chrome()
#soup = BeautifulSoup(page, "html.parser")
# print(soup)
# str = soup.find('div' , class="layui-layout layui-layout-admin")
#str  = soup.find_all(name='div' , attrs ={"class": "layui-form-item"})
# print(str)
'''
#tableBox = soup.find('layui-tab-item', class_='layui-tab-box')
tabCard = soup.find('layui-tab layui-tab-card')
layuiTableBox = tabCard.find('div' , class_='layui-table-box')
tableBox = layuiTableBox.find('table' , class_='layui-table')
for link in tableBox.find_all('tr'):
	name = link.find(attrs={'data-field':'ip'})
	print(name.get_text('title'))
#tableMain = table.find();

#for link in tb.find_all('b'):

#name = link.find('a')

#print(name.get_text('title'))'''
