# import sys
# import requests
# import json
import yaml
import mysql.connector
from pymongo import MongoClient
import hashlib
from six import text_type
# from rest_framework import status
from rest_framework.response import Response
# from django.http import Http404
import logging
from datetime import datetime


log = logging.getLogger(__name__)

class AlreadyExistError(Exception):
    """Exception indicating that task is already done"""
    message = 'Requested task is already exist'

    def __init__(self, message=None):
        if not message:
            message = self.message
        super(AlreadyExistError, self).__init__(message)

class edXServicesError(Exception):
    """Exception indicating that task is already done"""
    message = 'Requested task is already exist'

    def __init__(self, message=None):
        if not message:
            message = self.message
        super(edXServicesError, self).__init__(message)

class Response:
    def __init__(self):
        self.status_code = 0
        self.ErrMsg = ""
        self.Message = ""
        self.Result = ""

class RegisterUserDetail:
    def __init__(self):
        self.edxresponse = Response()

    def RegisterUserDetail(self, method, user_data):
        """
        Function: RegisterUserDetail
        Output: Response
        Description: The function perform CRUD operation on user registration detail to the Open EdX.
        """
        if method == "POST":
            print("in post")
            self.edxresponse = self.post_RegisterUserDetail(user_data)
        else:
            self.edxresponse.status_code = 405
            self.edxresponse.ErrMsg = "Method Not Allowed. " + str(e)
            return self.edxresponse

        # self.edxresponse.status_code = 201
        print("@edxe@ *** Return edx service: RegisterUserDetail: ", self.edxresponse.status_code, self.edxresponse.ErrMsg, self.edxresponse.Message)
        return self.edxresponse

    def post_RegisterUserDetail(self, user_data):
        """
        Function: post_RegisterUserDetail
        Output: Response
        Description: The function post user registration detail to Open EdX.
        """

        # post user MySQL Data
        self.edxresponse = self.post_userMySQLData(user_data)
        print("@edxe@ *** Return from post_userMySQLData: ", self.edxresponse.status_code, self.edxresponse.ErrMsg, self.edxresponse.Message)


        if self.edxresponse.status_code != 201:
            return self.edxresponse

        # # post user mongodb Data
        self.edxresponse = self.post_userMongoData(user_data)
        # print("@edxe@ *** Return from post_userMongoData: ", self.edxresponse.status_code, self.edxresponse.ErrMsg, self.edxresponse.Message)

        if self.edxresponse.status_code != 201:
            return self.edxresponse

        return self.edxresponse

    def post_userMySQLData(self, user_data):
        """
        Function: post_userMySQLData
        Output: Response
        Description: The function post user registration detail to Open EdX MySQL database.
        """

        # post user Profile Data
        self.edxresponse = self.post_mysqlUserProfileData( user_data)
        print("@edxe@ *** Return from post_mysqlUserProfileData: ", self.edxresponse.status_code, self.edxresponse.ErrMsg, self.edxresponse.Message)

        if self.edxresponse.status_code != 201:
            return self.edxresponse

        self.edxresponse = self.post_mysqlUserCustomData( user_data)
        print("@edxe@ *** Return from post_mysqlUserCustomData: ", self.edxresponse.status_code, self.edxresponse.ErrMsg, self.edxresponse.Message)

        if self.edxresponse.status_code != 201:
            return self.edxresponse

        print("@edxe@ *** Return from post_userProfileData: ", self.edxresponse.status_code, self.edxresponse.ErrMsg, self.edxresponse.Message)
        return self.edxresponse

    def mysql_connection(self, database_name):
        """
        Function: mysql_connection
        Output: MySQL connection
        Description: The function connect to the Open EdX MySQL Server.
        """
        # Read config.yml File
        try:
            config_dict = self.read_yml('config.yml')
            if type(config_dict)== Response:
                return config_dict
        except FileNotFoundError as e:
            print("55@edxe@: ",type(e),e)
            self.edxresponse.status_code = 500
            self.edxresponse.ErrMsg = "Please check config.yml file not found."
            return self.edxresponse
        except Exception as e:
            print("56@edxe@: ",type(e),e)
            self.edxresponse.status_code = 500
            self.edxresponse.ErrMsg = "Unable to read file config.yml."
            return self.edxresponse

        # Read config.yml File varibles
        try:
            mysql_server = config_dict['mysql_server']
            mysql_pwd = config_dict['mysql_pwd']
            mysql_user = config_dict['mysql_user']
            mysql_port = config_dict['mysql_port']
        except KeyError as e:
            print("62@edxe@: ",type(e),e)
            self.edxresponse.status_code = 500
            self.edxresponse.ErrMsg = "Please check some config varibles are not set in config.yml."
            return self.edxresponse
        except Exception as e:
            print("63@edxe@: ",type(e),e)
            self.edxresponse.status_code = 500
            self.edxresponse.ErrMsg = "Please check the config varibles in config.yml."
            return self.edxresponse

        #establishing the connection
        try:
            conn = mysql.connector.connect(user=mysql_user, password=mysql_pwd, host=mysql_server, database=database_name)
        except Exception as e:
            print("@MySQL cONNCSTION@: ",type(e),e)
            self.edxresponse.status_code = 500
            self.edxresponse.ErrMsg = "Please check connection."
            return self.edxresponse

        return conn

    def post_mysqlUserProfileData(self, user_data):
        """
        Function: post_mysqlUserProfileData
        Output: Response
        Description: The function post user profile detail to Open EdX MySQL database.
        """
        # Connect to the edxapp MySQL database.
        con = self.mysql_connection('edxapp')
        print("con", con)

        #Creating a cursor object using the cursor() method
        cursor = con.cursor()

        # Preparing SQL query to INSERT a record into the database.
        sql = ("INSERT INTO auth_userprofile(name, year_of_birth, gender, level_of_education, city, country, goals, user_id) VALUES (%s, %s, %s, %s, %s, %s,%s, %s) ")
        data = (
            user_data["username"],
            user_data["year_of_birth"],
            user_data["gender"],
            user_data["level_of_education"],
            user_data["city"],
            user_data["country"],
            user_data["goals"],
            user_data["id"]
            )
        print("sql", sql)

        try:
           # Executing the SQL command
           cursor.execute(sql, data)

           # Commit your changes in the database
           con.commit()
        except Exception as e:
           # Rolling back in case of error
           print("@81 MySQL Rolling back auth_userprofile @edxe@: ",type(e),e)
           con.rollback()
           self.edxresponse.status_code = 404
           self.edxresponse.ErrMsg = "Undefine Error while inserting data in the auth_userprofile table. " + str(e)
           return self.edxresponse

        print("auth_userprofile Data inserted")
        # Closing the connection
        con.close()

        self.edxresponse.status_code = 201
        return self.edxresponse

    def post_mysqlUserCustomData(self, user_data):
        """
        Function: post_mysqlUserCustomData
        Output: Response
        Description: The function post user detail to Open EdX MySQL custom_reg_form_extrainfo table.
        """
        # Connect to the edxapp MySQL database.
        con = self.mysql_connection('edxapp')
        print("con", con)

        cursor = con.cursor()

        sql = ("INSERT INTO custom_reg_form_extrainfo(state, city, pincode, aadharid, user_id ) VALUES (%s, %s, %s,%s, %s) ")
        data = (
            user_data["state"],
            user_data["city"],
            user_data["pincode"],
            user_data["aadharid"],
            user_data["id"]
            )
        print("sql", sql)
        try:
           # Executing the SQL command
           cursor.execute(sql, data)
           # Commit your changes in the database
           con.commit()
        except Exception as e:
           # Rolling back in case of error
           print("@82 MySQL Rolling back custom_reg_form_extrainfo @edxe@: ",type(e),e)
           con.rollback()
           self.edxresponse.status_code = 404
           self.edxresponse.ErrMsg = "Undefine Error while inserting data in the custom_reg_form_extrainfo table. " + str(e)
           return self.edxresponse

        print("custom_reg_form_extrainfo Data inserted")
        # Closing the connection
        con.close()

        self.edxresponse.status_code = 201
        return self.edxresponse

    def post_userMongoData(self, user_data):
        """
        Function: post_userMongoData
        Output: Response
        Description: The function post user registration detail to Open EdX Mongo database.
        """
        # post user Data
        self.edxresponse = self.post_mongoUserData( user_data)
        print("@edxe@ *** Return from post_mongoUserData: ", self.edxresponse.status_code, self.edxresponse.ErrMsg, self.edxresponse.Message)
        return self.edxresponse

    def mongo_connection(self, database_name):
        """
        Function: mongo_connection
        Output: Mongodb connection
        Description: The function connect to the Open EdX Mongodb Server.
        """
        # Read config.yml File
        try:
            config_dict = self.read_yml('config.yml')
            if type(config_dict)== Response:
                return config_dict
        except FileNotFoundError as e:
            print("55@edxe@: ",type(e),e)
            self.edxresponse.status_code = 500
            self.edxresponse.ErrMsg = "Please check config.yml file not found."
            return self.edxresponse
        except Exception as e:
            print("55@edxe@: ",type(e),e)
            self.edxresponse.status_code = 500
            self.edxresponse.ErrMsg = "Unable to read file config.yml."
            return self.edxresponse

        # Read config.yml File varibles
        try:
            mongo_server = config_dict['mongo_server']
            mongo_pwd = config_dict['mongo_pwd']
            mongo_user = config_dict['mongo_user']
            mongo_port = config_dict['mongo_port']
            mongo_authSource =config_dict['mongo_authSource']
        except KeyError as e:
            print("62@edxe@: ",type(e),e)
            self.edxresponse.status_code = 500
            self.edxresponse.ErrMsg = "Please check some config varibles are not set in config.yml."
            return self.edxresponse
        except Exception as e:
            print("63@edxe@: ",type(e),e)
            self.edxresponse.status_code = 500
            self.edxresponse.ErrMsg = "Please check the config varibles in config.yml."
            return self.edxresponse

        try:
            # Creating a pymongo client
            # client = MongoClient('mongodb://'+ mongo_user+ ':'+mongo_pwd+'@'+mongo_server+':'+mongo_port+'/edxapp',authSource=mongo_authSource)
            client = MongoClient('mongodb://' + mongo_user + ':' + mongo_pwd + '@' + mongo_server + ':' + mongo_port + '/' + database_name, authSource = mongo_authSource)

        except Exception as e:
            print("@mongo cONNCSTION@: ",type(e),e)
            self.edxresponse.status_code = 500
            self.edxresponse.ErrMsg = "Please check connection."
            return self.edxresponse

        return client

    def post_mongoUserData(self, user_data):
        """
        Function: post_mongoUserData
        Output: Response
        Description: The function post user profile detail to Open EdX mongo database.
        """
        # Connect to the edxapp mongo database.
        database_name='cs_comments_service'
        client = self.mongo_connection(database_name)
        print("client", client)

        #Getting the database instance
        db = client[database_name]

        # a collection
        coll = db['users']

        #documents to be inserted into collection
        # doc1 = { "_id" : "19", "default_sort_key" : "date", "external_id" : "19", "username" : "edx2" }
        doc = {
            "_id" : user_data["id"],
            "default_sort_key" : "date",
            "external_id" : user_data["id"],
            "username" : user_data["username"]
        }


        #Inserting document into a collection
        try:
           # Executing the Mongodb command
            coll.insert_one(doc)
            print(coll.find_one())
        except Exception as e:
           print("@Executing the Mongodb command@: ",type(e),e)
           self.edxresponse.status_code = 404
           self.edxresponse.ErrMsg = "Undefine Error. " + str(e)
           return self.edxresponse

        print("Mongo Data inserted")
        # Closing the connection

        self.edxresponse.status_code = 201
        return self.edxresponse

    def read_yml(self, filename):
        """
        Function: read_yml
        Parameters: filename - filename is name of yml config file.
                               No validation done on filename
        Output: python object or error message
        Description: The function open the .yml config file in read mode.
              The function yaml.load converts a YAML document to a Python
              object and return python object or error message as received
                     from the server.
        """
        # edxresponse = Response()
        print("filename", filename)
        with open(filename, 'r') as stream:
            try:
                return (yaml.load(stream))
            except yaml.YAMLError as exc:
                print("37@edxe@: ",type(exc),exc)
                self.edxresponse.status_code = 500
                self.edxresponse.ErrMsg = "Syntax error in config.yml."
                return self.edxresponse

