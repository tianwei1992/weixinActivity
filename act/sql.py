# coding=utf-8
import MySQLdb
import activity, user
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


'''
sae.const.MYSQL_DB      # 数据库名
sae.const.MYSQL_USER    # 用户名
sae.const.MYSQL_PASS    # 密码
sae.const.MYSQL_HOST    # 主库域名（可读写）
sae.const.MYSQL_PORT    # 端口，类型为<type 'str'>，请根据框架要求自行转换为int
sae.const.MYSQL_HOST_S  # 从库域名（只读）
'''


def intlist_to_strlist(intlist):
    return [str(i) for i in intlist]


def strlist_to_intlist(strlist):
    return [int(i) for i in strlist]


class mysql:
    def __init__(self):
        try:
            from sae.const import MYSQL_DB, MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT
            self.conn = MySQLdb.connect(
                host=MYSQL_HOST,
                port=int(MYSQL_PORT),
                user=MYSQL_USER,
                passwd=MYSQL_PASS,
                db=MYSQL_DB,
                charset='utf8'
            )
            self.cur = self.conn.cursor()
        except:
            self.conn = MySQLdb.connect(
                host='w.rdc.sae.sina.com.cn',
                port=3307,
                user='ylxxyj451l',
                passwd='444y0yzwzlx125i5m2wxlyll25mywyhx2yj4h1mk',
                db='app_activity',
                charset='utf8'
            )
            self.cur = self.conn.cursor()

    def close(self):
        self.cur.close()
        self.conn.close()

    def insert_act(self,act):
        str_id_list = ' '.join(intlist_to_strlist(act.id_list))
        sql = "insert into Activity VALUE " "(%d,'%s','%s',%f,%d,'%s','%s')" \
              % (act.act_id, act.create_userid, act.title, act.date, act.num, str_id_list, act.remark)
        print sql
        print self.cur.execute(sql)
        self.conn.commit()
        self.close()

    def get_max_actid(self):
        # 默认表不为空
        sql = 'select max(act_id) from Activity'
        self.cur.execute(sql)
        id = self.cur.fetchall()[0][0]
        # print type(id)
        # print id
        self.close()
        return int(id)

    def update_act(self,act, title=False, id_list=False, remark=False):
        if title:
            sql = "update Activity set title='%s' where act_id=%d" % (act.title, act.act_id)
            self.cur.execute(sql)
        if id_list:
            sql = "update Activity set id_list='%s',num=%d where act_id=%d" % (' '.join(act.id_list), act.num + 1, act.act_id)
            self.cur.execute(sql)
        if remark:
            sql = "update Activity set remark='%s' where act_id=%d" % (act.remark, act.act_id)
            self.cur.execute(sql)
        self.conn.commit()
        self.close()

    def select_act(self,act_id):
        sql = "select * from Activity where act_id=%d" % act_id
        count = self.cur.execute(sql)
        if count == 0:
            return
        result = self.cur.fetchall()[0]
        print result
        act = activity.activity(act_id)
        act.create_userid=result[1]
        act.title = result[2]
        act.date = result[3]
        act.num = int(result[4])
        act.id_list = result[5].split()
        act.remark = result[6]
        self.close()
        return act

    def insert_user(self,u):
        str_act_list = ' '.join(intlist_to_strlist(u.create_act_list))
        str_join_list = ' '.join(intlist_to_strlist(u.join_act_list))
        sql = "insert into user VALUE ('%s','%f','%s','%s',%d,%d)" % (
        u.user_id, u.subscribe_date, str_act_list, str_join_list, u.state, u.last_act_id)
        print sql
        self.cur.execute(sql)
        self.conn.commit()
        self.close()

    def select_user(self,user_id):
        sql = "select * from user where user_id='%s'" % user_id
        self.cur.execute(sql)
        result = self.cur.fetchall()[0]
        u = user.user(user_id, float(result[1]))
        # u.subscribe_date=result[1]
        u.create_act_list = strlist_to_intlist(result[2].split())
        u.join_act_list = strlist_to_intlist(result[3].split())
        u.state = int(result[4])
        u.last_act_id = int(result[5])
        self.close()
        return u

    def update_user(self,u, flag=0):
        # flag=0更新create_act_list   flag=1更新join_act_list
        if flag == 0:
            str_act_list = ' '.join(intlist_to_strlist(u.create_act_list))
            sql = "update user set create_act_list='%s',last_act_id=%d where user_id='%s'" % (str_act_list, u.create_act_list[-1],u.user_id)
            self.cur.execute(sql)
        elif flag == 1:
            str_join_list = ' '.join(intlist_to_strlist(u.join_act_list))
            sql = "update user set join_act_list='%s',last_act_id=%d where user_id='%s'" % (str_join_list,u.join_act_list[-1], u.user_id)
            self.cur.execute(sql)
        self.conn.commit()
        self.close()

    def delete_user(self,userid):
        sql = "delete from user where user_id='%s'" % userid
        self.cur.execute(sql)
        self.conn.commit()
        self.close()


if __name__ == '__main__':
    # print mysql().get_max_actid()
    # u= mysql().select_user('o6ngQv5DAxoOoABubGsPCYLynFFc')
    # u.create_act_list.append(4)
    # print u.create_act_list
    # mysql().update_user(u)
    # act=mysql().select_act(5)
    # print act,act.title,act.remark
    act=activity.activity(6)
    act.id_list=['o6ngQv5DAxoOoABubGsPCYLynFFc','isjdighsudghskg']
    mysql().update_act(act,id_list=True)

# def create_act_table():
#     sql='''create table IF NOT EXISTS Activity(
# act_id int(10) NOT NULL UNIQUE ,
# create_userid VARCHAR(50) ,
# title VARCHAR(30) not NULL ,
# date FLOAT NOT null,
# num int not NULL ,
# id_list TEXT,
# remark varchar(100))'''
#     cur.execute(sql)
#
#
# def create_user_table():
#     sql='''create table if not EXISTS user(
# user_id varchar(50) not NULL ,
# subscribe_date FLOAT ,
# create_act_list TEXT ,
# join_act_list TEXT ,
# state int,
# last_act_id VARCHAR(50))'''
#     cur.execute(sql)
#     conn.commit()















