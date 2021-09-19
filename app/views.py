from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from django.contrib.auth.hashers import check_password


# def landing_page(request):
#     return render(request, 'landing_page.html')

    
def index(request):
    return HttpResponseRedirect("user_dashboard")


def top_users():
    # get uniques users top 3 levels from completed
    users = User.objects.all()
    completed_level = Completed_Quiz.objects.filter().order_by('-level')
    top_users = []
    for u in users:
        for c_l in completed_level:
            if u.id == c_l.user.id:
                t_s = {
                    "name": u.name,
                    "level": c_l.level,
                    "cat": c_l.category.name,
                }
                top_users.append(t_s)
                break

    return  top_users


def try_signin(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:

            user = User.objects.get(email=email)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                context={
                    "user":user,
                    "top_users":top_users,
                }
                return HttpResponseRedirect("user_dashboard",context)
            else:
                context = {
                    "msg": "Wrong Email/Password"
                }
                return render(request, "signin.html", context)

        except:
            context = {
                "msg": "This Email Does Not Exist, Register your Email First"
            }
            return render(request,"signin.html",context)
    else:
       return render(request, "signin.html")
def try_signup(request):
    if request.method =="POST":
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            User.objects.get(email=email)
            context = {
                "msg": "This Email is already Registered! Enter another Email"
            }
            return render(request, "signup.html", context)
        except User.DoesNotExist:
            user = User(name=name, email=email, password=password)
            user.save()
            context={
                "msg":"congratulations! Account created Successfully"
            }
            return render(request,"signup.html",context)
    else:
       return render(request, "signup.html")
def signup(request):
    return render(request,"signup.html")

def signin(request):
    return render(request,"signin.html")

def user_dashboard(request):
    if 'user_id' in request.session:
            user = User.objects.get(id=request.session['user_id'])
            quiz_Category = Category.objects.all()

            if quiz_Category:
                context = {
                        "user": user,
                        'Categories':quiz_Category,
                        'top_users':top_users,
                    }
                return render(request, "user_dashboard.html", context)
            else:
                context = {
                    "user": user,
                    'top_users':top_users,
                    'msg': "No Quiz Added Yet !"

                }
                return render(request, "user_dashboard.html", context)
    else:
        context = {
            "msg": "Your Session Was expired! Please Login Again."
        }
        return HttpResponseRedirect("signin",context)
def logout(request):
        try:
            del request.session['user_id']
        except KeyError:
            pass
        return render(request,"signin.html")


def withdraw(request):
    if 'user_id' in request.session:
        try:
            user = User.objects.get(id=request.session['user_id'])
            if request.method == "POST":
                user.paypal_email = request.POST['paypal_email']
                user.save()
            if user.paypal_email == None:
                context = {
                    'user': user,
                    'top_users': top_users
                }
                return render(request, "withdraw_form.html",context)
            else:
                context = {
                    'user': user,
                    'top_users':top_users,
                    'payments':Payment.objects.filter(user=user),
                }
                return render(request, "withdraw.html",context)

        except User.DoesNotExist:
            return HttpResponseRedirect("user_dashboard")
    else:
        return HttpResponseRedirect("signin")


def change_img(request):
    from django.core.files.storage import FileSystemStorage
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session["user_id"])
        if request.method == "GET":
            context = {
                'user': user,
                'top_users':top_users,
            }
            return render(request,"change_img.html",context)
        elif request.method == "POST":
            image = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            uploaded_file_url = fs.url(filename)
            user.picture=uploaded_file_url
            user.save()
            context = {
                'user': user,
                'top_users':top_users,
                'preview_img':uploaded_file_url
            }
            return render(request, "change_img.html",context)


