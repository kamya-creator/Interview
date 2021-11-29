from django.shortcuts import render, redirect
from django. http import HttpResponse
from django.db import connection
from django.contrib import messages
from django.core.mail import message, send_mail
from django.core.mail import EmailMultiAlternatives
import datetime
# Create your views here.

# This function used for creating key value pair which is used in context for sending to frontend
def dynamic_dict(sample_dict, key, value):
    if key not in sample_dict:
        sample_dict[key] = value
    return sample_dict

# index page call this function whenerver page get load
def home(request):
    context = {}
    
    if request.method == "POST" :
        if request.POST.get("button_value_edit") == "edit":
            button_clicked = request.POST['button_value_edit']
            interview_id_edit = request.POST['interview_id_edit']
            start_time, end_time , email= edit(request, interview_id_edit)
            global interview_id_update 
            interview_id_update = interview_id_edit
            context = dynamic_dict(context,'start_time',start_time)
            context = dynamic_dict(context,'end_time',end_time)
            context = dynamic_dict(context, 'selected', email)
            context = dynamic_dict(context, 'show_update_button', "1")

                    

        elif request.POST.get("button_value") == "delete":
            button_clicked = request.POST['button_value']
            if button_clicked == 'delete' :
                print("'delete=========")
                interview_id = request.POST['interview_id']
                print(interview_id)
                
                res_delete = delete_interview(interview_id)
                if(res_delete):
                    messages.success(request, 'Deleted')
                    '''names, emails,start_time, end_time, interview_id = show_upcoming_interviews()
                    res = zip( names,emails, start_time,end_time, interview_id)
                    context = dynamic_dict(context,'records',res)'''
                else:
                    messages.error(request, 'Cannot delete because no. of candidates must be greater than 2')
                    


        elif request.POST.get('button_value_update'):
            button_clicked = request.POST['button_value_update']
            if button_clicked == 'update_interview' :
                print("Krishna")
                print("I M HERE")
                interview_id = interview_id_update 
                end_Time = request.POST['end_Time']
                start_Time = request.POST['start_Time']
                print(end_Time, "+++++++++++++++++++++++++")
                update(request , interview_id,start_Time, end_Time)

                    
                           
        else: ###################### ADD INTERVIEW BUTTON IS CLICKED
            email2 = request.POST.getlist("list")
            if(len(email2)<2):
                
                names, emails,start_time, end_time, interview_id = show_upcoming_interviews()
                res = zip( names,emails, start_time,end_time, interview_id)
                context = dynamic_dict(context,'records',res)
                messages.error(request, 'Number of candidates must be greater than 2')
                return render(request, 'index.html', context)

            else :

                email2 = request.POST.getlist("list")
                start = request.POST['start_Time']
                end = request.POST['end_Time']
                
                validate = checking(email2, start,end)
                link = "https://meet.google.com/upb-kvky-xqf"
                
                if validate :
                    print("Good Luck")
                    start_time = start + ":00"
                    end_time = end + ":00"
                    start_time = start_time.replace('T', " ")
                    end_time = end_time.replace('T', " ")
                    
                    for e in email2:
                        cursor = connection.cursor()
                        cursor.execute("Select name from users where email_id =%s",[e] )
                        name = cursor.fetchone()
                        cursor.close()

                        cursor = connection.cursor()
                        cursor.execute("INSERT INTO interviews(Email, name ,startTime,endTime) values( %s , %s, %s, %s)",[e, name, start_time, end_time])
                        if cursor.rowcount == 1:
                                print("Inserted correctly!")
                                
                        cursor.close()
                    subject = "Invitation for Interview"
                    text_message = "Congratulations you have cleared round 1 , meet us in round 2 Interview" + " "+ link + "\n" 
                    text_message = text_message + " From : " + start_time + " \n" +  " To " + end_time
                    recipitent = []
                    for email in email2:
                        
                        cursor = connection.cursor()
                        cursor.execute("Select name from users where email_id =%s",[e] )
                        name = cursor.fetchone()[0]
                        cursor.close()
                        recipitent.append(email)
                    
                    send_email(subject=subject, text_content=text_message, sender = "interviewb08@gmail.com" , recipient = recipitent)
                    
                    names, emails,start_time, end_time, interview_id = show_upcoming_interviews()
                    res = zip( names,emails, start_time,end_time, interview_id)
                    context = dynamic_dict(context,'records',res)
                    messages.success(request, 'Interview Scheduled ')
                    
                else:
                    messages.error(request, 'Candidates are not available ')
    #return HttpResponse('Home Page is working')


    cursor = connection.cursor()
    cursor.execute("select email_id from users ")
    record = cursor.fetchall()
    cursor.close()
    emails = []
    if(len(record) >0):
        for li in record:
            emails.append(li)

    
    context = dynamic_dict(context,'email1',emails[0][0])
    context = dynamic_dict(context,'email2',emails[1][0])
    context = dynamic_dict(context,'email3',emails[2][0])
    context = dynamic_dict(context,'email4',emails[3][0])
    context = dynamic_dict(context,'email5',emails[4][0])

    ## Upcoming interviews list
    names, emails_list,start_time, end_time, interview_id = show_upcoming_interviews()
    res = zip( names,emails_list, start_time,end_time, interview_id)
    context = dynamic_dict(context,'records',res)

    



    return render(request, 'index.html', context)

    

