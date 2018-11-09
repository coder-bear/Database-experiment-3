from flask import Flask
from flask import request
import traceback
import pymysql
db_app = Flask(__name__)

@db_app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Database Experiment</h1>'

@db_app.route('/trigger',methods=['GET'])
def trigger_form():
    return  '''<form action="/result" method="post">
            <p>Search Friend Procedure:<br>
            Friend ID:<input name="Friend's ID"><br>
            Nick name:<input name="Friend nick name"><br>
            </p>
            <p>Delete Friend Procedure: <br>
            Friend_ID:<input name="Delete_Friend_ID"><br>
            Nick name:<input name="Delete_nickname"><br>
            </p>
            <p>Insert comment Procedure:<br>
            Friend ID:<input name="Insert_Friend_ID"><br>
            Comment ID:<input name="Insert_comment_id"><br>
            Content:<input name="Comment_content"><br>
            </p>
            <p>Edit Comment Procedure: <br>
            Friend ID:<input name="Edit_Friend_ID"><br>
            Comment:<input name="Edit_comment"><br>
            Comment ID:<input name="Insert_comment_id_1"><br>
            </p>
             <p><button type="submit">Submit</button></p>
            </form>
            '''

@db_app.route('/trigger', methods=['POST'])
def trigger_procede():
    Search_flag = -1
    Delete_flag = -1
    Update_flag = -1
    Insert_flag = -1
    results = []
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='db1')
        cursor = conn.cursor()
        if(request.form["Friend's ID"]!= None or request.form["Friend nick name"]!=None):
             Search_flag = cursor.execute('CALL Search_friend(%s, %s)', args=(request.form["Friend's ID"],
                                                           request.form["Friend nick name"]))
             results = cursor.fetchall()
             print(results)
             conn.commit()
        if(request.form["Delete_Friend_ID"]!= None or request.form["Delete_nickname"]!=None):
            Delete_flag = cursor.execute('CALL Delete_friend(%s, %s)', args=(request.form["Delete_Friend_ID"],
                                                           request.form["Delete_nickname"]))
            conn.commit()
        if(request.form["Edit_Friend_ID"]!=None or  request.form["Insert_comment_id_1"]!= None or request.form["Edit_comment"]!=None ):
            Update_flag = cursor.execute('CALL Change_comment(%s, %s, %s)', args=(request.form["Edit_Friend_ID"],
                                                                request.form["Insert_comment_id_1"],
                                                                request.form["Edit_comment"]))
            conn.commit()
        if (request.form["Insert_Friend_ID"] != None or request.form["Insert_comment_id"] != None or request.form["Comment_content"] != None):
            Insert_flag = cursor.execute('CALL Insert_comment(%s, %s, %s)', args=(request.form["Insert_Friend_ID"],
                                                                request.form["Insert_comment_id"],
                                                                request.form["Comment_content"]))
            conn.commit()
    except Exception as e:
        #设计缺陷，多个错误需要多处调试
        print(e.__traceback__)
        return '''<h1>Insertion Error!</h1>'''

    finally:
        print(Search_flag, Delete_flag, Update_flag)
        Error_string = ""
        #swtich case 优化,list
        if Search_flag == 0:
            Error_string = Error_string + "Search Error<br>"
        if Delete_flag == 0:
            Error_string = Error_string + "Delete Error!<br>"
        if Update_flag == 0:
            Error_string = Error_string + "Update Error!<br>"
        if Insert_flag == 0:
            Error_string = Error_string + "Insertion Error!<br>"
        if Error_string.__len__() != 0:
            return  '''<h1>%s</h1>'''%(Error_string)
        if len(results) != 0:
            return '''<html>
                Select Data: Head file: %s <br>
                Nickname:%s <br>
                Friend ID:%s <br>
                Delete, Insertion, Update Successfully!
                </html>
                '''%(results[0][0], results[0][1], results[0][2])
        else:
            return '''
                No search, Other operatations are successful!
            '''

if __name__ == '__main__':
    db_app.run()
