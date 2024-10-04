from django.shortcuts import render,redirect
from django.views import View
from .models import Question,Subcategory,CorrectAnswer,Score,Domain,Category,Feedback
from django.http import HttpResponse
import random
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages

# Create your views here.


class ShowQuestion(LoginRequiredMixin,View):
    def get(self, request, sub_id=None, category_id=None, domain_id=None):
            if (request.user.is_authenticated):
                if (request.session.get('number_of_questions') is None):
                    request.session['number_of_questions']=0
                ctx={}               
                round = request.session.get('round')
                timer=request.session.get('timer')
                difficulty = request.session.get('difficulty')
                if round is None:
                    round = 1
                if timer is None:
                    timer=10
                if difficulty is None:
                    difficulty = 'Easy'
                if difficulty == 'Easy':
                    number_of_questions = 6
                elif difficulty == 'Medium':
                    number_of_questions = 8
                elif difficulty == 'Hard':
                    number_of_questions = 10
                else:
                    number_of_questions = 5
                request.session['number_of_questions']=number_of_questions*int(request.session.get('total_round',1))
                print(request.session['number_of_questions']) 
                selected_category = {}
                if sub_id:
                    subcategory = Subcategory.objects.get(id=sub_id)
                    scd=subcategory
                    questions = list(Question.objects.filter(subcategory=subcategory))
                    selected_category['type'] = 'subcategory'
                    selected_category['name'] = subcategory.name
                    selected_category['id'] = subcategory.id
                elif category_id:
                    category = Category.objects.get(id=category_id)
                    scd=category
                    questions = list(Question.objects.filter(category=category))
                    selected_category['type'] = 'category'
                    selected_category['name'] = category.name
                    selected_category['id'] = category.id
                elif domain_id:
                    domain = Domain.objects.get(id=domain_id)
                    scd=domain
                    questions = list(Question.objects.filter(domain=domain))
                    selected_category['type'] = 'domain'
                    selected_category['name'] = domain.name
                    selected_category['id'] = domain.id
                else:
                    # Handle the case when no id is provided
                    #  return a 404 error or redirect to a default page
                    pass
                request.session['selected_category']=selected_category            
                    
                
                random.shuffle(questions) # there is a possibility for the question to repeat i need to track the questions with their id's
                questions = questions[:number_of_questions]
                ctx = {
                    'scd':scd,
                    'questions': questions,
                    'round': round,
                    'timer':timer,
                }
                return render(request, 'questions.html', ctx)
            else:
                return redirect("login")




    def post(self, request, sub_id=None, category_id=None, domain_id=None):
            # for the review answers qustion 
            if (request.session.get('que') is None):
                request.session['que']={}
            difficulty = request.session.get('difficulty')
            for key in request.POST.keys() :
                    print(key)

            if difficulty is None:
                difficulty="Easy"
            question_ids = [key for key in request.POST.keys() if key.isdigit()]
            questions = Question.objects.filter(id__in=question_ids)  
            correctanswer = CorrectAnswer.objects.all()
            score_user = request.session.get('score_user', 0)
            score_computer = request.session.get('score_computer', 0)
            round = request.session.get('round', 1)
            answers = {}
            user_answer=0
            for question in questions:
                user_answer = request.POST.get(f'{question.id}')
                request.session.get('que')[question.id]=user_answer
                answers[question.id] = user_answer
                if request.POST.get(f'{question.id}') == str(correctanswer.get(question=question).answer):
                    score_user += 1


                computer_score = random.randint(0,100)
                if difficulty == 'Easy':
                    if computer_score >= 50:
                        score_computer += 1
                elif difficulty == 'Medium':
                    if computer_score >= 30:
                        score_computer += 1
                elif difficulty == 'Hard':
                    if computer_score >= 1:
                        score_computer += 1


 
            request.session['score_user'] = score_user
            request.session['score_computer'] = score_computer
            round +=1
            request.session['round'] = round
            if round <= int(request.session.get('total_round',1)):
                if(sub_id):
                    return redirect('show_questions_by_subcategory', sub_id)
                elif(category_id):
                    return redirect('show_questions_by_category', category_id)
                else:
                    return redirect('show_questions_by_domain', domain_id)


            else:
                return redirect('result')




class ShowResult(LoginRequiredMixin,View):
    
    def get(self,request):


        if request.user.is_authenticated:

            score_user = request.session.get('score_user',0)         
            score_computer=request.session.get('score_computer',0)
            number_of_questions=request.session.get('number_of_questions')
         
            
            winning_message = "It's a draw" if score_user == score_computer else "You won" if score_user > score_computer  else "You lost"
            context={
                'score_user':score_user,
                'score_computer':score_computer,
                'number_of_questions':number_of_questions,
                'winning_message': winning_message,
            }

            context['score_user_percent']=(score_user/number_of_questions)*100
            context['score_computer_percent']=(score_computer/number_of_questions)*100

            return render(request, 'result.html', context)




        else:
            return redirect("login")



