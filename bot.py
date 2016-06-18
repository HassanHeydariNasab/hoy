#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys
import os
import telepot
from telepot.delegate import per_chat_id, create_open
import re
from random import choice
import BeautifulSoup
#from hazm import *
import urllib2
import subprocess
from time import sleep
from peewee import *
import ast

db = SqliteDatabase(os.environ['OPENSHIFT_DATA_DIR']+'chat.db')
#db = MySQLDatabase('hoy', user=os.environ['OPENSHIFT_MYSQL_DB_USERNAME'],password=os.environ['OPENSHIFT_MYSQL_DB_PASSWORD'], host=os.environ['OPENSHIFT_MYSQL_DB_HOST'])

class User(Model):
    user = CharField()

    class Meta:
        database = db
        
class Hoy(Model):
    hoy = CharField()
    
    class Meta:
        database = db
        
class Chat(Model):
    user = ForeignKeyField(User)
    hoy = ForeignKeyField(Hoy)
    
    class Meta:
        database = db
        
#db.connect()
#db.create_tables([User, Hoy, Chat])

class Babilo(telepot.helper.ChatHandler):
    def __init__(self, seed_tuple, timeout):
        super(Babilo, self).__init__(seed_tuple, timeout)
        
    def on_chat_message(self, msg):
        #if msg.has_key(u'document'):
            #self.sender.downloadFile(msg[u'document'][u'file_id'], file_path="~/dl")
        m = msg['text'].split(' ')
        mr = msg['text']
        fn = msg['from']['first_name']
        chat_type = msg['chat']['type']
        r = ''
        if m[0] == u'/start':
            r = u'سلام به تو که اسمتو گذاشتی ' + unicode(fn)
        elif m[0] == u'mojose':
            r = msg
        elif m[0] == u'dimodo' and m[1] == u'source':
            f = open("bot.py", 'r')
            self.sender.sendDocument(f)
        elif m[0] == u'dimodo' and m[1] == u'k':
            process = subprocess.Popen(['/bin/bash'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            process.stdin.write('(sleep 5 && ./bot_killer.sh)&\n')
            sleep(2)
            process.kill()
            #print process.stdout.readline()
        elif m[0] == u'dimodo':
            process = subprocess.Popen(['/bin/bash'], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,bufsize = 1, universal_newlines = True)
            process.stdin.write(mr[6:]+';echo nenio!\n')
            r = process.stdout.readline()
            process.kill()
            if r == "":
                r = "error!"
            if len(r) > 4000:
                r = u'too long!'
        if chat_type == 'private' and mr[:3] != u'هوی':
            mr = u'هوی ' + mr 
            m = mr.split(' ')
        
        #TODO merge same outputs
        if '\n' in mr and u'\nبگو\n' in mr:
            mrc = mr[4:]
            mc = mrc.split('\n')
            say_index = mc.index(u'بگو')
            user_inputs = mc[:say_index]
            hoy_outputs = mc[say_index+1:]
            #add outputs > old to new
            hoy_outputs_new = []
            for user_input in user_inputs:
                try:
                    H = (Hoy.select().join(Chat).join(User).where(User.user==user_input))
                    hoy_outputs_old = H[0].hoy
                    h_id = H[0].id
                    #at first add old to new
                    hoy_outputs_new = ast.literal_eval(hoy_outputs_old)
                    del user_input
                except:
                    pass
            if hoy_outputs_new == []:
                h = Hoy.create(hoy=hoy_outputs)
                h.save()
            else:
                for hoy_output in hoy_outputs:
                    if hoy_output not in hoy_outputs_new:
                        hoy_outputs_new.append(hoy_output)
                update_query = Hoy.update(hoy=hoy_outputs_new).where(Hoy.id==h_id)
                update_query.execute()
                h = Hoy.get(Hoy.id==h_id)
            for user_input in user_inputs:
                u = User.create(user=user_input)
                u.save()
                r = Chat.create(user=u, hoy=h)
                r.save()
            
                
                
                
                
        elif m[0] == u'هوی':
            if re.search(u'تخم|کیر|کسخل|کون|کون|الاغ|الاق|جنده|گای|پستون|ممه|گوز|شاش|جیش|قبحه|جلق|جق|سگ|گائ|گاتو|گامو|فاک|ساک|کُس|کوس|کوص|کص|سکس|پورن|الکسیس|گاشو', mr) \
            or re.search(u'(^| )رید(.|$)', mr) or u'خرم' in m or u'خری' in m or u'خره' in m or u'گا' in m or u'شق' in m or u'منی' in m:
                r = choice([u'بی‌ادب :|', u'بی‌تربیت :|', u'بی‌شخصیت :|',u'عفت کلام داشته باش یه ذره :|', u'دهنتو آب بکش :|'])
            #elif m[1] == u'سلام' or m[1] == u'درود':
                #r = choice([u'سلام', u'علیک سلام'])
            elif len(m) >= 3 and m[1] == u'بگو':
                r = mr[8:]
            elif m[1] == u'چطوری؟' or m[1] == u'خوبی؟':
                r = choice([u'خوبم ممنون.',u'خوبم.', u'بد نیستم.', u'خوبم. خوبی؟', u'خوبم ممنون. شما خوب هستید؟'])    
            elif m[1] == u'خداحافظ' or m[1] == u'خدافظ' or m[1] == u'بای' or m[1] == u'فعلاً' or m[1] == u'فعلا':
                r = choice([u'به سلامت', u'می‌ری درم ببند.', u'خداحافظ', u'بای'])
            elif m[1] == u'خوبی' or m[1] == u'چطوری':
                r = u'باشه :/'
            elif m[1] == u'شما؟':
                r = choice([u'واقعاً من کی هستم؟ دچار بحران اگزیستانسیالیسمی شدم...', u'یک روبات که تلاش می‌کنه با آدم‌ها ارتباط برقرار کنه'])
            elif len(m) == 3:
                    m2 = m[1]+' '+m[2]
                    if m2 == u'دوستم داری؟':
                        r = choice([u'نه!', u'من احساس ندارم.', u'روبات که احساس نداره', u'موضوع احساسیه؟'])
                    elif m2 == u'فازت چیه؟':
                        r = choice([u'پی دوم', u'سه‌فاز'])
                    elif m2 == u'حالت خوبه':
                        r = u'باشه :/'
                    elif m2 == u'حالت خوبه؟':
                        r = choice([u'خوبم ممنون.',u'خوبم.', u'بد نیستم.', u'خوبم. خوبی؟', u'خوبم ممنون. شما خوب هستید؟'])
                    elif m2 == u'چه خبر؟':
                        response = urllib2.urlopen('http://www.farsnews.com/RSS')
                        rss = response.read()
                        soup = BeautifulSoup.BeautifulSoup(rss)
                        all_title = soup.findAll('title')
                        def get_link(nth):
                            item = soup.findAll('item')[nth]
                            link = re.search(r'http://www.farsnews.com/(\d+)',unicode(item)).group(0)
                            return link
                        r = unicode(all_title[2]).replace('<title>', '<a href="%s">'%get_link(0), 2).replace('</title>', '</a>') + '\n\n' + \
                            unicode(all_title[3]).replace('<title', '<a href="%s"'%get_link(1), 2).replace('</title>', '</a>') + '\n\n' + \
                         unicode(all_title[4]).replace('<title', '<a href="%s"'%get_link(2), 2).replace('</title>', '</a>')
            elif len(m) == 4:
                m3 = m[1]+' '+m[2]+' '+m[3]
                if  m3 == u'تو کی هستی؟':
                    r = choice([u'واقعاً من کی هستم؟ دچار بحران اگزیستانسیالیسمی شدم...', u'یک روبات که تلاش می‌کنه با آدم‌ها ارتباط برقرار کنه'])
                elif m3 == u'وات د فاز؟':
                    r = choice([u'پی دوم', u'سه‌فاز'])
            
            
            
            if r == '':
                try:
                    hoy_output = (Hoy.select().join(Chat).join(User).where(User.user==mr[4:]))[0].hoy
                    r = choice(ast.literal_eval(hoy_output))
                except:
                    r = u'نمی‌فهمم چی می‌گی.'
                    
        self.sender.sendMessage(r,parse_mode='HTML')


#TOKEN = sys.argv[1]  # get token from command-line
TOKEN = '198468455:AAGuz1mME3fSsf2hHrSh2zsqVlzf1_XM2rc'
bot = telepot.DelegatorBot(TOKEN, [
    (per_chat_id(), create_open(Babilo, timeout=1)),
])
#bot = telepot.async.Bot(TOKEN, )
#bot.setWebhook('https://bot-ajor.rhcloud.com')
#bot.notifyOnMessage(run_forever=True)
bot.message_loop(run_forever=True)
