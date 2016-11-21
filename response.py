# coding=utf-8
import time

import Contant
from act import activity, user, sql


def get_time():
    TIMEFORMAT = '%Y-%m-%d %X'
    return time.strftime(TIMEFORMAT)


def time_sec_to_str(time_sec):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_sec))


def resp_menu_event(render,myid,userid,eventkey):
    if eventkey=='V1':
        msg='请使用new命令创建活动\n用法如下：\nnew活动标题 活动备注'
        return render.reply_text(userid, myid, int(time.time()), msg)
    elif eventkey=='V2':
        u= sql.select_user(userid)
        if u.last_act_id!=-1:
            act= sql.select_act(u.last_act_id)
            return render.reply_text(userid, myid, int(time.time()), show_act(act))
        else:
            return render.reply_text(userid, myid, int(time.time()), '你还没有参与过活动。')


def resp_event(render,event,myid,userid):
    if event == "subscribe":
        u= user.user(userid, time.time())
        sql.insert_user(u)
        return render.reply_text(userid, myid, int(time.time()),Contant.WELCOME)
    elif event=="unsubscribe":
        sql.delete_user(userid)


def resp_text(render,myid,userid,content):
    content=content.strip()
    if content.startswith('new'):
        msg=activity.create_act(userid,content[3:])
        return render.reply_text(userid,myid,int(time.time()),msg)
    elif content.startswith('join'):
        msg=activity.join_act(userid,int(content[4:]))
        return render.reply_text(userid, myid, int(time.time()), msg)