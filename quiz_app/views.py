from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student, Sub_Topic, Topic, Quiz, Question
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def index(request):
    logout(request)
    return render(request, 'quiz_app/index.html')

def aboutus(request):
    return render(request, 'quiz_app/aboutus.html')

@login_required(login_url="/sign_in_up_form/")
def quiz(request):
    return render(request,'quiz_app/quiz-default.html')

#To display main topics (Number,Algebra, Ratio etc)
@login_required(login_url="/sign_in_up_form/")
def quiz_sub_topics(request,pk):
    sub_topics = Sub_Topic.objects.filter(topic_id=pk)
    context = {
        'sub_top':sub_topics,
    }
    return render(request, 'quiz_app/quiz-questions.html', context)

#To display subtopics after main topic is selected
@login_required(login_url="/sign_in_up_form/")
def quiz_sub_topic_questions(request,pk, id):
    sub_topics = Sub_Topic.objects.filter(topic_id=pk)
    sub_topic_questions = Question.objects.filter(subtopic_id=id) 
    context = {
            'sub_top':sub_topics,
            'sub_top_que':sub_topic_questions,
    }  
    
    return render(request, 'quiz_app/quiz-questions.html', context)

#Directs to the sign in or sign up form
def sign_in_up_form(request):
    return render(request, 'quiz_app/sign_in_up_form.html')

