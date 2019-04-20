# -*- coding:utf-8 -*-
#版本一
from moviepy.video.VideoClip import  ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.fx.accel_decel import accel_decel
from moviepy.video.fx.blackwhite import blackwhite
from moviepy.video.fx.blink import blink
from moviepy.video.fx.crop import crop
from moviepy.video.fx.even_size import even_size
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from moviepy.video.fx.mirror_x import mirror_x
from moviepy.video.fx.mirror_y import mirror_y
from moviepy.video.fx.resize import resize

from moviepy.audio.fx.audio_fadein import audio_fadein
from moviepy.audio.fx.audio_fadeout import audio_fadeout
from moviepy.audio.fx.audio_left_right import audio_left_right
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
from moviepy.audio.fx.volumex import volumex
import os
import sys
import argparse
import pathlib
import time
import datetime
import fire


allpath=[]
allname=[] 
work_pat=r"D:\VideoEditing"
work_path=os.path.join(work_pat,datetime.datetime.now().strftime('%Y-%m-%d'))
#len_path=r"D:\MP4work\视频操作未成功"
if not os.path.isdir(work_path):
    os.makedirs(work_path)
        
def delmp4(filename,time1=0,time2=0,mv=0):
#剪切视频文件 路径文件名 去片头  去片尾  到片尾时间


    clip = VideoFileClip(filename)
    clip_len=clip.duration
    if time2==0 and mv>0:
         mvtime=mv
    else:
         mvtime=int(clip_len-time2)  
    if (clip_len-time1-time2)>0 and time1<clip_len and time2<clip_len and mv<clip_len:
    #if ((clip_len-time1-time2)>0 and mvtime==mv)  or (mv>time1 and mv<clip_len and mv>time2) :
        mvclip=clip.subclip(time1,mvtime)
        file_name = os.path.splitext(filename)[0]
        filen= os.path.basename(filename)
        mvclip.write_videofile(work_path+"\\"+filen)
        mvclip.close()
        #防止内存溢出,用完关闭!!!
    else:
        print("视频长度不够!!!!")
        if not os.path.isdir(work_path):
            os.makedirs(work_path)
        fo = open(work_path+"/错误!视频长度不够.txt", "a+")
        fo.write( filename+"\n")
        fo.close()
        #shutil.copy(file_name,len_path) 
        clip.close()    
    
def getallfile(path):
    allfilelist=os.listdir(path)
    # 遍历该文件夹下的所有目录或者文件
    for file in allfilelist:
        filepath=os.path.join(path,file)
        # 如果是文件夹，递归调用函数
        if os.path.isdir(filepath):
            getallfile(filepath)
        # 如果不是文件夹，保存文件路径及文件名
        elif os.path.isfile(filepath):
            if os.path.splitext(filepath)[1] == ".mp4":
                vfilepath=filepath.replace("\\","/")
                allpath.append(vfilepath)
                print(vfilepath)
                allname.append(file)
    return allpath, allname    
def check_dir(path):
    u"""
   用来判断是文件，还是文件夹的方法
       """
    my_path=pathlib.Path(path)
    ex = my_path.exists()
    if ex:
        is_dir = my_path.is_dir()
        is_file = my_path.is_file()
    else:
        is_dir=False
        is_file=False
    return ex,is_dir,is_file    
def fuck_dir(filedir,time1=0,time2=0,mv=0):
    mdir,mfilename=getallfile(filedir)
    #遍历mdir中MP4路径+文件名的数组
    for md in mdir:
        print (md)
        delmp4(md,time1,time2,mv)


def cut(file_path, mv_head_time=0, mv_end_time=0, end_time=0):
    u"""作者:huvipg
    
    参数         目录_文件名 去片头(秒)  去片尾=var(秒)  到片尾时间(当var==0,可选填时间)
                 功能:   剪辑视频文件 (如果参数是目录,会批量剪辑目录下所有视频) 
    """
    ex,is_dir,is_file=check_dir(file_path)
    print(ex,is_dir,is_file)
    if not ex:
        print("文件不存在！\n请重新输入")
    else:
        if is_dir:
           fuck_dir(file_path, mv_head_time, mv_end_time, end_time)
        elif is_file:
           delmp4(file_path, mv_head_time, mv_end_time, end_time)
def addmp4(head="",mp4="",end=""):
    L=[head,mp4,end]
    vl=[]
    ll=[]
    
    while "" in L:
        L.remove("")
    print (L)
    le=len(L)
    for v in range(le):
        t=VideoFileClip(L[v])
        ll.append(t)
    filen= os.path.basename(mp4)
    final_clip = concatenate_videoclips(ll,method='compose')
    final_clip.write_videofile(work_path+"\\"+filen)
    final_clip.close()           


def adddir(filedir="", head="",  end=""):
    mdir, mfilename = getallfile(filedir)
    for md in mdir:
        print(md)
        addmp4(md, head,  end)


def addmp4(mp4="", head="", end=""):
    L = [head, mp4, end]
    vl = []
    ll = []
    while "" in L:
        L.remove("")
    print(L)
    if not len(L) > 1:
        print("pass")
        pass
    else:
        le = len(L)
        for v in range(le):
           t = VideoFileClip(L[v])
           ll.append(t)
        filen = os.path.basename(mp4)
        final_clip = concatenate_videoclips(ll, method='compose')
        final_clip.write_videofile(work_path+"\\"+filen)
        final_clip.close()


def add(dir_or_file, head_file="", end_file=""):
    u"""作者:huvipg
    
    参数   视频名(文件名或目录)  添加片头   添加片尾 
           功能:   添加合并视频 (如果参数是目录,会批量为目录下所有视频添加片头) 
    """
    ex, is_dir, is_file = check_dir(dir_or_file)
    print(ex, is_dir, is_file)
    if not ex:
        print("文件不存在！\n请重新输入")
    else:
        if is_dir:
           adddir(dir_or_file, head_file,  end_file)
        elif is_file:
           addmp4(dir_or_file, head_file,  end_file)
def addlogo(file_dir,img="",time=20,X=30,Y=30):
   
    clip = VideoFileClip(file_dir)
    img_clip = ImageClip(img)   #位置
    img_clip = img_clip.set_pos((X,Y)).set_duration(time)
    clip = CompositeVideoClip([clip, img_clip])
    filen = os.path.basename(file_dir)
    clip.write_videofile(work_path+"\\"+filen)
    clip.close()
def dirlogo(file_dir,img="",time=20,X=30,Y=30):
    mdir, mfilename = getallfile(file_dir)
    for md in mdir:
        print(md)
        addlogo(md,img,time,X,Y)    
def logo(file_dir,img="",time=20,X=30,Y=30):
    u"""作者:huvipg
    
    参数   视频名(文件名或目录)  图片名 logo显示时间 logo位置_x logo位置y
           功能:   添加图片logo到视频 (如果参数是目录,会批量为目录下所有视频添加logo) 
    """
    ex, is_dir, is_file = check_dir(file_dir)
    print(ex, is_dir, is_file)
    if not ex:
        print("文件不存在！\n请重新输入")
    else:
        if is_dir:
           dirlogo(file_dir,img,time,X,Y)
        elif is_file:
           addlogo(file_dir,img,time,X,Y)
           

if __name__ == "__main__":
    #fire.Fire() 
    fire.Fire({'cut':cut,'add':add,'logo':logo}) 

    
    



