from flask import Flask,jsonify,request
import datetime
import jwt
import mysql.connector

app=Flask(__name__)

app.config['SECRET_KEY']='Atif'

try:
    db=mysql.connector.connect(
        host="localhost",
        user="root",
        password="inandout",
        database="qc_portal_db"
    )
    db.autocommit=True
    print("DB connection successful.")
except Exception as e:
    print("DB connection was not successful.",e)

class User:
    @staticmethod
    def generate_token(user_id):
        payload={
            'user_id':user_id,
            'expire':(datetime.datetime.now()+datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
        }
        token=jwt.encode(payload,app.config['SECRET_KEY'])
        return token.encode('utf-8')
    
    @staticmethod
    def find_user(username,password):
        cur=db.cursor()
        cur.execute("SELECT * FROM users where username=%s AND password=%s",(username,password))
        user=cur.fetchone()
        cur.close()
        return user

    @staticmethod
    def get_available_users():
        cur=db.cursor()
        cur.execute("SELECT * FROM users WHERE availability=1")
        available_users=cur.fetchall()
        cur.close()
        return available_users
    
class Task:
    @staticmethod
    def get_pending_tasks_for_user(user_id):
        cur=db.cursor()
        cur.execute("SELECT * FROM tasks WHERE status='Pending' AND assigned_user_id=%s",(user_id,))
        pending_tasks=cur.fetchall()
        cur.close()
        return pending_tasks
    
    @staticmethod
    def assign_to_user(task_id:int,user_id:int)->None:
        cur=db.cursor()
        cur.execute("UPDATE tasks SET status = 'Assigned', assigned_user_id = %s WHERE task_id = %s",(user_id,task_id))
        cur.close()
        
    @staticmethod
    def mark_completed(task_id):
        cur=db.cursor()
        cur.execute("UPDATE tasks SET status = 'Completed' WHERE task_id = %s", (task_id,))
        cur.close()

# Task.mark_completed(5)
# print(Task.get_pending_tasks_for_user(22))


@app.route("/login",methods=['POST'])
def login():
    data=request.get_json()
    username=data['username']
    password=data['password']
    
    user=User.find_user(username,password)
    if(user):
        token=User.generate_token(user[0])
        return jsonify({'token':token})
    else:
        return jsonify({'message':'Invalid Credentials'}),401

@app.route("/availability",methods=["PUT"])
def update_availability():
    data=request.get_json()
    user_id=data['user_id']
    availability=data['availability']

    cur=db.cursor()
    cur.execute("UPDATE users SET availability=%s WHERE user_id=%s",(availability,user_id))
    cur.close()
    return jsonify({"message":"Availability updated"})


@app.route("/assign_task",methods=["POST"])
def assign_task():
    data=request.get_json()
    task_id=data['task_id']

    available_users=User.get_available_users()

    if not available_users:
        return jsonify({"message":"No available users to assign task"})
    
    Task.assign_to_user(task_id,available_users[0][0])

    return jsonify({"message":"Task assigned"})


@app.route("/complete_task",methods=['POST'])
def complete_task():
    data=request.get_json()
    task_id=data["task_id"]
    user_id=data["user_id"]

    Task.mark_completed(task_id)

    pending_tasks=Task.get_pending_tasks_for_user(user_id)
    if(pending_tasks):
        return jsonify({'message':'Task Completed, next task is Pending'})
    else:
        return jsonify({'message':'Task Completed, no task is pending'})


if __name__ == '__main__':
    app.run()

    
# Task.mark_completed(5)
# # print(User.generate_token("xcv"))
# cur=db.cursor()
# cur.execute("Select * from users")
# res=cur.fetchall()
# print(res)

# u="fraz@gmail.com"
# p="fraz123"
# user=User.find_user(u,p)
# print(user)

# print(User.get_available_users())

# print(Task.get_pending_tasks_for_user())

# print(Task.assign_to_user(3,22))