# import sys
# import requests
# import json
import yaml
import mysql.connector
from pymongo import MongoClient

# from rest_framework import status
from rest_framework.response import Response
# from django.http import Http404

class Response:
    def __init__(self):
        self.status_code = 0
        self.ErrMsg = ""
        self.Message = ""

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
        except:
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
        except:
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
        except:
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