def change_password(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session["user_id"])
        if request.method == "GET":
            context = {
                "user": user,
                'top_users': top_users,
            }
            return render(request,"change_password.html",context)
        elif request.method == "POST":
            oldpassword = request.POST["oldpassword"]
            password = request.POST["password"]
            if check_password(oldpassword, user.password):
                user.password = password
                user.save()
                context={
                    "user":user,
                    'msg':"Password Changed Successfully",
                    'yes':1,
                    'top_users': top_users,
                }
                return render(request,"change_password.html",context)
            else:
                context = {
                    "user": user,
                    'top_users': top_users,
                    'msg': "Old password is wrong"
                }
                return render(request,"change_password.html",context)


def start_quiz(request):
    if 'user_id' in request.session:
         user = User.objects.get(id=request.session['user_id'])
         if request.method == "POST" and int(request.POST["post_id"])==0:
            quiz_category_id = request.POST["category_id"]
            category = Category.objects.get(id=quiz_category_id)

            # do it for if quiz is starting for first time...
            completed_levels = Completed_Quiz.objects.filter(user=user, category=category).order_by('-level').first()
            if completed_levels:
                if completed_levels.level == 10:
                    context = {
                        "user": user,
                        'top_users': top_users,
                        "msg": "You Already Won 10 Levels, chose another Type!",

                    }
                    return render(request, "msg.html", context)
                else:
                    request.session["category"] = category.id
                    request.session["level"] = int(completed_levels.level) +1
                    quiz=Quiz.objects.filter(category=category, level=int(completed_levels.level) + 1)

                    if not quiz:
                        context = {
                            "user": user,
                            'top_users': top_users,
                            "msg": "Next Level is not added Yet!",
                            "alert": "1"

                        }
                        return render(request, "msg.html", context)

                    context = {
                        "user": user,
                        'top_users': top_users,
                        "language_level":quiz
                    }
                    return render(request, "start_quiz.html", context)
            else:
                # This else run when quiz is not started yet...!
                # he is just starting his quiz for first time...
                request.session["category"]= category.id
                request.session["level"]= 1
                quiz= Quiz.objects.filter(category=category,level=1)
                if not quiz:
                    context = {
                        "user": user,
                        'top_users': top_users,
                        "msg": "Sorry! There is No Quiz Added for this Level!",
                        "alert": "1"

                    }
                    return render(request, "msg.html", context)

                context = {
                    "user": user,
                    'top_users': top_users,
                    "language_level":quiz
                }
                return render(request, "start_quiz.html", context)
         elif request.method == "POST" and int(request.POST["post_id"])==1:
                 quiz_id = request.POST["quiz_id"]
                 quiz = Quiz.objects.get(id=quiz_id)

                 questions = Question.objects.filter(quiz=quiz,asked=False).first()
                 if questions ==None:
                     context = {
                         "user": user,
                         'top_users': top_users,
                         "msg":"Sorry No Questions Found!",
                         "alert":"1"

                     }
                     return render(request, "msg.html", context)
                 request.session["attempt"]=2
                 request.session["ques_no"]=1
                 request.session["quiz_id"]=quiz_id

                 context = {
                     "user": user,
                     'top_users': top_users,
                     "questions":questions,

                 }
                 return render(request, "quiz.html",context)
         else:
                 request.session['user_id'] = user.id
                 context = {
                     "user": user,
                     'top_users': top_users,
                 }
                 return HttpResponseRedirect("user_dashboard", context)
    else:
        return HttpResponseRedirect("try_signin")



