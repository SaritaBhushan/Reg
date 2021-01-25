from django.shortcuts import render
from django.db import transaction
from registration.forms import RegisterationForm, AddressForm, EnrollForm
from registration import edx_services
from registration.edx_services import AlreadyExistError, edXServicesError
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError

# Create your views here.
def home(request):
    return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        userform = RegisterationForm(request.POST)
        #logger.info(form)
        if userform.is_valid():
            model = User()
            model.username = userform.cleaned_data['username']
            # model1.password = make_password(userform.cleaned_data['password'])
            model.password = userform.cleaned_data['password'] #userform.cleaned_data['password']
            model.email = userform.cleaned_data['email']
            model.first_name = userform.cleaned_data['firstname']
            model.last_name = userform.cleaned_data['lastname']
            model.is_active = 1

            try:
                model.set_password(model.password)
                model.save()
            except IntegrityError as e:
                print('VIEW.PY: Username already exists. 222Please choose another username.')
                # CHK DONE
                userform.add_error('username', 'Username already exists. 222Please choose another username.')
                context = {}
                context['form']= userform
                return render(request, 'registration/register.html', context)
            # else:
            #     # userform.add_error('username', 'Username already exists. 222Please choose another username.')
            #     # context = {}
            #     # context['form']= userform
            #     # return render(request, 'registration/register.html', context)
            #     return self.form_invalid(userform)


            user_id=model.id
            print("user_id", user_id)

            user_data={}
            user_data["id"]=user_id;
            user_data["gender"] = userform.cleaned_data['gender']
            user_data["year_of_birth"] = userform.cleaned_data['year_of_birth']
            user_data["aadharid"] = userform.cleaned_data['aadharid']
            # user_data["username"] = userform.cleaned_data['username']
            user_data["username"] = userform.cleaned_data['username']
            # email = self.cleaned_data.get('email', None)
            user_data["country"] = userform.cleaned_data['country']
            user_data["state"] = userform.cleaned_data['state']
            user_data["city"] = userform.cleaned_data['city']
            user_data["pincode"] = userform.cleaned_data['pincode']
            user_data["level_of_education"] = userform.cleaned_data['level_of_education']
            user_data["goals"] = userform.cleaned_data['goals']
            print("user_data", user_data)

            # edx service
            # Create object of the class CourseGrades of the edx_mongo_services
            RegisterUserDetail_obj= edx_services.RegisterUserDetail()

            # # # Call the edx_mongo_services to get the grades of course
            # RegisterUserDetail_response = RegisterUserDetail_obj.RegisterUserDetail(request.method, user_data)
            RegisterUserDetail_response = RegisterUserDetail_obj.RegisterUserDetail(request.method, user_data)
            print("edx service return in view.py:", RegisterUserDetail_response.status_code, RegisterUserDetail_response.ErrMsg, RegisterUserDetail_response.Message)

            msg = {"code":1, "content":"Registration Successful."}
            # return render(request,"registration/confirm.html", {'detailerror':msg})
            messages.success(request, "Save sucessfully")
            return render(request, "registration/confirm.html")
            # return render(request,"registration/confirm.html")

            # new_user = userform.save()
            # return HttpResponseRedirect("registration/crispy_registration.html",)
    else:
        userform = RegisterationForm()

    return render(request, "registration/register.html", {'form': userform,})

@transaction.atomic
def enroll(request):
    if request.method == 'POST':
        print("POST ======================")
        # print("Method POST", request.method)
        enrollForm = EnrollForm(request.POST)
        if enrollForm.is_valid():
            learner = enrollForm.cleaned_data['learner']
            learner_name = enrollForm.cleaned_data.get('learner')
            course = enrollForm.cleaned_data['course']
            print("\n\n\t\t\t\t***** learner, course:",learner, course)
            # print("\n\n***** learner_name",learner_name, learner)
            # edx service

            try:
                enroll_obj = edx_services.EnrollUser()
                enroll_response = enroll_obj.enrollUser(learner,course)
                print("courses_response", enroll_response, enroll_response.status_code)
                if enroll_response.status_code != 201:
                    enrollForm = EnrollForm()
                    messages.success(request, "User is not Enroll for the course "+ course + ". Reasons: " + enroll_response.ErrMsg)
                    return render(request, "registration/course_Enroll.html", {'form': enrollForm,})
                print("======================")
            except AlreadyExistError as e:
                print("\t\t\t@@81 MySQL @edxe@: ",type(e),e)
                enrollForm.add_error('learner', e)
                context = {}
                context['form']= enrollForm
                return render(request, 'registration/course_Enroll.html', context)
            except edXServicesError as e:
                print("@@83 MySQL @edxe@: ",type(e),e)
                messages.success(request, e)
                return render(request, 'registration/course_Enroll.html', {'form': enrollForm,})
            # except Exception as e:
            #     print("@@82 MySQL @edxe@: ",type(e),e)
            #     messages.success(request, e)
            #     return render(request, "registration/course_Enroll.html", {'form': enrollForm,})

            enrollForm = EnrollForm()
            messages.success(request, learner_name +" Enroll for the course "+ course +" sucessfully")
            return render(request, "registration/course_Enroll.html", {'form': enrollForm,})
        # return render(request, "registration/confirm.html")
        # return render(request, "registration/course_Enroll.html")
    else:
        print("GET ======================")
        print("Method OTHER", request.method)
        enrollForm = EnrollForm()
        return render(request, "registration/course_Enroll.html", {'form': enrollForm,})

def crispy_register(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        #logger.info(form)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("registration/crispy_registration.html",)
    else:
        form = AddressForm()

    return render(request, "registration/crispy_registration.html", {'form': form,})
