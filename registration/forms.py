from django import forms
from django.contrib.auth.models import User
from django.urls import reverse


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset, ButtonHolder
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab
from crispy_forms.bootstrap import (
    PrependedText )
# from crispy_forms.bootstrap import ( PrependedText, PrependedAppendedText, FormActions)

from datetime import datetime, timedelta
from pytz import UTC

from registration import edx_services

this_year = datetime.now(UTC).year
VALID_YEARS = list(range(this_year, this_year - 120, -1))
YEARS = [(ele,ele ) for ele in VALID_YEARS]
YEARS=tuple(YEARS)

STATE = (
    ('', 'Choose...'),
    ('MG', 'Minas Gerais'),
    ('SP', 'Sao Paulo'),
    ('RJ', 'Rio de Janeiro')
)

class AddressForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput())
    address_1 = forms.CharField(
        label='Address',
        widget=forms.TextInput(attrs={'placeholder': '1234 Main St'})
    )
    address_2 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Apartment, studio, or floor'})
    )
    city = forms.CharField()
    state = forms.ChoiceField(choices=STATE)
    zip_code = forms.CharField(label='Zip')
    check_me_out = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('password', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'address_1',
            'address_2',
            Row(
                Column('city', css_class='form-group col-md-6 mb-0'),
                Column('state', css_class='form-group col-md-4 mb-0'),
                Column('zip_code', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            'check_me_out',
            Submit('submit', 'Sign in')
        )
COUNTRIES = (
        ('IN', 'India'),
        )

# For all Countries comment the above "COUNTRIES" tuple and Un-comment the below "COUNTRIES" tuple
# COUNTRIES = (
#         ('AL', 'Alabama'),
#         ('AK', 'Alaska'),
#         ('AZ', 'Arizona'),
#         ('AR', 'Arkansas'),
#         ('AA', 'Armed Forces Americas'),
#         ('AE', 'Armed Forces Europe'),
#         ('AP', 'Armed Forces Pacific'),
#         ('CA', 'California'),
#         ('CO', 'Colorado'),
#         ('CT', 'Connecticut'),
#         ('DE', 'Delaware'),
#         ('DC', 'District Of Columbia'),
#         ('FL', 'Florida'),
#         ('GA', 'Georgia'),
#         ('HI', 'Hawaii'),
#         ('ID', 'Idaho'),
#         ('IL', 'Illinois'),
#         ('IN', 'Indiana'),
#         ('IA', 'Iowa'),
#         ('KS', 'Kansas'),
#         ('KY', 'Kentucky'),
#         ('LA', 'Louisiana'),
#         ('ME', 'Maine'),
#         ('MD', 'Maryland'),
#         ('MA', 'Massachusetts'),
#         ('MI', 'Michigan'),
#         ('MN', 'Minnesota'),
#         ('MS', 'Mississippi'),
#         ('MO', 'Missouri'),
#         ('MT', 'Montana'),
#         ('NE', 'Nebraska'),
#         ('NV', 'Nevada'),
#         ('NH', 'New Hampshire'),
#         ('NJ', 'New Jersey'),
#         ('NM', 'New Mexico'),
#         ('NY', 'New York'),
#         ('NC', 'North Carolina'),
#         ('ND', 'North Dakota'),
#         ('OH', 'Ohio'),
#         ('OK', 'Oklahoma'),
#         ('OR', 'Oregon'),
#         ('PA', 'Pennsylvania'),
#         ('RI', 'Rhode Island'),
#         ('SC', 'South Carolina'),
#         ('SD', 'South Dakota'),
#         ('TN', 'Tennessee'),
#         ('TX', 'Texas'),
#         ('UT', 'Utah'),
#         ('VT', 'Vermont'),
#         ('VA', 'Virginia'),
#         ('WA', 'Washington'),
#         ('WV', 'West Virginia'),
#         ('WI', 'Wisconsin'),
#         ('WY', 'Wyoming'),
#     )

STATES = (
        ('', 'Choose...'),
        ('Andaman and Nicobar islands', 'Andaman and Nicobar islands'),
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Arunachal Pradesh', 'Arunachal Pradesh'),
        ('Assam', 'Assam'),
        ('Bihar', 'Bihar'),
        ('Chandigarh', 'Chandigarh'),
        ('Chattisgarh', 'Chattisgarh'),
        ('Dadra and Nagar Haveli', 'Dadra and Nagar Haveli'),
        ('Daman and Diu', 'Daman and Diu'),
        ('Delhi', 'Delhi'),
        ('Goa', 'Goa'),
        ('Gujarat', 'Gujarat'),
        ('Haryana', 'Haryana'),
        ('Himachal Pradesh', 'Himachal Pradesh'),
        ('Jammu and Kashmir', 'Jammu and Kashmir'),
        ('Jharkhand', 'Jharkhand'),
        ('Karnataka', 'Karnataka'),
        ('Kerala', 'Kerala'),
        ('Lakshadweep', 'Lakshadweep'),
        ('Madhya Pradesh', 'Madhya Pradesh'),
        ('Maharashtra', 'Maharashtra'),
        ('Manipur', 'Manipur'),
        ('Meghalaya', 'Meghalaya'),
        ('Mizoram', 'Mizoram'),
        ('Nagaland', 'Nagaland'),
        ('Orissa', 'Orissa'),
        ('Pondicherry', 'Pondicherry'),
        ('Punjab', 'Punjab'),
        ('Rajasthan', 'Rajasthan'),
        ('Sikkim', 'Sikkim'),
        ('Tamil Nadu', 'Tamil Nadu'),
        ('Telangana', 'Telangana'),
        ('Tripura', 'Tripura'),
        ('Uttar Pradesh', 'Uttar Pradesh'),
        ('Uttarakhand', 'Uttarakhand'),
        ('West Bengal', 'West Bengal'),
    )
GENDER_CHOICES = (
        ('', 'Choose...'),
        ('m', 'Male'),
        ('f', 'Female'),
        # Translators: 'Other' refers to the student's gender
        ('o', 'Other/Prefer Not to Say')
    )
LEVEL_OF_EDUCATION_CHOICES = (
        ('', "Choose..."),
        ('p', "Doctorate"),
        ('m', "Master's or professional degree"),
        ('b', "Bachelor's degree"),
        ('a', "Associate degree"),
        ('hs', "Secondary/high school"),
        ('jhs', "Junior secondary/junior high/middle school"),
        ('el', "Elementary/primary school"),
        # Translators: 'None' refers to the student's level of education
        ('none', "No formal education"),
        # Translators: 'Other' refers to the student's level of education
        ('other', "Other education")
    )

class RegisterationForm(forms.Form):
    email = forms.CharField(label='Email Id', required=True, max_length=254,  widget=forms.TextInput(attrs={'placeholder': 'Email'}))

    firstname = forms.CharField(label='First Name', required=False, max_length=30, widget=forms.TextInput(attrs={'placeholder': 'First Name'}) ) #autocomplete='off',
    lastname = forms.CharField(label='Last Name', required=False, max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}) ) #autocomplete='off',
    gender = forms.ChoiceField(label='Gender', required=False, choices=GENDER_CHOICES)
    year_of_birth = forms.ChoiceField(label='Year of Birth', required=False, choices=YEARS)
    aadharid = forms.CharField(label='Aadhar Id(UIDAI)', required=False, max_length=12, widget=forms.TextInput(attrs={'placeholder': 'Aadhar Id(UIDAI)'}) ) #autocomplete='off',
    username = forms.CharField(label='Public User Name', required=True, max_length=150,widget=forms.TextInput(attrs={'placeholder': 'Public User Name'}) ) #autocomplete='off',
    password = forms.CharField(label='Password', required=True, max_length=100, widget=forms.PasswordInput, initial='pan@1234')
    confirm_password = forms.CharField(label= "Confirm Password", required=True, max_length=100, widget=forms.PasswordInput, initial='pan@1234')
    country = forms.ChoiceField(label="Country", choices=COUNTRIES, required=True)
    state = forms.ChoiceField(label="States", choices=STATES, required=True)
    city = forms.CharField(label='City',required=True, max_length=150,widget=forms.TextInput(attrs={'placeholder': 'City'}))
    pincode = forms.CharField(label='Pin Code',required=True, max_length=6,widget=forms.TextInput(attrs={'placeholder': 'Pin Code'}))
    level_of_education = forms.ChoiceField(label='Highest level of education completed', required=False,choices=LEVEL_OF_EDUCATION_CHOICES)
    stra="Tell us why yo're interested in IITBombayX (optional)"
    goals = forms.CharField(label="Tell us why yo're interested in IITBombayX", required=False,widget=forms.Textarea(),initial=stra)

    class Meta:
        model = User
        fields = ("firstname", "lastname", "username", "email", "password", "is_active")
        # model = UserProfile
        # fields = ("year_of_birth", "gender", "level_of_education", "city", "country", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # super(RegisterationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-RegisterationForm'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('register')
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-success'))
        self.helper.form_class = 'form-horizontal'
        self.helper.field_template = 'registration/register.html'
        # self.helper.layout = Layout(
        #     Fieldset('Name',
        #         Field('username', placeholder='Username', css_class="some-class"),
        #         PrependedText('password', '@', placeholder="password", autocomplete='off'),),
        #    # Fieldset('Contact data', 'email', 'phone', style="color: brown;"),
        #    # InlineRadios('user_role'),
        #    # TabHolder(Tab('Address', 'address'),
        #    #           Tab('More Info', 'more_info'))
        #    )

    def clean(self):
        cleaned_data = super(RegisterationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        # print(password, confirm_password)

        # if password != confirm_password:
        #     self.add_error('confirm_password', "Password does not match")
        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

        return cleaned_data

    def clean_username(self):
        """
            Validate that the supplied Username is unique for the
            site.
        """
        username = self.cleaned_data['username']
        # print("clean_username",  self.cleaned_data['username'])
        if len(self.cleaned_data['username'])<4:
            raise forms.ValidationError('Username should have Minimum 4 Charecters.')
        return self.cleaned_data['username']

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("That user is already taken , please select another ")

        if User.objects.filter(username__iexact=self.cleaned_data['username']):
            raise forms.ValidationError('Username already exists. 123Please choose another username.')

        return username

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        # print("clean_email", self.cleaned_data['email'])
        f = forms.EmailField()
        try:
            f.clean(self.cleaned_data['email'])
        except ValidationError as e:
            raise forms.ValidationError("Enter valid email address.")

        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError("111This email address is already in use. Please enter a different email address.")

        return self.cleaned_data['email']

    def clean_password(self):
        """
            Validate that the supplied password length for the
            site.

        """
        if len(self.cleaned_data['password'])<8:
            raise forms.ValidationError('Password should have Minimum 8 Charecters.')
        return self.cleaned_data['password']

class EnrollForm(forms.Form):
    """docstring for ."""
    learner = forms.ChoiceField(label="Select Learner", required=True)
    course = forms.ChoiceField(label="Select Course", required=True)

    class Meta:
        model = User
        fields = ("username")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # resp = User.objects.all().order_by("username")  # it is OK
        # resp = User.objects.get(is_active=1).order_by("username")  # it is NOT OK
        resp = User.objects.filter(is_active=1).order_by("username")  # it is also OK

        # print("resp", resp)
        userList = []

        i=1
        userList.append([])
        userList[0].append('')
        userList[0].append("Choose...")
        for item in resp:  # self.roles:
            userList.append([])#Adding empty List for Each Platform
            userList[i].append(item.id)#Populating the list with id and platform_name
            userList[i].append(item.username)
            i = i+1

        self.fields['learner'] = forms.ChoiceField(choices=userList)

        # Openedx Courses
        edxCourses_obj= edx_services.EdxCourses()
        courses_response = edxCourses_obj.edxCourses("GET", None)
        # print("courses_response", courses_response)
        self.fields['course'] = forms.ChoiceField(choices=courses_response.Result)

    def clean(self):
        cleaned_data = super(EnrollForm, self).clean()
        return cleaned_data