def check_ans(request,ques_id=0):
    # after timer goes to zero should be submitted as false
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        if request.method == "POST":
                 quesion = Question.objects.get(id=ques_id)
                # asked = True  for previous one
                 if quesion.ans_key == request.POST["option"] and quesion.asked == False:
                     request.session['check']=True
                     quesion.asked = True
                     quesion.save()
                     if request.session["ques_no"] == 10:
                         quiz_id = request.session["quiz_id"]
                         quiz = Quiz.objects.get(id=quiz_id)
                         user.balance=int(user.balance)+int(quiz.Win_Payment)
                         user.save()
                         categ= Category.objects.get(id=request.session["category"])
                         c_q= Completed_Quiz(user=user,category=categ,level=request.session["level"])
                         c_q.save()
                         context = {
                             "user": user,
                             'top_users': top_users,
                             "msg": "congratulations! You Won $"+str(quiz.Win_Payment),

                         }
                         return render(request, "msg.html", context)

                     request.session["ques_no"] = int(request.session["ques_no"]) + 1
                     quiz_id= request.session["quiz_id"]
                     quiz = Quiz.objects.get(id=quiz_id)
                     questions = Question.objects.filter(quiz=quiz, asked=False).first()
                     if questions==None:
                         context = {
                             "user": user,
                             'top_users': top_users,
                             "msg": "No More Questions! Try Letter",
                             "alert": "1"
                         }
                         return render(request, "msg.html", context)

                     context = {
                             "user": user,
                             'top_users': top_users,
                             "questions": questions,
                             "ans": quesion,
                             "ans_y": True,
                         }
                     return render(request, "quiz.html", context)


                 else:

                    if quesion.asked == False:
                     request.session['check']=False
                     quesion.asked = True
                     quesion.save()
                     request.session["attempt"] = int(request.session["attempt"])-1
                     if request.session["attempt"] <=0:
                         context = {
                             "user": user,
                             'top_users': top_users,
                             "msg": "You Loose Try Again!",
                             "alert":1

                         }
                         return render(request, "msg.html", context)
                     else:
                         request.session["ques_no"] = int(request.session["ques_no"]) + 1
                         quiz_id = request.session["quiz_id"]
                         quiz = Quiz.objects.get(id=quiz_id)
                         questions = Question.objects.filter(quiz=quiz, asked=False).first()
                         if questions ==None:
                             context = {
                                 "user": user,
                                 'top_users': top_users,
                                 "msg": "No More Questions! Try Letter",
                                 "alert": "1"
                             }
                             return render(request, "msg.html", context)
                         context = {
                                 "user": user,
                                 'top_users': top_users,
                                 "questions": questions,
                                 "ans": quesion,
                                 "ans_y": False,
                             }
                         return render(request, "quiz.html", context)

                    else:
                        quiz_id = request.session["quiz_id"]
                        quiz = Quiz.objects.get(id=quiz_id)
                        questions = Question.objects.filter(quiz=quiz, asked=False).first()
                        if questions == None:
                            context = {
                                "user": user,
                                'top_users': top_users,
                                "msg": "No More Questions! Try Letter",
                                "alert": "1"
                            }
                            return render(request, "msg.html", context)
                        context = {
                                "user": user,
                                'top_users': top_users,
                                "questions": questions,
                                "ans": quesion,
                                "ans_y": request.session['check'],

                            }
                        return render(request, "quiz.html", context)

        else:
                 return HttpResponseRedirect("/user_dashboard")
    else:
        return HttpResponseRedirect("try_signin")



def completed_levels(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        c_q= Completed_Quiz.objects.filter(user=user)
        if c_q is not None:
            completed=[]
            for c in c_q:
                category = Category.objects.get(id=c.category.id)
                level = c.level
                complete = {
                    'cat':category,
                    'level':level
                }
                completed.append(complete)


        context = {
            "completed_levels":completed,
            "user": user,
            'top_users':top_users,
        }
        return render(request,"completed_levels.html", context)
    else:
        return HttpResponseRedirect("try_signin")



def withdraw_payment(request):
    if 'user_id' in request.session:
            user = User.objects.get(id=request.session['user_id'])
            if request.method == "POST":

                if user.balance != 0:
                    status=Status.objects.get(status="Pending")
                    payment = Payment(user=user,payment=user.balance,payment_status=status)
                    payment.save()
                    user.balance=0
                    user.save()
                    context = {
                        'user': user,
                        'top_users':top_users,
                        'payments':Payment.objects.filter(user=user),
                        'msg':"Your payment will in your Paypal as soon as!"
                    }
                    return render(request, "withdraw.html",context)

            context = {
                        'user': user,
                        'top_users': top_users,
                        'payments': Payment.objects.filter(user=user),
                    }
            return render(request, "withdraw.html", context)

    else:
        return HttpResponseRedirect("signin")


