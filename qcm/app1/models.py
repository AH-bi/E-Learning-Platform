from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Domain(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField()
    def __str__(self):
        return self.name



# category Model
class Category(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()
    def __str__(self):
        return self.name 

    class Meta:
        verbose_name_plural="Categories"


# Subcategory Model
class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural='Subcategories'

# Question Model
class Question(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE,null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True)
    question = models.TextField()
    answer_1 = models.CharField(max_length=255)
    answer_2 = models.CharField(max_length=255)
    answer_3 = models.CharField(max_length=255)
    answer_4 = models.CharField(max_length=255)
    explanation= models.TextField(blank=True,null=True)
    
    def __str__(self):
        return self.question
        

    # Retrive option from a specific Question Model  
    def get_options(self):
        return [(1, self.answer_1), (2, self.answer_2), (3, self.answer_3), (4, self.answer_4)]
    
    # Retrive correct answer 
    def get_correct_answer(self, question_id):
        correct_answer = CorrectAnswer.objects.get(question=question_id).answer
        if correct_answer == 1:
            return self.answer_1
        elif correct_answer == 2:
            return self.answer_2
        elif correct_answer == 3:
            return self.answer_3
        else:
            return self.answer_4
    

    
    """
 
    def get_answer_display(self):
        return getattr(self, 'answer_' + str(self.correctanswer_set.all().first().answer))

    def get_correct_answer(self, question_id):
        correct_answer = CorrectAnswer.objects.get(question=question_id)
        return correct_answer.get_answer_1_display()
    """


class CorrectAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.IntegerField()

    def __str__(self):
        return str(self.answer) +": "+self.question.get_options()[self.answer-1][1]



class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE,null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True)


class Feedback(models.Model):
    RATING_CHOICES = [
        (1, 'Very dissatisfied'),
        (2, 'Somewhat dissatisfied'),
        (3, 'Neither satisfied nor dissatisfied'),
        (4, 'Somewhat satisfied'),
        (5, 'Very satisfied'),
    ]
    rating = models.IntegerField(choices=RATING_CHOICES)
    reasons = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Feedback #{self.id}"