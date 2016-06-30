#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys

reload(sys)  
sys.setdefaultencoding('utf8')

import os
import telepot
from telepot.delegate import per_chat_id, create_open
import re
from random import choice
import BeautifulSoup
import urllib2
from peewee import *
import ast
#from playhouse.sqlite_ext import *
from fuzzywuzzy import fuzz
from hazm import Normalizer

if 'OPENSHIFT_DATA_DIR' in os.environ:
    db = SqliteDatabase(os.environ['OPENSHIFT_DATA_DIR']+'mchat.db')
else:
    db = SqliteDatabase('mchat.db')
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
        normalizer = Normalizer()
        #if msg.has_key(u'document'):
            #self.sender.downloadFile(msg[u'document'][u'file_id'], file_path="~/dl")
        m = msg['text'].split(' ')
        mr = msg['text']
        fn = msg['from']['first_name']
        chat_type = msg['chat']['type']
        user_id = msg['from']['id']
        r = ''
        if m[0] == u'/start':
            r = u'سلام به تو که اسمتو گذاشتی ' + unicode(fn)
        elif m[0] == u'mojose':
            r = msg
        if chat_type == 'private' and mr[:3] != u'هوی':
            mr = u'هوی ' + mr 
            m = mr.split(' ')
            
        if user_id == 170378225:
            #global ddd = {index, keyOf dd }
            global h_id
            global d
            global ddd
            global q2
            #get outputs from db
            if m[1] == u'g':
                try:
                    q = Hoy.select(User, Hoy).join(Chat).join(User).where(Hoy.hoy.contains(': 0')).get()
                    h_id = q.id
                    q2 = User.select().join(Chat).join(Hoy).where(Hoy.id==h_id)
                    d = ast.literal_eval(q.hoy)
                    o = ''
                    i = 0
                    d_iter = d.iteritems()
                    for (k, v) in (d_iter):
                        o += str(i)+' : '+k+' : '+str(v)+'\n'
                        i += 1
                    i = 0
                    d_k = d.keys()
                    dd = {}
                    for k in d_k:
                        dd[i] = k
                        i += 1
                    ddd = dd
                    inputs = ''
                    for i in q2:
                        inputs += i.user + '\n'
                    r = inputs+'\n-----------\n'+o
                    
                except:
                    r = 'چیزی برای تأیید نیست!'
            elif mr[4] == u'g' and '\n' in mr:
                mrc = mr[4:]
                mc = mrc.split('\n')
                user_input = mc[1]
                try:
                    q = Hoy.select(User, Hoy).join(Chat).join(User).where(User.user == user_input).get()
                    h_id = q.id
                    q2 = User.select(Hoy, User).join(Chat).join(Hoy).where(Hoy.id==h_id)
                    d = ast.literal_eval(q.hoy)
                    o = ''
                    i = 0
                    d_iter = d.iteritems()
                    for (k, v) in (d_iter):
                        o += str(i)+' : '+k+' : '+str(v)+'\n'
                        i += 1
                    i = 0
                    d_k = d.keys()
                    dd = {}
                    for k in d_k:
                        dd[i] = k
                        i += 1
                    ddd = dd
                    inputs = ''
                    for i in q2:
                        inputs += i.user + '\n'
                    r = inputs+'\n-----------\n'+o
                except:
                    r = 'نبود که!'
            #review items
            elif m[1] == u'r':
                o = ''
                i = 0
                d_iter = d.iteritems()
                for (k, v) in (d_iter):
                    o += str(i)+' : '+k+' : '+str(v)+'\n'
                    i += 1
                i = 0
                d_k = d.keys()
                dd = {}
                for k in d_k:
                    dd[i] = k
                    i += 1
                ddd = dd
                inputs = ''
                for i in q2:
                    inputs += i.user + '\n'
                r = inputs+'\n-----------\n'+o 
            #commit changes
            elif m[1] == u'c':
                d_i = d.items()
                for k, v in d_i:
                    if v == 0:
                        del d[k]
                Hoy.update(hoy=d).where(Hoy.id == h_id).execute()
                d = {}
                ddd = {}
                inputs = ''
                r = 'تغییرات ذخیره شد!'
            #change state of an item
            elif len(m) == 2:
                try:
                    i = int(m[1])
                    if d[ddd[i]] == 0:
                        d[ddd[i]] = 1
                    else:
                        d[ddd[i]] = 0
                    r = ddd[i] + ' : ' + str(d[ddd[i]])
                except:
                    pass
            #if m[1] == 'grupoj':
                
            
        
        #TODO merge same outputs
        if '\n' in mr and u'\nبگو\n' in mr and r == '':
            mrc = normalizer.normalize(mr[4:])
            mc = mrc.split('\n')
            say_index = mc.index(u'بگو')
            user_inputs = mc[:say_index]
            hoy_outputs = mc[say_index+1:]
            hoy_outputs = {k:0 for k in hoy_outputs}
            hoy_outputs_old = {}
            for user_input in user_inputs:
                try:
                    H = (Hoy.select().join(Chat).join(User).where(User.user==user_input))
                    hoy_outputs_old = H[0].hoy
                    h_id = H[0].id
                    hoy_outputs_old = ast.literal_eval(hoy_outputs_old)
                    del user_inputs[user_inputs.index(user_input)]
                except:
                    pass
            if hoy_outputs_old == {}:
                h = Hoy.create(hoy=hoy_outputs)
                r = u'پاسخ‌های شما در صف بررسی قرار گرفت. تا ارباب چی بگن!'
            else:
                try:
                    hoy_outputs.update(hoy_outputs_old)
                    update_query = Hoy.update(hoy=hoy_outputs).where(Hoy.id==h_id)
                    update_query.execute()
                    h = Hoy.get(Hoy.id==h_id)
                    r = u'پاسخ‌های شما نیز در صف بررسی قرار گرفت. تا ارباب چی بگن!'
                except Exception as e:
                    pass
                    #print e
            try:
                for user_input in user_inputs:
                    u, created = User.get_or_create(user=user_input)
                    if created:
                        Chat.create(user=u, hoy=h)
            except Exception as e:
                pass
                #print e
        
        elif '\n' in mr and u'\nنفهم' in mr and r == '' and user_id == 170378225:
            mrc = mr[4:]
            mc = mrc.split('\n')
            say_index = mc.index(u'نفهم')
            user_input = mc[:say_index]
            try:
                dq = User.delete().where(User.user==user_input[0])
                dq.execute()
                r = u'اطاعت! دیگر به چنین چیزی پاسخ نمی‌دهم.'
                #TODO delete u_id that not exist in User, from Chat
            except:
                r = u'چنین چیزی وجود ندارد!'
                
                
                
                
        elif m[0] == u'هوی':
            if re.search(u'تخم|کیر|کسخل|کون|کون|الاغ|الاق|جنده|گای|پستون|ممه|گوز|شاش|جیش|قبحه|جلق|جق|سگ|جاکش|گائ|گاتو|کیون|لاشی|گامو|فاک|ساک|کُس|کوس|کوص|کص|سکس|پورن|الکسیس|گاشو', mr) \
            or re.search(u'(^| )رید(.|$)', mr) or u'خرم' in m or u'خری' in m or u'خره' in m or u'گا' in m or u'شق' in m or u'منی' in m or re.search(u'(^| )حشری(.|$)', mr):
                r = choice([u'بی‌ادب :|', u'بی‌تربیت :|', u'بی‌شخصیت :|',u'عفت کلام داشته باش یه ذره :|', u'دهنتو آب بکش :|'])
            #elif m[1] == u'سلام' or m[1] == u'درود':
                #r = choice([u'سلام', u'علیک سلام'])
            elif len(m) >= 3 and m[1] == u'بگو':
                r = normalizer.normalize(mr[8:])
            elif len(m) == 3:
                m2 = m[1]+' '+m[2]
                if m2 == u'چه خبر؟':
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
            elif len(m) == 2:
                if m[1] == u'راهنما':
                    r = u'• به این شکل هوی را آموزش دهید:\n\
\n\
سلام\n\
درود\n\
بگو\n\
علیک سلام\n\
سلام حاجی\n\
\n\
!> دقت کنید که در یک پیام و در خط‌های جدا باشد.\n\
\n\
!> اگر در گروه آموزشش می‌دهید، ابتدا هوی بنویسید و سپس مثل بالا خطوط را وارد کنید. این دو شکل قابل قبول است:\n\
\n\
هوی سلام\n\
درود\n\
بگو\n\
علیک سلام\n\
سلام حاجی\n\
---------\n\
هوی\n\
سلام\n\
درود\n\
بگو\n\
علیک سلام\n\
سلام حاجی\n\
\n\
• آموخته‌ها پس از تأیید به نمایش در می‌آیند.\n\
\n\
!> آموخته‌هایی که به اشخاص مربوط است و جنبهٔ عمومی ندارد، تأیید نمی‌شود.\n\
!> آموخته‌های شامل حرف بد، توهین و… تأیید نمی‌شود.\n\
!> آموخته‌های دارای اشتباه نوشتاری تأیید نمی‌شود.\n\
\n\
• اگر مثلاً «سلام» برای هوی تعریف شده باشد، می‌تواند این‌گونه از پاسخ‌های «سلام» برای «هلو» هم استفاده کند:\n\
\n\
سلام\n\
هلو\n\
بگو\n\
علیک\n\
های\n\
سلام عزیز\n\
\n\
• اگر پیشنهادی دارید، به @HSN6789 پیام بدهید.'
            
            if r == '':
                mrr = mr[4:].replace(u'؟', u'').replace(u'.', u'').replace(u'!', u'').replace(u'می ', u'می').replace(u'می‌', u'می')
                mrr = normalizer.normalize(mrr)
                #print 'normalized user input:', mrr
                mm = mrr.split(' ')
                rgx = u''
                for w in mm:
                    rgx += w+'|'
                    if u'می' == w[:2] and u'‌' != w[2] and u' ' != w[2]:
                        rgx += u'می‌'+w[2:]+u'|'
                if len(mm) < 3:
                    rgx = u'(' + rgx[:-1] + u') '
                else:
                    rgx = u'(' + rgx[:-1] + u')? '
                rgx = rgx * len(mm)
                rgx = rgx[:-1]
                #print 'regex:', rgx
                try:
                    q = Chat.select(Chat, Hoy, User).join(User).switch(Chat).join(Hoy).where(User.user.regexp(rgx)).limit(10)
                    #print 'records founded (max 10):', len(q)
                    if len(q) == 0:
                        #try to fuzzy string and rematch
                        #print 'not found!'
                        raise
    
                    else:
                        n = 0
                        #rd = {n: ratio}
                        rd = {}
                        while n < len(q):
                            us = q[n].user.user
                            #print 'string founded: ', us
                            ratio = fuzz.ratio(us, mrr)
                            #print ratio
                            if ratio >= 40:
                                rd[n] = ratio
                            n += 1
                        #print rd
                        ho = ''
                        while len(ho) == 0:
                            maxn = max(rd.values())
                            n = rd.keys()[rd.values().index(maxn)]
                            hoo = q[n].hoy.hoy
                            #print 'founded a dict for', n
                            try:
                                ho = ast.literal_eval(hoo)
                                #print 'a valid dict:', ho
                                if 1 not in ho.values():
                                    #print 'this dict haven\'t any valid item'
                                    raise
                            except:
                                #print 'deleting', rd[n]
                                del rd[n]
                                #print 'deleted!'
                                ho = ''
                        try:
                            outputs = []
                            for key in ho.keys():
                                if ho[key]==1:
                                    outputs.append(key)
                            r = normalizer.normalize(choice(outputs))
                            w = r.split(' ')
                            if u'می' == w[-1][:2] and u'‌' != w[-1][2] and u' ' != w[-1][2]:
                                w[-1] = u'می‌'+w[-1][2:]
                            r = ' '.join(w)
                        except:
                            r = ''
                    if r == '':
                        raise
                except Exception as e:
                    if re.search(u'(نظرت|نظر تو) (در مورد|درباره|دربارهٔ|درباره ی|درباره‌ی|راجع به|راجب) .* (چیست|چیه)', mr):
                        r = choice([u'در مورد همه چی باید نظر بدم؟!', u'نظر خاصی ندارم.', u'در این زمینه صاحب نظر نیستم.'])
                    elif re.search(u'؟$', mr):
                        r = choice([u'چرا می‌پرسی؟', u'نپرس!', u'نمی‌دونم.'])
                    elif re.search(u'!$', mr):
                        r = choice([u'عجب!', u'چه جالب!'])
                    elif re.search(u'\.$', mr):
                        r = choice([u'این که پایان جمله‌ت نقطه گذاشتی خیلی عالیه! ولی معنی جمله‌ت رو نمی‌فهمم. یادم بده.'])
                    else:   
                        r = u'نمی‌فهمم چی می‌گی. بیا خصوصی یادم بده!'
                    #print 'erorr:', e
                    #r = e
        if len(r) > 0:            
            self.sender.sendMessage(r,parse_mode='HTML')

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == 'd':
            TOKEN = '185401678:AAF_7PbchYOIDAKpy6lJqX7z01IsFgDTksA'
    else:
        TOKEN = open(os.path.join(os.environ['OPENSHIFT_DATA_DIR'], 'token')).read()
    bot = telepot.DelegatorBot(TOKEN, [(per_chat_id(), create_open(Babilo, timeout=1)),])
    bot.message_loop(run_forever=True)

