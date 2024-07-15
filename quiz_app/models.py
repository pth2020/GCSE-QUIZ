import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Topic(models.Model):
    topic_id = models.BigAutoField(primary_key=True)
    
    topic = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.topic)
    
class Sub_Topic(models.Model):
    
    sub_topic_id = models.BigAutoField(primary_key=True)
    
    sub_topic = models.CharField(max_length=100)
        
    topic = models.ForeignKey(Topic , on_delete = models.CASCADE)
    
    def __str__(self):
        return str(self.sub_topic)
    
    
class Student(AbstractUser):
    
    student_id = models.BigAutoField(primary_key=True)
    
    email  = models.EmailField(max_length=100)
    
    username = models.CharField(max_length=100, unique=True)  
    
    password = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.username)    
    
class Question(models.Model):
    
    question_id = models.BigAutoField(primary_key=True)
    
    question = models.CharField(max_length=200)
    
    option1 = models.CharField(max_length=20)
    
    option2 = models.CharField(max_length=20)
    
    option3 = models.CharField(max_length=20)
    
    option4 = models.CharField(max_length=20)
    
    answer = models.CharField(max_length = 20)    
    
    subtopic = models.ForeignKey(Sub_Topic, on_delete=models.CASCADE, null=True)
    
            
    def __str__(self):
        
        return "{} {} {} {}\n".format(self.subtopic_id, ":", self.question,":", self.answer)
    
    

class Quiz(models.Model):
    student = models.CharField(max_length=100)
    quiz_date = models.DateTimeField(default=datetime.datetime.now, blank=True)
    subtopic = models.ForeignKey(Sub_Topic, on_delete=models.CASCADE, null=True)    
    mark = models.IntegerField()  
    total_number_of_questions = models.IntegerField()  
    result_percentage = models.DecimalField(max_digits=10, decimal_places=1, null=True) 
    real_answers_list = []
    user_answer_list = []  
    correct_user_answer_list = []   
        
    #method to compute score/mark of a quiz
    def get_result(self):
        #compares user-answer-list with real-answer-list and stores the same elements (correct answers) in another list
        self.correct_user_answer_list = [value for value in self.real_answers_list if value in self.user_answer_list] 
        #number of correct answers (score)
        self.marks = len(self.correct_user_answer_list)
        #convert score to percentage
        self.result_percentage = ((len(self.correct_user_answer_list))/(len(self.real_answers_list)))*100
        #clearing all lists for next comparision
        self.correct_user_answer_list.clear()
        self.real_answers_list.clear()
        self.real_answers_list.clear()      
        
        return self.marks
        
    
        
        
        
        
        
    