def send_email(subject, text_content, sender="interviewb08@gmail.com", recipient=None):
    email = EmailMultiAlternatives(subject=subject, body=text_content, from_email=sender, to=recipient if isinstance(recipient, list) else [recipient])
    email.send()



def checking(emails, start_time, end_time):
    count = True
    start_time = start_time + ":00"
    end_time = end_time + ":00"
    start_time = start_time.replace('T', " ")
    end_time = end_time.replace('T', " ")
    for email in emails:
        cursor = connection.cursor()
        cursor.execute("select count(*) from interviews where Email=  %s ",[email])
        flag = cursor.fetchone()
        print("IIIIIIIIIIIIIIII", flag)
        cursor.close()
        if flag[0] == 0 :
                count = True
                
        else:
            cursor = connection.cursor(); 
            cursor.execute("select count(*) from interviews where Email = %s and startTime <=%s and endTime >=%s",[email,start_time, start_time])
            
            flag2 = cursor.fetchone()
            cursor.close()
            print(flag2[0], "-----------------------KKKKKKKKKKKKKKKKKK")
            if(flag2[0] > 0):
                count = False
                #print(count)
                return False     

    if(count == False):
        print(count)
        return False
    else :
        return True     


def show_upcoming_interviews():
    
    # dd/mm/YY H:M:S
    context = {}
    dt_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #print("date and time =", dt_string)
    cursor = connection.cursor(); 
    cursor.execute("select  Email, startTime , endTime , id from interviews where  startTime >=%s ",[dt_string])
    records = cursor.fetchall()
    cursor.close()
    interview_id = []
    emails = []
    startTime = []
    endTime = []

    for row in records:
        emails.append(row[0])
        start_time = row[1].strftime("%d-%m-%Y,  %H:%M:%S")
        startTime.append(start_time)
        end_time = row[2].strftime("%d-%m-%Y,   %H:%M:%S")
        endTime.append(end_time) 
        interview_id.append(row[3])

    #print(interview_id)
    names = []
    for e in emails:
        
        cursor = connection.cursor(); 
        cursor.execute("select name from users where email_id=%s ",[e])
        records = cursor.fetchone()
        names.append(records[0])
        

    return names,emails, startTime, endTime, interview_id
                

def delete_interview(interview_id):
        
        cursor = connection.cursor(); 
        cursor.execute("select startTime, endTime from interviews where id=%s ",[interview_id])
        record = cursor.fetchone()
        cursor.close()
        delete_start_time = record[0]
        delete_end_time = record[1]

        
        cursor = connection.cursor(); 
        cursor.execute("select count(*) from interviews where startTime=%s and endTime =%s ",[delete_start_time,delete_end_time])
        record_count = cursor.fetchone()[0]
        cursor.close()

        if record_count -1 >= 2:
            cursor = connection.cursor(); 
            cursor.execute("delete from interviews where id=%s ",[interview_id])
            cursor.close()
            return True
        else :
            return False    
            

def edit(request, interview_id_edit):
    
    interview_id_edit = (int)(interview_id_edit)
    
    cursor = connection.cursor(); 
    cursor.execute("select startTime , endTime , email from interviews where id=%s ",[interview_id_edit])
    record = cursor.fetchone()
    cursor.close()
    start_time = record[0]
    end_time= record[1]
    email = record[2]

    start_time = record[0].strftime("%Y-%m-%dT%H:%M:%S")
    
    end_time = record[0].strftime("%Y-%m-%dT%H:%M:%S")

    return start_time, end_time  , email 

def update(request , interview_id,start_updated, end_updated) :
   
    start_updated = start_updated.replace('T', " ")
    end_updated = end_updated.replace('T', " ")
    
    cursor = connection.cursor(); 
    cursor.execute("Update interviews set startTime=%s, endTime=%s where id=%s ",[start_updated, end_updated, interview_id])
    record = cursor.fetchone()
    cursor.close()
    
    messages.success(request, 'Interview Updated Successfully ')
    return
    ########## Checking if candidate is available or not in this time slot
    '''validate = checking(email, start_updated, end_updated)
    if(validate):
        update(interview_id_edit, start_updated, end_updated)
        messages.success(request, 'Updated Successfully')
    else:
        messages.error(request, 'Candidate is not available in this time slot')  '''  
    
   
    
          
