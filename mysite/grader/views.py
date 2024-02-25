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
from gensim.models import word2vec
# from .models import ForumEssay
current_path = os.path.abspath(os.path.dirname(__file__))

from django.shortcuts import render

def index(request):
    return render(request, 'grader/index.html')

def about(request):
    return render(request, 'grader/about.html')

def view_answers(request, content_id):
    content = get_object_or_404(Form_Question, id=content_id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment-text')
        new_comment = Comment(user=request.user, text=comment_text)
        new_comment.save()
        # Add the newly created comment to the context
        content.Comment.add(new_comment)
        content.save()
    context = {'content': content}
    return render(request, 'grader/view_answer.html', context)



def essay_prediction(request):
    questions_list = Question.objects.order_by('set')
    context = {
        'questions_list': questions_list,
        }
    return render(request, 'grader/essay_prediction.html', context)

def essay_writing_forum(request):
    essay_data = Form_Question.objects.all()
    context = {
        'essay_data': essay_data,
    }
    return render(request, 'grader/essay_writing_forum.html', context)


def ask_essay(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        expectation = request.POST.get('tried')
        tags_input = request.POST.get('tags')

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

        # Process tags
        if tags_input:
            tags = [tag.strip() for tag in tags_input.split(',')]
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                new_essay.tags.add(tag)

        # Redirect to a success page or any other desired page
        return redirect('grader/ask_essay.html')  # Change 'success_page' to your desired URL name
    return render(request, 'grader/ask_essay.html')

# Create your views here.
# def index(request):
#     questions_list = Question.objects.order_by('set')
#     context = {
#         'questions_list': questions_list,
    # }
    # return render(request, 'grader/index.html', context)

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