class ReviewAnswers(View):
    def get(self, request):      

        if request.user.is_authenticated:  
            users_answers=request.session.get('que')
            correct_answers = []
            incorrect_answers = []

            for question_id, answer in users_answers.items():
                question = Question.objects.get(id=int(question_id))
                question.correct_answer = question.get_correct_answer(question.id)
                question.answer = int(answer)
                print(type(question.answer))
                print(question.correct_answer)
                if question.answer == CorrectAnswer.objects.get(question_id=question.id).answer:
                    correct_answers.append(question)
                else:
                    incorrect_answers.append(question)
         
            return render(request, 'review.html', {'correct_answers': correct_answers, 'incorrect_answers': incorrect_answers})
        else:
            return redirect('login')



class ScoreView(LoginRequiredMixin, View):
    def post(self, request):
        score = int(request.POST.get('score_user', 0))
        selected_category = request.session.get('selected_category')
        if (selected_category):
                print('here')
                print(type(selected_category['id']))
                # probleme to knwo how to get the function to score base on the  domain or the category or sub same as the  first get 
                if selected_category['type']=='domain':
                    domain = Domain.objects.get(id=selected_category['id'])
                    Score.objects.create(user=request.user,score=score,domain=domain )
                elif selected_category['type']=='category':
                    category = Category.objects.get(id=selected_category['id'])
                    Score.objects.create(user=request.user,score=score,category=category )
                else:
                    subcategory = Subcategory.objects.get(id=selected_category['id'])
                    Score.objects.create(user=request.user,score=score,subcategory=subcategory)
                
                messages.success(request, 'Your score is Saved!')
                return redirect('/home')

    def get(self, request):
        scores = Score.objects.all().order_by('-score')
      
        """  domains = Domain.objects.all()
        categories = Category.objects.all()
        subcategories = Subcategory.objects.all()
        """
        domain_id = request.GET.get('domain')
        category_id = request.GET.get('category')
        subcategory_id = request.GET.get('subcategory')

        if domain_id:
            scores = scores.filter(domain__id=domain_id)
            categories = categories.filter(domain__id=domain_id)
            subcategories = subcategories.filter(category__id__in=[c.id for c in categories])
        elif category_id:
            scores = scores.filter(category__id=category_id)
            subcategories = subcategories.filter(category__id=category_id)
        elif subcategory_id:
            scores = scores.filter(subcategory__id=subcategory_id)

        context = {
            'scores': scores,
            
        }
        return render(request, 'leaderboard.html', context)


"""'domains': domains,
            'categories': categories,
            'subcategories': subcategories,
        """"""
"""



class FB(LoginRequiredMixin,View):

    def post(self, request):
        print("test")
        rating = request.POST.get('feedback')
        user=request.user
        reasons = request.POST.get('reasons')
        feedback = Feedback(rating=rating, reasons=reasons,user=user)
        feedback.save()
        messages.success(request, 'Your feedback has been submitted successfully. Thank you for your input!')
        return redirect('result')





""" back up get function:
   
    def get(self, request, sub_id):
        # Retrieve the round value from the session
        round = request.session.get('round')
        timer=request.session.get('timer')
        difficulty = request.session.get('difficulty')
        if round is None:
            round = 1
        if timer is None:
            timer=10
        if difficulty is None:
            difficulty = 'Easy'

        # Determine the number of questions to display based on the difficulty level
        if difficulty == 'Easy':
            number_of_questions = 3
        elif difficulty == 'Medium':
            number_of_questions = 8
        elif difficulty == 'Hard':
            number_of_questions = 10
        else:
            number_of_questions = 5
        

        # Filter the question base on the sub_id
        subcategory = Subcategory.objects.get(id=sub_id)
        questions = Question.objects.filter(subcategory=subcategory)[:number_of_questions]
        # the same questions will be displayed in every round.


        ctx = {
            'subcategory': subcategory,
            'questions': questions,
            'round': round,
            'timer':timer,
        }
        return render(request, 'questions.html', ctx)

// back up for post 
    def post(self, request, sub_id):
            difficulty = request.session.get('difficulty')
            questions = Question.objects.filter(subcategory_id=sub_id)
            correctanswer = CorrectAnswer.objects.all()
            score_user = request.session.get('score_user', 0)
            score_computer = request.session.get('score_computer', 0)
            round = request.session.get('round', 1)
            for question in questions:
                if request.POST.get(f'qid{question.id}') == str(correctanswer.get(question=question).answer):
                    score_user += 1
                computer_score = random.randint(0,100)
                if difficulty == 'Easy':
                    if computer_score >= 50:
                        score_computer += 1
                elif difficulty == 'Medium':
                    if computer_score >= 30:
                        score_computer += 1
                elif difficulty == 'Hard':
                    if computer_score >= 1:
                        score_computer += 1
            
            request.session['score_user'] = score_user
            request.session['score_computer'] = score_computer

            context = {
                'score_user': score_user,
                'score_computer': score_computer,
            }
            round +=1
            request.session['round'] = round

            if round <= int(request.session.get('total_round')):
                    print("test")
                    return redirect('subcategory_questions', sub_id)
            else:
                winning_message = "It's a draw" if score_user == score_computer else "You won" if score_user > score_computer  else "You lost"
                context['winning_message'] = winning_message
                #del request.session['your key']
                # request.session.clear() This will remove all data stored in the session, so be sure to only add it when the final round is reached.
                del request.session['score_user']
                del request.session['score_computer']
                del request.session['round']
                return render(request, 'result.html', context)

"""