class dbConnection:
    def __init__(self):
        self.edxresponse = Response()

    def read_yml(self, filename):
        """
        Function: read_yml
        Parameters: filename - filename is name of yml config file.
                               No validation done on filename
        Output: python object or error message
        Description: The function open the .yml config file in read mode.
              The function yaml.load converts a YAML document to a Python
              object and return python object or error message as received
                     from the server.
        """
        # edxresponse = Response()
        print("filename", filename)
        with open(filename, 'r') as stream:
            try:
                return (yaml.load(stream))
            except yaml.YAMLError as exc:
                print("37@edxe@: ",type(exc),exc)
                self.edxresponse.status_code = 500
                self.edxresponse.ErrMsg = "Syntax error in config.yml."
                return self.edxresponse

    def mysql_connection(self, database_name):
        """
        Function: mysql_connection
        Output: MySQL connection
        Description: The function connect to the Open EdX MySQL Server.
        """
        # Read config.yml File values
        try:
            config_dict = _read_yml_values()
        except Exception as e:
            print("56@edxe@: ",type(e),e)
            self.edxresponse.status_code = 500
            self.edxresponse.ErrMsg = "Unable to read file config.yml."
            return self.edxresponse

        # Read config.yml File varibles
        try:
            mysql_server = config_dict['mysql_server']
            mysql_pwd = config_dict['mysql_pwd']
            mysql_user = config_dict['mysql_user']
            mysql_port = config_dict['mysql_port']
        except KeyError as e:
            print("62@edxe@: ",type(e),e)
            self.edxresponse.status_code = 500
            self.edxresponse.ErrMsg = "Please check some config varibles are not set in config.yml."
            return self.edxresponse
        except Exception as e:
            print("63@edxe@: ",type(e),e)
            self.edxresponse.status_code = 500
            self.edxresponse.ErrMsg = "Please check the config varibles in config.yml."
            return self.edxresponse

        #establishing the connection
        try:
            conn = mysql.connector.connect(user=mysql_user, password=mysql_pwd, host=mysql_server, database=database_name)
        except Exception as e:
            print("@MySQL cONNCSTION@: ",type(e),e)
            self.edxresponse.status_code = 500
            self.edxresponse.ErrMsg = "Please check connection."
            return self.edxresponse

        return conn

    def mongo_connection(self, database_name):
        """
        Function: mongo_connection
        Output: Mongodb connection
        Description: The function connect to the Open EdX Mongodb Server.
        """
        # Read config.yml File values
        try:
            config_dict = _read_yml_values()
        except Exception as e:
            print("56@edxe@: ",type(e),e)
            self.edxresponse.status_code = 500
            self.edxresponse.ErrMsg = "Unable to read file config.yml."
            return self.edxresponse

        # Read config.yml File varibles
        try:
            mongo_server = config_dict['mongo_server']
            mongo_pwd = config_dict['mongo_pwd']
            mongo_user = config_dict['mongo_user']
            mongo_port = config_dict['mongo_port']
            mongo_authSource =config_dict['mongo_authSource']
        except KeyError as e:
            print("62@edxe@: ",type(e),e)
            self.edxresponse.status_code = 500
            self.edxresponse.ErrMsg = "Please check some config varibles are not set in config.yml."
            return self.edxresponse
        except Exception as e:
            print("63@edxe@: ",type(e),e)
            self.edxresponse.status_code = 500
            self.edxresponse.ErrMsg = "Please check the config varibles in config.yml."
            return self.edxresponse

        try:
            # Creating a pymongo client
            # client = MongoClient('mongodb://'+ mongo_user+ ':'+mongo_pwd+'@'+mongo_server+':'+mongo_port+'/edxapp',authSource=mongo_authSource)
            client = MongoClient('mongodb://' + mongo_user + ':' + mongo_pwd + '@' + mongo_server + ':' + mongo_port + '/' + database_name, authSource = mongo_authSource)

        except Exception as e:
            print("@mongo cONNCSTION@: ",type(e),e)
            self.edxresponse.status_code = 500
            self.edxresponse.ErrMsg = "Please check connection."
            return self.edxresponse

        return client

