from django.shortcuts import render

from registration.forms import RegisterationForm, AddressForm
from registration import edx_services

from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError

# Create your views here.
def home(request):
    return render(request,'index.html')

def register1(request):
    # logger.info("Will register user now, add code to save user here....")
    if request.method == 'POST':
        # userform = (request.POST)
        userform = RegisterationForm()
        # logger.info("%s", userform)
        context = {}
        try:
            if not userform.is_valid():
                if userform.data['password'] != userform.data['confirm_password']:
                    userform.add_error('confirm_password', 'The confirm_password do not match with password.')
                # else:
                #     userform.add_error('Check Contain')
                #     # msg = {"code":2, "content":"Username already exists. Please choose another username2."}

                # context['form_errors'] = userform.errors
                context['form']= userform
                return render(request, 'registration/register.html', context)

            if userform.is_valid():
                model1 = User()
                model1.username = userform.cleaned_data['username']
                # model1.password = make_password(userform.cleaned_data['password'])
                model1.password = userform.cleaned_data['password'] #userform.cleaned_data['password']
                model1.email = userform.cleaned_data['email']
                model1.first_name = userform.cleaned_data['firstname']
                model1.last_name = userform.cleaned_data['lastname']
                model1.is_active = 1

                # print("is_active....",model1.is_active)
                try:
                    model1.set_password(model1.password)
                    model1.save()
                except IntegrityError as e:
                    # print ("Duplicate entry error contains: ", e)
                    # msg = {"code":2, "content":"Username already exists. Please choose another username1."}
                    # return render(request,"api_response.html", {'detailerror':msg})
                    userform.add_error('username', 'Username already exists. Please choose another username.')
                    context['form']= userform
                    return render(request, 'registration/register.html', context)
                iid=model1.id
                # logger.info("Value of id is ----------------------------------- %s",iid)
                # logger.info("user_role ********************************************** %s", userform.cleaned_data['user_role'])

                userroleobj=UserRoles.objects.get(id=userform.cleaned_data['user_role'])
                # logger.info("user_role ********************************************** %s", userroleobj.id)

                # model2 = UserProfile()
                #USER_TYPE_CHOICES = (
                #                      (1, 'admin'),
                #                      (2, 'coursecreator'),
                #                     )
                #user_type = model2.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
                #print ("Values in user_type",user_type)
                # model2.user_role = userroleobj
                # # logger.info("********************************************** %s", model2.user_role)
                #
                # model2.user_id = iid
                # try:
                #     model2.save()
                # except IntegrityError as e:
                #     # logger.error ("Duplicate entry error contains: %s", e)
                #     msg = {"code":2, "content":"Username already exists. Please choose another username1."}
                #     return render(request,"api_response.html", {'detailerror':msg})

                # logger.info("form is valid********")
                #new_user = userform.save()
                msg = {"code":1, "content":"Registration Successful."}
            # elif userform.data['password'] != userform.data['confirm_password']:
            #     userform.add_error('confirm_password', 'The passwords do not match')
            #     msg = {"code":2, "content":"The passwords do not match."}
            # else:
            #     print()
            #     msg = {"code":2, "content":"Username already exists. Please choose another username2."}
            return render(request,"registration/register.html", {'detailerror':msg})
        except Exception as e:
            pass
            # logger.error("Error : %s",e)

        # return render(request,
        #     'registerUser.html',
        #     {'user_form': userform,  'registered': registerUser} )
    else:
        userform = RegisterationForm()
        errormsg = {"code":3, "content":"Will register user now, add code to save user here....."}
        args = {}
        args.update(csrf(request))
        args['userform'] = RegisterationForm()
        # return render(request,"api_response.html", {'detailerror':errormsg}, args)
        return render(request,"registration/register.html", {'detailerror':errormsg}, args)

    return render(request, 'registration/register.html')


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
