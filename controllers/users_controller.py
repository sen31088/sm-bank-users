
from flask import request, render_template, url_for, redirect, Blueprint, session
from models.model_users import Userlogin, Userdata, Carddetails, Usertranscation, Beneficiarydetails
from models.model_users import  Adminlogin
from utils.sendmail import Sendmail
import os
from dotenv import  load_dotenv


users_ctrl = Blueprint("users", __name__, static_folder='static', template_folder='templates')


usertranscation = Usertranscation()
load_dotenv()
app_url = os.getenv("URL")
act_page = 'users'

@users_ctrl.route('/pending-users', methods=('GET','POST'))
def pending_users():
    user_session = session.get('username')
    if not user_session:
        #print("In Transfer functuon username is: ", user_found)
        return render_template('admin.index.html')
    
    else:
        user_session = session.get('username')
        input_userdata = {'userid': user_session}
        userdata_found = Adminlogin.find_data(input_userdata)
        if not userdata_found:
             return render_template('admin-index.html')
        else:
        #user_status ='Pending'
            Pending_user_login_found = Userlogin.find_pending_users()

            Pending_user_data_found = Userdata.find_pending_users()

            if not Pending_user_login_found:
                msg = 'No Users found for Activation'
                return render_template('pending-users.html', active_page = act_page, messages1 = msg, logedin_user = user_session)
            else:
                #Pending_list1 = []
                msg = 'Account Activation Pending/Suspended Users List'
                pending_user_list = []

                for i in Pending_user_login_found:
                    for j in Pending_user_data_found:
                        if i['userid'] == j['userid']:
                            merged_dict = {**i, **j}
                            merged_dict.pop('_id')
                            pending_user_list.append(merged_dict)
                Pending_user_values= [list(dict.values()) for dict in pending_user_list]

                #print("Pending_user_values: ", Pending_user_values)
                return render_template('pending-users.html', active_page = act_page, data = Pending_user_values, messages = msg, logedin_user = user_session)


@users_ctrl.route('/api/v1/approve-users', methods=('GET','POST'))
def approve_users():
    user_session = session.get('username')
    if not user_session:
        #print("In Transfer functuon username is: ", user_found)
        return render_template('admin.index.html')
    else:
        user_session = session.get('username')
        input_userdata = {'userid': user_session}
        userdata_found = Adminlogin.find_data(input_userdata)
        if not userdata_found:
            return render_template('admin-index.html')
        if request.method=='POST':
            user_input = request.form.getlist('input_userid')
            user_in = user_input[0]
            current_user_data = Userlogin.get_data_userid(user_in)
            current_status = current_user_data['Activation_status']
            status_to_update = 'Activated'
            for i in user_input:
                Userlogin.update(i, status_to_update)
                Userdata.update(i, status_to_update)
                userdata = Userlogin.get_data_userid(i)
                email_id = userdata['email']
                username_in = userdata['Name']
                recipient_email = email_id
                subject = 'SM Bank | Account Activation  Confirmation'
                if current_status == 'Pending':
                    body = 'Thanks for registring to SM Bank, your account is Activated. Please login'
                    message = render_template ('mail-activation.html', username_in = username_in, mail_body = body, login_url = app_url)
                    #message = 'Dear ' + username_in + ', \n \nThanks for registring to SM Bank, your account is Activated. Please login. \n\nRegards\nSM Bank'
                    Sendmail.send_email(recipient_email, subject, message)
                else:
                    body = 'Your account is Re-Activated. Please login'
                    message = render_template ('mail-activation.html', username_in = username_in, mail_body = body, login_url = app_url)
                    #message = 'Dear ' + username_in + ', \n \nThanks for registring to SM Bank, your account is Activated. Please login. \n\nRegards\nSM Bank'
                    Sendmail.send_email(recipient_email, subject, message)

    return redirect(url_for('users.pending_users'))

@users_ctrl.route('/user-details', methods=('GET','POST'))
def user_details():
    user_session = session.get('username')
    if not user_session:
        #print("In Transfer functuon username is: ", user_found)
        return render_template('admin.index.html')
    else:
        user_session = session.get('username')
        input_userdata = {'userid': user_session}
        userdata_found = Adminlogin.find_data(input_userdata)
        if not userdata_found:
             return render_template('admin-index.html')
        else:
            user_session = session.get('username')
            return render_template('user-details.html', active_page = act_page, logedin_user = user_session)

