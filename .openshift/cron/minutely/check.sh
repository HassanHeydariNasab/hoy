if  `pgrep "bot.py" >/dev/null 2>&1`
then
    echo "bot is Running"
else
    killall python &> /dev/null
    source $OPENSHIFT_HOMEDIR/python/virtenv/bin/activate
    python $OPENSHIFT_REPO_DIR/dimodo.py &
    python $OPENSHIFT_REPO_DIR/bot.py &
    disown
    echo 'done!'
fi