class EdxCourses:
    def __init__(self):
        self.edxresponse = Response()

    def edxCourses(self, method, course_id = None):
        """
        Function: EdxCourses
        Output: Response
        Description: The function perform CRUD operation on course(s) of the Open EdX.
        """
        if method == "GET":
            print("in GET")
            if course_id == None:
                self.get_Courses()
                print("@edxe@ *** Return edx service: get_Courses: ", self.edxresponse.status_code, self.edxresponse.Result, self.edxresponse.Message)
            else:
                pass
        else:
            self.edxresponse.status_code = 405
            self.edxresponse.ErrMsg = "Method Not Allowed. " + str(e)
            return self.edxresponse

        self.edxresponse.status_code = 200
        print("@edxe@ *** Return edx service: edxCourses: ", self.edxresponse.status_code, self.edxresponse.ErrMsg, self.edxresponse.Message)
        return self.edxresponse

    def get_Courses(self):
        """
        Function: get_Courses
        Output: Response
        Description: The function get list of Open EdX Courses from MySQL database.
        """
        # Connect to the edxapp MySQL database.
        db_obj= dbConnection()
        con = db_obj.mysql_connection('edxapp')
        print("con", con)

        #Creating a cursor object using the cursor() method
        cursor = con.cursor() #by default buffered=False then cursor.rowcount=-1 otherwise it is exact

        # Preparing SQL query to SELECT recordS from the database.
        # SELECT courseS those enrollment is started and end enrollment date define
        sql = ("SELECT `id`, CONCAT(`display_name`,' - ', `id`) as course FROM `course_overviews_courseoverview` WHERE date(enrollment_start) <= CURDATE() AND date(enrollment_end)>= CURDATE() order by `display_name`, `id`")
        # SELECT courseS those enrollment is started and end enrollment date not-define
                # sql = ("SELECT `id`, CONCAT(`display_name`,' - ', `id`) as course FROM `course_overviews_courseoverview` WHERE date(enrollment_start) <= CURDATE() AND ( date(enrollment_end) >= CURDATE() OR enrollment_end IS NULL) order by `display_name`, `id`")
        print("sql", sql)

        try:
           # Executing the SQL command
           cursor.execute(sql)

           # print("\n\n#@#@#  cursor.rowcount buffered=True: ", cursor.rowcount)

           #Fetching all rows from the table
           result = cursor.fetchall();
        except Exception as e:
           # Rolling back in case of error
           print("@81 MySQL @edxe@: ",type(e),e)
           self.edxresponse.status_code = 404
           self.edxresponse.ErrMsg = "Undefine Error while Getting Courses data. " + str(e)
           self.edxresponse
           return None

        print("get Data course")
        # Closing the connection
        con.close()

        self.edxresponse.status_code = 200
        self.edxresponse.Result=result

