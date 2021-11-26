from django.shortcuts import render
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
    cursor = connection.cursor()
    cursor.execute("select email_id from users ")
    record = cursor.fetchall()
    cursor.close()
    ## Upcoming interviews list
    names, emails,start_time, end_time, interview_id = show_upcoming_interviews()
    res = zip( names,emails, start_time,end_time, interview_id)
    context = dynamic_dict(context,'records',res)

    emails = []
    if(len(record) >0):
        for li in record:
            emails.append(li)

    
    context = dynamic_dict(context,'email1',emails[0][0])
    context = dynamic_dict(context,'email2',emails[1][0])
    context = dynamic_dict(context,'email3',emails[2][0])
    context = dynamic_dict(context,'email4',emails[3][0])
    context = dynamic_dict(context,'email5',emails[4][0])
    
    
    if request.method == "POST" :
        print("Kamya Krishna",request.POST.get('button_value'))
        if request.POST.get('button_value'):
            button_clicked = request.POST['button_value']
            if button_clicked == 'delete' :
                print("'delete=========")
                interview_id = request.POST['interview_id']
                print(interview_id)
                
                print(start_time , end_time, "Krishna+++++++++++++++++++++++++++++++++++")
                res_delete = delete_interview(interview_id, start_time, end_time)
                if(res_delete):
                    messages.success(request, 'Deleted')
                    names, emails,start_time, end_time, interview_id = show_upcoming_interviews()
                    res = zip( names,emails, start_time,end_time, interview_id)
                    context = dynamic_dict(context,'records',res)
                    return render(request, 'index.html', context)
                else:
                    messages.error(request, 'Cannot delete because no. of candidates must be greater than 2')
                    
                    return render(request, 'index.html', context)
        else:
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
                
                print(validate , "Krishnaaaa help")
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
                    messages.success(request, 'Interview Scheduled Please Refesh!!!!!')
                    return render(request, 'index.html', context)
                else:
                    messages.error(request, 'Candidates are not available ')
    #return HttpResponse('Home Page is working')
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
        start_time = row[1].strftime("%m/%d/%Y, %H:%M:%S")
        startTime.append(start_time)
        end_time = row[2].strftime("%m/%d/%Y, %H:%M:%S")
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
                

def delete_interview(interview_id, start_time, end_time):
        
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
            
       