@users_ctrl.route('/api/v1/get-user-details', methods=('GET','POST'))
def api_get_user_details():
    user_session = session.get('username')
    if not user_session:
        #print("In Transfer functuon username is: ", user_found)
        return render_template('admin.index.html')
    else:
        user_session = session.get('username')
        input_userdata = {'userid': user_session}
        userdata_found = Adminlogin.find_data(input_userdata)
        if not userdata_found:
            return render_template('admin-index.html')
        if request.method=='POST':

            if 'radioaccno' in request.form:
                accnumber_in = request.form['accno']
                query = {"Accno": accnumber_in}
                userdata_found = Userdata.get_acc_data(query)
                msg = 'Account Number not found'
    
            if 'radiouserid' in request.form:
                userid_in = request.form['userid']
                userdata_found = Userdata.get_acc_data({"userid": userid_in})
                msg = 'User ID not found'
            if not userdata_found:
                return render_template('user-details.html', active_page = act_page, message = msg, logedin_user = user_session)
            else:
                trans_list1 = []
                msg = 'User Account Details'
                #print("Transcation found")
                for i in userdata_found:
                    del i['_id']
                    for j in i.values():
                        trans_list1.append(j)
                ##print(trans_list1)
                trans_list = [trans_list1[x:x+9] for x in range(0, len(trans_list1), 9)]
                ##print(trans_list)
                return render_template('user-details.html', active_page = act_page, accountfound = msg, data = trans_list, messages = msg, logedin_user = user_session)

@users_ctrl.route('/add-user', methods=('GET','POST'))
def add_user():
    user_session = session.get('username')
    if not user_session:
        #print("In Transfer functuon username is: ", user_found)
        return render_template('admin.index.html', logedin_user = user_session)
    else:
        user_session = session.get('username')
        input_userdata = {'userid': user_session}
        userdata_found = Adminlogin.find_data(input_userdata)
        if not userdata_found:
             return render_template('admin-index.html')
        else:
            user_session = session.get('username')
            return render_template('add-user.html', active_page = act_page, logedin_user = user_session)

@users_ctrl.route('/suspend-user', methods=('GET','POST'))
def suspend_user():
    user_session = session.get('username')
    if not user_session:
        #print("In Transfer functuon username is: ", user_found)
        return render_template('admin.index.html', logedin_user = user_session)
    else:
        user_session = session.get('username')
        input_userdata = {'userid': user_session}
        userdata_found = Adminlogin.find_data(input_userdata)
        if not userdata_found:
             return render_template('admin-index.html')
        else:
          return render_template('suspend-user.html', active_page = act_page, logedin_user = user_session)

@users_ctrl.route('/api/v1/suspend-user', methods=('GET','POST'))
def api_suspend_user():
    user_session = session.get('username')
    if not user_session:
        #print("In Transfer functuon username is: ", user_found)
        return render_template('admin.index.html')
    else:
        user_session = session.get('username')
        input_userdata = {'userid': user_session}
        userdata_found = Adminlogin.find_data(input_userdata)
        if not userdata_found:
            return render_template('admin-index.html')
        if request.method=='POST':

            if 'radioaccno' in request.form:
                accnumber_in = request.form['accno']
                user_confirmation_input = request.form.get("confirmation")
                query = {"Accno": accnumber_in}
                msg = 'Account Number not found'
                userdata_found = Userdata.get_acc_data(query)
                if userdata_found:
                    userid_in1 = userdata_found[0]
                    userid_in = userid_in1['userid']
                    acc_name = userid_in1['Name']
                    acc_number = userid_in1['Accno']
                    acc_status = userid_in1['Activation_status']
                    user_login_found = Userlogin.get_data_userid(userid_in)
                    email_id = user_login_found['email']
                    
            
            if 'radiouserid' in request.form:
                userid_in = request.form['userid']
                user_confirmation_input = request.form.get("confirmation")
                msg = 'User ID not found'
                userdata_found = Userdata.get_acc_data({"userid": userid_in})
                if userdata_found:
                    userid_in1 = userdata_found[0]
                    userid_in = userid_in1['userid']
                    acc_name = userid_in1['Name']
                    acc_number = userid_in1['Accno']
                    acc_status = userid_in1['Activation_status']
                    user_login_found = Userlogin.get_data_userid(userid_in)
                    email_id = user_login_found['email']
            
            if user_confirmation_input != 'yes':
               msg = "Please type yes"
               return render_template('suspend-user.html', active_page = act_page, message = msg, logedin_user = user_session)
                
            if not userdata_found:
                return render_template('suspend-user.html', active_page = act_page, message = msg, logedin_user = user_session)
            
          
            
            if acc_status == 'Suspended':
                msg = "Account is already Suspended status"
                return render_template('suspend-user.html', active_page = act_page, message = msg, logedin_user = user_session)

            if acc_status == 'Pending':
                msg = "Account is already Pending status"
                return render_template('suspend-user.html', active_page = act_page, message = msg, logedin_user = user_session)
            
            
            else:
                status_to_update = 'Suspended'
                Userlogin.update(userid_in, status_to_update)
                Userdata.update(userid_in, status_to_update)
                recipient_email = email_id
                username_in = acc_name
                subject = 'SM Bank | Account Suspended Notification'
                message = render_template ('mail-suspended.html', username_in = username_in)
                Sendmail.send_email(recipient_email, subject, message)

                return render_template('user-suspend-sucess.html', active_page = act_page, user_id = userid_in, accname = acc_name , accno = acc_number, logedin_user = user_session)