class EnrollUser:
    # def __init__(self, user_id=None, course_id=None):
    #     # self.edxresponse = Response()
    #     self.user_id = user_id
    #     self.course_id = course_id
    def __init__(self):
        super(EnrollUser, self).__init__()

    def enrollUser(self, user_id, course_id):
        """
        Function: enrollUser
        Output: Response
        Description: The function enroll user to the course on the Open EdX Platform.
        """
        edxresponse = Response()
        if self._is_userEnrolled(user_id, course_id):
            print("\t\t\t error_message:" "The User is already enrolled for the course " + course_id)
            # log.warning("Duplicate task found for task_type %s and task_key %s", task_type, task_key)
            error_message = "The User is already enrolled for the course " + course_id
            raise AlreadyExistError(error_message)

        # try:
        #     self.userEnrollment(user_id, course_id)
        # except Exception as e:
        #     error_message ="Unknown error: "+str(e)
        #     raise edXServicesError(error_message)
        #
        # edxresponse.status_code = 201
        # edxresponse.Message="User Enroll Sucessfully in the course " +course_id
        return self.userEnrollment(user_id, course_id)

    def userEnrollment(self, user_id, course_id):
        """
        Function: userEnrollment
        Output: Response
        Description: The function enroll user to the course on the Open EdX Platform.
        """
        edxresponse = Response()

        # Connect to the edxapp MySQL database.
        db_obj= dbConnection()
        con = db_obj.mysql_connection('edxapp')
        print("con", con)

        try:
            # Get "Student" role id of course
            role_id = self._get_role_id(con, course_id)
            print("@@ role_id:",role_id)

            addroleuser_response=self._addroleuser(con, role_id, user_id)
            if addroleuser_response.status_code != 201:
                raise edXServicesError(addroleuser_response.ErrMsg)

            if not self._is_anonymoususerid :
                addanonymoususerid_response=self._addanonymoususerid(con, user_id)
                if addanonymoususerid_response.status_code != 201:
                    raise edXServicesError(addroleuser_response.ErrMsg)

            enrollment_response = self._enrollment(con, user_id, course_id)
            if enrollment_response.status_code != 201:
                raise edXServicesError(enrollment_response.ErrMsg)

            con.commit()

        except edXServicesError as e:
            print("@811 MySQL Rolling back  @edxe@: ",type(e),e)
            con.rollback()
            edxresponse.status_code = 404
            edxresponse.ErrMsg = "Define Error in the user enrollment. " + str(e)
            return edxresponse
        except Exception as e:
           # Rolling back in case of error
           print("@81 MySQL Rolling back  @edxe@: ",type(e),e)
           con.rollback()
           edxresponse.status_code = 404
           edxresponse.ErrMsg = "Undefine Error in the user enrollment. " + str(e)
           return edxresponse

        con.close()
        edxresponse.status_code = 201
        edxresponse.Message="User Enroll Sucessfully in the course " +course_id
        return edxresponse

    def _is_anonymoususerid(self, user_id):
        """
        Function: _is_anonymoususerid
        Output: boolean
        Description: return anonymous_user_id exist for user_id or not.
        """
        # Connect to the edxapp MySQL database.
        db_obj= dbConnection()
        con = db_obj.mysql_connection('edxapp')
        print("con", con)

        #Creating a cursor object using the cursor() method
        cursor = con.cursor(buffered=True)

        # Preparing SQL query to SELECT a record from the database.
        sql = ("select anonymous_user_id from anonymous_user_id WHERE course_id='' AND user_id = " + user_id)
        # sql = ("SELECT `id`, CONCAT(`display_name`,' - ', `id`) as course FROM `course_overviews_courseoverview` WHERE date(enrollment_start) <= CURDATE() AND ( date(enrollment_end) >= CURDATE() OR enrollment_end IS NULL) order by `display_name`, `id`")
        print("sql", sql)

        try:
           # Executing the SQL command
           cursor.execute(sql)
        except Exception as e:
           # Rolling back in case of error
           print("@81 MySQL @edxe@: ",type(e),e)
           # edxresponse.status_code = 404
           # edxresponse.ErrMsg = "Undefine Error while Getting Courses data. " + str(e)
           raise edXServicesError("Undefine Error while Getting Courses data.")
           # return edxresponse

        if cursor.rowcount == 1:
            return True

        return  False

    def _addanonymoususerid(self, con, user_id):
        """
        Function: _addanonymoususerid
        Output: Response
        Description: Insert a row in the "student_anonymoususerid" MySQL table of edxapp database.
        """
        edxresponse = Response()

        anonymous_user_id=_get_anonymous_user_id(user_id)
        sql = ("INSERT INTO student_anonymoususerid(anonymous_user_id, user_id) VALUES  (%s, %s) ")
        data = (
            anonymous_user_id,
            user_id
            )
        print("sql", sql)

        try:
           # Executing the SQL command
           cursor.execute(sql, data)

           # Commit your changes in the database
        except Exception as e:
           # Rolling back in case of error
           print("@81 MySQL Rolling back django_comment_client_role_users @edxe@: ",type(e),e)
           edxresponse.status_code = 404
           edxresponse.ErrMsg = "Undefine Error while inserting data in the django_comment_client_role_users table. " + str(e)
           return edxresponse

        print("django_comment_client_role_users Data inserted")
        # Closing the connection

        edxresponse.status_code = 201
        return edxresponse

    def _get_anonymous_user_id(self, user_id):
        """
        Function: get_anonymous_user_id
        Output: anonymous_user_id
        Description: return anonymous_user_id.
        """
        user_obj = User.objects.get(id=user_id)
        assert user_obj

        # NOT WORKING
        # cached_id = getattr(user_obj, '_anonymous_id', {}).get(course_id)
        # if cached_id is not None:
        #     return cached_id

        # include the secret key as a salt, and to make the ids unique across different LMS installs.
        hasher = hashlib.md5()
        SECRET_KEY=read_EDXAPP_SECRET_KEY()
        hasher.update(SECRET_KEY.encode('utf-8'))
        hasher.update(text_type(user_obj.id).encode('utf-8'))

        # NOT WORKING
        # if course_id:
        #     hasher.update(text_type(course_id).encode('utf-8'))

        digest = hasher.hexdigest()
        return digest

    def _enrollment(self, con, user_id, course_id):
        """
        Function: _enrollment
        Output: Response
        Description: Insert a row in the "student_courseenrollment" MySQL table of edxapp database.
        """
        edxresponse = Response()

        #Creating a cursor object using the cursor() method
        cursor = con.cursor()

        now = datetime.now()
        create_date = now.strftime('%Y-%m-%d %H:%M:%S')

        # Preparing SQL query to INSERT a record into the database.
        # INSERT INTO student_courseenrollment(course_id, is_active, mode, user_id) VALUES (<course_id>, 1, "audit", <user_id>)

        # Correct
        sql = ("INSERT INTO student_courseenrollment(course_id, created, is_active, mode, user_id) VALUES  (%s, %s, %s, %s, %s) ")
        # # To TEST @transaction.atomic
        # sql = ("INSERT INTO student_courseenrollment(course_id, created, is_active, mode, user_id) VALUES  (%s, %s, %s, %s) ")

        data = (
            course_id,
            create_date,
            1,
            "audit",
            user_id
            )

        print("sql", sql)

        try:
           # Executing the SQL command
           cursor.execute(sql, data)
        except Exception as e:
           # Rolling back in case of error
           print("@81 MySQL Rolling back student_courseenrollment @edxe@: ",type(e),e)
           edxresponse.status_code = 404
           edxresponse.ErrMsg = "Undefine Error while inserting data in the student_courseenrollment table. " + str(e)
           return edxresponse

        print("student_courseenrollment Data inserted")

        edxresponse.status_code = 201
        return edxresponse

    def _addroleuser(self, con, role_id, user_id):
        """
        Function: -addroleusers
        Output: Response
        Description: Insert a row in the "django_comment_client_role_users" MySQL table of edxapp database.
        """
        edxresponse = Response()

        #Creating a cursor object using the cursor() method
        cursor = con.cursor()

        # Preparing SQL query to INSERT a record into the database.
        # INSERT INTO django_comment_client_role_users(role_id, user_id) VALUES (, );
        sql = ("INSERT INTO django_comment_client_role_users(role_id, user_id) VALUES  (%s, %s) ")
        data = (
            role_id,
            user_id
            )
        print("sql", sql)

        try:
           # Executing the SQL command
           cursor.execute(sql, data)
        except Exception as e:
           # Rolling back in case of error
           print("@81 MySQL Rolling back django_comment_client_role_users @edxe@: ",type(e),e)
           edxresponse.status_code = 404
           edxresponse.ErrMsg = "Undefine Error while inserting data in the django_comment_client_role_users table. " + str(e)
           return edxresponse

        print("django_comment_client_role_users Data inserted")
        # Closing the connection

        edxresponse.status_code = 201
        return edxresponse

    def _get_role_id(self, con, course_id):
        """
        Function: _get_role_id
        Output: role_id
        Description: find "student" role_id for the course from "django_comment_client_role" MySQL table of edxapp database.
        """
        edxresponse = Response()

        #Creating a cursor object using the cursor() method
        cursor = con.cursor(buffered=True)

        # Preparing SQL query to SELECT a record from the database.
        sql = ("SELECT id FROM `edxapp`.`django_comment_client_role` where  course_id='" + course_id + "' and name='Student'")
        # sql = ("SELECT `id`, CONCAT(`display_name`,' - ', `id`) as course FROM `course_overviews_courseoverview` WHERE date(enrollment_start) <= CURDATE() AND ( date(enrollment_end) >= CURDATE() OR enrollment_end IS NULL) order by `display_name`, `id`")
        print("sql", sql)

        try:
           # Executing the SQL command
           cursor.execute(sql)
        except Exception as e:
           # Rolling back in case of error
           print("@81 MySQL @edxe@: ",type(e),e)
           edxresponse.status_code = 404
           edxresponse.ErrMsg = "Undefine Error while Getting Courses data. " + str(e)
           # return edxresponse

        if cursor.rowcount !=1:
            if cursor.rowcount ==0:
                # Role not define
                error_message = "Student role not define."
                raise edXServicesError(error_message)

            else:
                # More than one role id define
                error_message = "More than one role define for a 'Student'."
                raise edXServicesError(error_message)
                # edxresponse.status_code = 404
                # edxresponse.ErrMsg = "More than one role define for a 'Student'. " + str(e)
        else:
            result = cursor.fetchone();
            print("\t\t\t @@@@@@ _get_role_id result",result, type(result))
            return result[0]

    def _is_userEnrolled(self, user_id, course_id):
        """
        Function: _is_userEnrolled
        Output: boolean value
        Description: The function check is user enroll to the course on the Open EdX Platform.
        """
        # Connect to the edxapp MySQL database.
        db_obj= dbConnection()
        con = db_obj.mysql_connection('edxapp')
        print("con", con)

        #Creating a cursor object using the cursor() method
        cursor = con.cursor(buffered=True)

        # Preparing SQL query to SELECT a record from the database.
        sql = ("select is_active from student_courseenrollment WHERE is_active=1 AND user_id = " + user_id + " AND course_id = '"+ course_id +"'")
        # sql = ("SELECT `id`, CONCAT(`display_name`,' - ', `id`) as course FROM `course_overviews_courseoverview` WHERE date(enrollment_start) <= CURDATE() AND ( date(enrollment_end) >= CURDATE() OR enrollment_end IS NULL) order by `display_name`, `id`")
        print("sql", sql)

        try:
           # Executing the SQL command
           cursor.execute(sql)
        except Exception as e:
           # Rolling back in case of error
           print("@81 MySQL @edxe@: ",type(e),e)
           # edxresponse.status_code = 404
           # edxresponse.ErrMsg = "Undefine Error while Getting Courses data. " + str(e)
           raise edXServicesError("Undefine Error while Getting Courses data.")
           # return edxresponse

        print("cursor.rowcount:", cursor.rowcount)
        if cursor.rowcount >0:
            print("\t\t\t\t @@@@@@The User is already enrolled for the course " + course_id)
            return True

        return  False

