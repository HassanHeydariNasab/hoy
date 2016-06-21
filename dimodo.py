#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys
import os
import telepot
from telepot.delegate import per_chat_id, create_open
import re
import subprocess
from time import sleep

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
        user_id = msg['from']['id']
        
        r = ''
        if m[0] == u'mojose':
            r = msg
        elif user_id == 170378225:
            '''
            if m[1] == u'source':
                f = open("bot.py", 'r')
                self.sender.sendDocument(f)
            elif and m[1] == u'k':
                process = subprocess.Popen(['/bin/bash'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                process.stdin.write('(sleep 5 && ./bot_killer.sh)&\n')
                sleep(2)
                process.kill()
                #print process.stdout.readline()
            '''
            process = subprocess.Popen(['/bin/bash'], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,bufsize = 1, universal_newlines = True)
            process.stdin.write(mr+';echo nenio!\n')
            r = process.stdout.readline()
            process.kill()
            if r == "":
                r = "error!"
            if len(r) > 4000:
                r = u'too long!'
       
        self.sender.sendMessage(r,parse_mode='HTML')

TOKEN = '208704782:AAErS5HiEKZxBuIAwOm4LP3zoZEBqVOSGxQ'
bot = telepot.DelegatorBot(TOKEN, [
    (per_chat_id(), create_open(Babilo, timeout=1)),
])
bot.message_loop(run_forever=True)