@users_ctrl.route('/delete-user', methods=('GET','POST'))
def delete_user():
    user_session = session.get('username')
    if not user_session:
        #print("In Transfer functuon username is: ", user_found)
        return render_template('admin.index.html', logedin_user = user_session)
    else:
        user_session = session.get('username')
        input_userdata = {'userid': user_session}
        userdata_found = Adminlogin.find_data(input_userdata)
        if not userdata_found:
             return render_template('admin-index.html')
        else:
          return render_template('delete-user.html', active_page = act_page, logedin_user = user_session)

@users_ctrl.route('/api/v1/delete-user', methods=('GET','POST'))
def api_delete_user():
    user_session = session.get('username')
    if not user_session:
        #print("In Transfer functuon username is: ", user_found)
        return render_template('admin.index.html')
    else:
        user_session = session.get('username')
        input_userdata = {'userid': user_session}
        userdata_found = Adminlogin.find_data(input_userdata)
        if not userdata_found:
            return render_template('admin-index.html')
        if request.method=='POST':
            
            if 'radioaccno' in request.form:
                accnumber_in = request.form['accno']
                query = {"Accno": accnumber_in}
                user_confirmation_input = request.form.get("confirmation")
                msg = 'Account Number not found'
                userdata_found = Userdata.get_acc_data(query)
                if userdata_found:
                    userid_in1 = userdata_found[0]
                    userid_in = userid_in1['userid']
                    acc_name = userid_in1['Name']
                    acc_number = userid_in1['Accno']
                    
            if 'radiouserid' in request.form:
                userid_in = request.form['userid']
                msg = 'User ID not found'
                user_confirmation_input = request.form.get("confirmation")
                userdata_found = Userdata.get_acc_data({"userid": userid_in})
                if userdata_found:
                    userid_in1 = userdata_found[0]
                    userid_in = userid_in1['userid']
                    acc_name = userid_in1['Name']
                    acc_number = userid_in1['Accno']

            if user_confirmation_input != 'yes':
               msg = "Please type yes"
               return render_template('delete-user.html', active_page = act_page, message = msg, logedin_user = user_session)
                
            if not userdata_found:
                return render_template('delete-user.html', active_page = act_page, message = msg, logedin_user = user_session)
          
            else:
                # Delete user id from user data
                Userdata.delete_data(userid_in)

                # Delete user from user login
                Userlogin.delete_data(userid_in)

                # Delete user card details
                Carddetails.delete_data(userid_in)

                # Delete user Benificiary details
                Beneficiarydetails.delete_data(userid_in)

                # Delete User Transcation
                col_transactions_enduser= userid_in + 'transactions'

                usertranscation.delete_col(col_transactions_enduser)


                return render_template('user-delete-sucess.html', active_page = act_page, user_id = userid_in, accname = acc_name , accno = acc_number, logedin_user = user_session)