def _read_EDXAPP_SECRET_KEY():
    # edxresponse = Response()
    # Read config.yml File
    try:
        config_dict = _read_yml_values()
        EDXAPP_EDXAPP_SECRET_KEY=config_dict["EDXAPP_EDXAPP_SECRET_KEY"]
    except KeyError as e:
        print("62@edxe@: ",type(e),e)
        # edxresponse.status_code = 500
        # edxresponse.ErrMsg = "Please check some config varibles are not set in config.yml."
        error_message ="KeyError error in reading config.yml: "+str(e)
        raise edXServicesError(error_message)
    except Exception as e:
        print("55@edxe@: ",type(e),e)
        error_message ="Unknown error: "+str(e)
        raise edXServicesError(error_message)

    return EDXAPP_EDXAPP_SECRET_KEY

def _read_yml(filename):
    """
    Function: read_yml
    Parameters: filename - filename is name of yml config file.
                           No validation done on filename
    Output: python object or error message
    Description: The function open the .yml config file in read mode.
          The function yaml.load converts a YAML document to a Python
          object and return python object or error message as received
                 from the server.
    """
    edxresponse = Response()
    print("filename", filename)
    with open(filename, 'r') as stream:
        try:
            return (yaml.load(stream))
        except yaml.YAMLError as exc:
            print("37@edxe@: ",type(exc),exc)
            edxresponse.status_code = 500
            edxresponse.ErrMsg = "Syntax error in config.yml."
            return edxresponse