#logging in user
def sign_in(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')          
        password = request.POST.get('password')  
        
        try:
            #checking if user exists
            student = Student.objects.get(username=username)
        except:
            #if user doesn't exis throuw an error message
            messages.error(request, 'User does not exist!')
        
        #User exists and now authenticating (checking username and password) user
        stud = authenticate(request,username=username,password=password)
        
        #When user is authenticated, they are directed to different pages
        #according to their privillages - admin (superuser) to admin page, user to quiz page
        if stud is not None:
            if stud.is_superuser:
                login(request,stud)
                return redirect('admin-home')
            else:
                login(request,stud)
                return redirect('quiz')
        else:
            messages.error(request, "Username or password doesn't exists!")
            return HttpResponse("Incorrect")

#logs out authenticated user 
def signout(request):
    logout(request)
    return redirect('index')
    
#users can sign up by themselves by providing their details
def register(request):
    
    if request.method == 'POST':
        
        email = request.POST.get('email')
        username = request.POST.get('username')          
        password = request.POST.get('password')           
                
        student = Student(email=email, username=username, password=password)
        
        #converts user password into a hash algorithm for security reasons
        #Random example -  password=johnsmith2  
        # (hash - pbkdf2_sha256$789047$qtS4Yssquerr7ncufMyH3z$SheYWFjnsU3vrOYsWy5nsPfIoFUeGY4/6U=)
        student.set_password(student.password)
        
        student.save()
                
        return render(request,'quiz_app/sign_in_up_form.html')   
                
    else: 
        return HttpResponse("Invalid request method!")
    
#View to help list down all users in a template
def admin_users(request):
    
    users = Student.objects.all()
    
    context = {
        'students':users,
    }
    return render(request, 'quiz_app/admin_users.html',context)

#view to help add a user in using a template (form)
def user_add_form(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        student = Student(email=email,username=username,password=password)
        
        context = {
            'stud':student
        }
    
        return render(request, 'quiz_app/user-add-form.html', context)

#view to help save user details in the DB using a template
def save_user(request):
    
    if request.method == 'POST':
        
        email = request.POST.get('email')
        username = request.POST.get('username')          
        password = request.POST.get('password')           
                
        student = Student(email=email, username=username, password=password)
        
        student.set_password(student.password)
        
        student.save()
                
        return redirect('admin-users')   
                
    else: 
        return HttpResponse("Invalid request method!")

#view to help update user details using a template
def user_update_form(request, pk):
    
    stud = Student.objects.get(student_id=pk)
    
    context = {
        'stud':stud,    
    }
    
    
    return render(request, 'quiz_app/user-update-form.html',context)

#view to help update user details in the DB
def user_update(request,pk):
    
    if request.method == 'POST':

        stud = Student.objects.get(student_id=pk)
        
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        stud.email = email
        stud.username = username
        stud.password = password
        
        stud.save()        
        
        return redirect('admin-users')
    
#view to help delete user from the DB
#pk an argument passed to view to pin point the user to be deleted
def user_delete(self, pk):
    
    stud = Student.objects.get(student_id=pk)
        
    stud.delete()        
        
    return redirect('admin-users')
 
#view to help list down all topics and subtopics using a template
def admin_topics(request):
    admin_sub_topics = Sub_Topic.objects.all()
    context = {
        'admin_sub_top':admin_sub_topics,
    }
    return render(request, 'quiz_app/admin-topics.html', context)

#view to help admin add a new subtopic using a template
def subtopic_add_form(request):
    topics = Topic.objects.all()
    
    context = {
        'topics':topics
    }   
    
    return render(request, 'quiz_app/subtopic-add-form.html', context)

#adds a new subtopic to DB and redirects to topic and subtopic list page
def admin_add_subtopic(request):
    if request.method == "POST":
        subtopic = request.POST.get('subtopic')
        
        subtop = Sub_Topic(sub_topic=subtopic, topic=Topic( request.POST.get('topic')))
        
        subtop.save()
        
        return redirect('admin-topics')

#view to help update a subtopic using a template
def subtopic_update_form(request, pk):
    
    update_subtopic = Sub_Topic.objects.get(sub_topic_id=pk)    
    topics = Topic.objects.all()
    
    context = {
        'update_subtopic':update_subtopic,
        'topics':topics,
    }
    
    return render(request,'quiz_app/subtopic-update-form.html',context)

#updates a subtopic in the DB
def subtopic_update(request, pk):
    if request.method == 'POST':
        
        subtop = Sub_Topic.objects.get(sub_topic_id=pk)
        
        topic = Topic(request.POST.get('topic'))
        subtopic = request.POST.get('subtopic')
        
        subtop.topic = topic
        subtop.sub_topic = subtopic        
        
        subtop.save()        
        
        return redirect('admin-topics')

#view to help delete a subtopic from the DB
def subtopic_delete(request, pk):
    subtop = Sub_Topic.objects.get(sub_topic_id=pk)
        
    subtop.delete()        
        
    return redirect('admin-topics')

#view to diplay admin page
def admin_home(request):
    return render(request, 'quiz_app/admin-home.html')

#displays a list of available questions
def admin_questions(request):
    admin_ques = Question.objects.all()
    
    context = {
        'admin_questions':admin_ques,
    }
    
    return render(request, 'quiz_app/admin-questions.html', context)

#view to help add a question using a template (form)
def question_add_form(request):
    subtopics = Sub_Topic.objects.all()
    
    context = {
        'subtopics':subtopics
    }   
    
    return render(request, 'quiz_app/questions-add-form.html', context)

#adds a new question to DB and redirects to questions list page
def admin_add_question(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        option_one = request.POST.get('option 1')
        option_two = request.POST.get('option 2')
        option_three = request.POST.get('option 3')
        option_four = request.POST.get('option 4')
        answer = request.POST.get('answer')
        subtopic = Sub_Topic(request.POST.get('subtopic'))
        
        ques = Question(question=question, option1= option_one,
                        option2=option_two,option3=option_three,
                        option4=option_four,answer=answer,subtopic=subtopic)
        
        ques.save()
        
        return redirect('admin-questions')

#view to help update a question using a template (form) 
def question_update_form(request, pk):
    
    update_question = Question.objects.get(question_id=pk)    
    subtopics = Sub_Topic.objects.all()
    
    context = {
        'update_question':update_question,
        'subtopics':subtopics,
    }
    
    return render(request,'quiz_app/question-update-form.html',context)

#updates a question in the DB
def question_update(request, pk):
    if request.method == 'POST':
        
        question = Question.objects.get(question_id=pk)
        
        quest = request.POST.get('question')
        subtopic = Sub_Topic(request.POST.get('subtopic'))
        
        question.sub_topic = subtopic  
        question.question = quest      
        
        question.save()        
        
        return redirect('admin-questions')
    
#deletes a questions from the DB    
def question_delete(request, pk):
    question = Question.objects.get(question_id=pk)
        
    question.delete()        
        
    return redirect('admin-questions')

#view to help generate stats 
def admin_stats(request):
    #Generating a report on number of
    #questions,Users(Students),Topics, Subtopics, Quizzes, Questions,
    questions = Question.objects.all().count()
    students = Student.objects.all().count()
    topics = Topic.objects.all().count()
    subtopics = Sub_Topic.objects.all().count()
    quizzes = Quiz.objects.all().count()
    subtopic_number = Sub_Topic.objects.filter(topic_id=1).count()
    subtopic_algebra = Sub_Topic.objects.filter(topic_id=2).count()
    subtopic_ratio_and_proportion = Sub_Topic.objects.filter(topic_id=3).count()
    subtopic_geometry_and_measurement = Sub_Topic.objects.filter(topic_id=4).count()
    subtopic_probability_and_statistics = Sub_Topic.objects.filter(topic_id=5).count()
    
    context = {
        'students':students,
        'topics':topics,
        'subtopics':subtopics,
        'quizzes':quizzes,
        'questions':questions,
        'subtopic_number':subtopic_number,
        'subtopic_algebra':subtopic_algebra,
        'subtopic_ratio_and_proportion': subtopic_ratio_and_proportion,
        'subtopic_geometry_and_measurement': subtopic_geometry_and_measurement,
        'subtopic_probability_and_statistics': subtopic_probability_and_statistics,
    }    
    
    return render(request, 'quiz_app/admin-stats.html', context)

#view to help work out quiz score    
def quiz_marked(request, pk):
    
    if request.method == "POST":
        #instiantiating a default Quiz object
        a_quiz = Quiz() 
        #filtering based on subtopic_id of questions
        for q in Question.objects.filter(subtopic_id=pk): #looping through questions of the same subtopic
            #getting responses for each question from a quiz(specific topic) 
            user_ans = request.POST.get(str(q.question_id))
            #storing user's responses in a list located in the quiz model
            a_quiz.user_answer_list.append(user_ans)
            #retrieving answers of each question from Question model and storing
            #answers in a list located in quiz model
            a_quiz.real_answers_list.append(q.answer)
        
        #getting credentials of logged in user- store in quiz   
        logged_student = request.user
        #retrieving subtopic of the quiz and storing this in quiz model
        subtopic = Sub_Topic.objects.get(sub_topic_id=pk)   
        #working out total number of questions (same subtopic) in the quiz             
        total_questions = Question.objects.filter(subtopic_id=pk).count()  
        #calling a method (get_result) in quiz (model) to work out how many questions user got correct
        mark = a_quiz.get_result()
        #getting score(mark) as a percentage from quiz(model) field
        mark_percentage = a_quiz.result_percentage 
        #re-instantiating a Quiz object before saving it to DB 
        a_quiz = Quiz(student=logged_student, subtopic=Sub_Topic(subtopic.sub_topic_id),mark=mark,total_number_of_questions=total_questions, 
                result_percentage=mark_percentage)
        #Filtering Quiz based on user
        quizzes = Quiz.objects.filter(student=logged_student)
        #filtering questions based on quiz's subtopic
        questions = Question.objects.filter(subtopic_id=pk)
        
        #Saving Quiz object    
        a_quiz.save()
        
        context = {
            'quizzes':quizzes,
            'questions':questions,           
        }
        
        
            
    return render(request,'quiz_app/quiz-marked.html',context)
    

    



