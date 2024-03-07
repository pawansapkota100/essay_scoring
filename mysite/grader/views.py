from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import *
from .forms import AnswerForm

from tensorflow.keras import backend as K
from .utils.helpers import *
from .utils.model import get_model
import os
import math
import numpy as np
from django.contrib.auth.decorators import login_required

current_path = os.path.abspath(os.path.dirname(__file__))

from django.shortcuts import render
from time import sleep
def index(request):
    try:
        if request.method == "POST":
            name = request.POST["name"]
            email = request.POST["email"]
            phone = request.POST["phone"]  
            message = request.POST["message"]
            sleep(10)
            data = Contact_info(name=name, email=email, phone=phone, message=message)
            # No need to check data.is_valid() since it's not a form, just save it directly
            data.save()
    except Exception as e:
        return render(request, 'grader/index.html', {'error': e})
    else:
        print("no data")
    return render(request, 'grader/index.html')

def view_answers(request, content_id):
    content = get_object_or_404(Form_Question, id=content_id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment-text')
        new_comment = Comment(user=request.user, text=comment_text)
        new_comment.save()
        # Add the newly created comment to the context
        content.Comment.add(new_comment)
        content.save()
    forum_question= Form_Question.objects.all()     
    context = {'content': content, 'forum_question': forum_question}
    return render(request, 'grader/view_answer.html', context)


@login_required(login_url='login')
def essay_prediction(request):
    questions_list = Question.objects.order_by('set')
    context = {
        'questions_list': questions_list,
        }
    return render(request, 'grader/essay_prediction.html', context)

@login_required(login_url='login')
def essay_writing_forum(request):
    essay_data = Form_Question.objects.all()
    context = {
        'essay_data': essay_data,
    }
    return render(request, 'grader/essay_writing_forum.html', context)

@login_required(login_url='login')
def ask_essay(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        expectation = request.POST.get('tried')


        # Validate form data
        if not title or not description:
            # If title or description is empty, render the form again with an error message
            error_message = "Please fill in both the title and description."
            return render(request, 'grader/essay_writing_forum.html', {'error_message': error_message})

        # Create a new Form_Question instance and save it to the database
        new_essay = Form_Question.objects.create(
            title=title,
            description=description,
            expectation=expectation,

            user=request.user if request.user.is_authenticated else None,
            time=timezone.now()
        )



        # Redirect to a success page or any other desired page
        return redirect("success/")  # Change 'success_page' to your desired URL name
    return render(request, 'grader/ask_essay.html')

def essay(request, question_id, essay_id):
    essay = get_object_or_404(Essay, pk=essay_id)
    context = {
        "essay": essay,
    }
    return render(request, 'grader/essay.html', context)
from gensim.models import KeyedVectors

def question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    essay = None  # Initialize essay to None

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data.get('answer')

            if len(content) > 20:
                num_features = 300
                model = KeyedVectors.load_word2vec_format(os.path.join(current_path, "deep_learning_files/word2vec.bin"), binary=True)
                clean_test_essays = []
                clean_test_essays.append(essay_to_wordlist(content, remove_stopwords=True))
                testDataVecs = getAvgFeatureVecs(clean_test_essays, model, num_features)
                testDataVecs = np.array(testDataVecs)
                testDataVecs = np.reshape(testDataVecs, (testDataVecs.shape[0], 1, testDataVecs.shape[1]))

                lstm_model = get_model()
                lstm_model.load_weights(os.path.join(current_path, "deep_learning_files/final_lstm.h5"))
                preds = lstm_model.predict(testDataVecs)

                if math.isnan(preds):
                    preds = 0
                else:
                    preds = np.around(preds)

                if preds < 0:
                    preds = 0
                if preds > question.max_score:
                    preds = question.max_score

                K.clear_session()  # Move this line here
                essay = Essay.objects.create(
                    content=content,
                    question=question,
                    score=preds
                )
                return redirect('essay', question_id=question.set, essay_id=essay.id)

    else:
        form = AnswerForm()

    context = {
        "question": question,
        "form": form,
    }
    return render(request, 'grader/question.html', context)

from django.contrib.auth import authenticate,login
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Server-side validation (example)
        if not username or not password:
            # Handle invalid form submission
            return render(request, 'grader/login.html', {'error': 'Please enter both email and password.'})

        user = authenticate(username=username, password=password)
        print('user',user)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'grader/fail.html', {'error': 'Invalid login credentials.'})

    return render(request, 'grader/login.html')




def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 == password2:
            # Check if the username or email already exists
            try:
                if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                    return render(request, 'register.html', {'error': 'Username or email already exists.'})
            except:
                pass
            
            else:
                # Create the user
                user = User.objects.create_user(username=username, email=email, password=password1)
                # Optionally, log in the user after registration
                user = authenticate(username=username, password=password1)
                login(request, user)
                # Redirect to a success page or home page
                return redirect('index')
        else:
            # Handle case when passwords don't match
           print('passwords dont match')
    else:
        pass
    
    return render(request, 'grader/register.html')



def fail(request):
    return render('grader/fail.html')
    
from django.contrib.auth import logout    
def logout_view(request):
    logout(request)
    return redirect('index')

@login_required(login_url='login')
def profile(request):
    return render(request, 'grader/profile.html')

def service(request):
    return render (request, 'grader/service.html')

def contact(request):
    return render(request, 'grader/contact.html')

def success(request):
    return render(request, 'grader/success.html')
def about(request):
    return render(request, 'grader/about.html')