def _read_yml_values():
    edxresponse = Response()
    # Read config.yml File
    try:
        config_dict = _read_yml('config.yml')
        if type(config_dict)== Response:
            return config_dict
    except FileNotFoundError as e:
        print("55@edxe@: ",type(e),e)
        edxresponse.status_code = 500
        edxresponse.ErrMsg = "Please check config.yml file not found."
        return edxresponse
    except Exception as e:
        print("56@edxe@: ",type(e),e)
        edxresponse.status_code = 500
        edxresponse.ErrMsg = "Unable to read file config.yml."
        return edxresponse

    # Read config.yml File varibles
    config_values={}
    try:
        config_values["EDXAPP_EDXAPP_SECRET_KEY"] = config_dict['EDXAPP_EDXAPP_SECRET_KEY']
        config_values["mysql_server"] = config_dict['mysql_server']
        config_values["mysql_pwd"] = config_dict['mysql_pwd']
        config_values["mysql_user"] = config_dict['mysql_user']
        config_values["mysql_port"] = config_dict['mysql_port']
        config_values["mongo_server"] = config_dict['mongo_server']
        config_values["mongo_pwd"] = config_dict['mongo_pwd']
        config_values["mongo_user"] = config_dict['mongo_user']
        config_values["mongo_port"] = config_dict['mongo_port']
        config_values["mongo_authSource"] = config_dict['mongo_authSource']
    except KeyError as e:
        print("62@edxe@: ",type(e),e)
        edxresponse.status_code = 500
        edxresponse.ErrMsg = "Please check some config varibles are not set in config.yml."
        return edxresponse
    except Exception as e:
        print("63@edxe@: ",type(e),e)
        edxresponse.status_code = 500
        edxresponse.ErrMsg = "Please check the config varibles in config.yml."
        return edxresponse

    return config_values
