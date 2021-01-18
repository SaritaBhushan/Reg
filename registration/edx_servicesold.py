# import sys
# import requests
# import json
# import yaml
import mysql.connector
# from rest_framework import status
from rest_framework.response import Response
# from django.http import Http404
#
# import logging
#
#
# logger = logging.getLogger(__name__)
#
# logging.config.dictConfig({
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'console': {
#             'format': '%(name)-12s %(levelname)-8s %(message)s'
#         },
#         'file': {
#             'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
#         }
#     },
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'console'
#         },
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'formatter': 'file',
#             'filename': '/tmp/debug.log'
#         }
#     },
#     'loggers': {
#         '': {
#             'level': 'DEBUG',
#             'handlers': ['console', 'file']
#         }
#     }
# })
#
#
# class urlError(Exception):
#     """Exception indicating that url address or port is not valid"""
#     pass

class Response:
    def __init__(self):
        self.status_code = 0
        self.ErrMsg = ""
        self.Message = ""

class RegisterUserDetail:
    def __init__(self):
        pass
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
        edxresponse = Response()
        with open(filename, 'r') as stream:
            try:
                return (yaml.load(stream))
            except yaml.YAMLError as exc:
                print("37@edxe@: ",type(exc),exc)
                edxresponse.status_code = 500
                edxresponse.ErrMsg = "Syntax error in config.yml."
                return edxresponse

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
            edxresponse.status_code = 500
            edxresponse.ErrMsg = "Please check config.yml file not found."
            return edxresponse
        except Exception as e:
            print("55@edxe@: ",type(e),e)
            edxresponse.status_code = 500
            edxresponse.ErrMsg = "Unable to read file config.yml."
            return edxresponse

        # Read config.yml File varibles
        try:
            mysql_server = config_dict['mysql_server']
            mysql_pwd = config_dict['mysql_pwd']
            mysql_user = config_dict['mysql_user']
            mysql_port = config_dict['mysql_port']
        except KeyError as e:
            print("62@edxe@: ",type(e),e)
            edxresponse.status_code = 500
            edxresponse.ErrMsg = "Please check some config varibles are not set in config.yml."
            return edxresponse
        except Exception as e:
            print("68@edxe@: ",type(e),e)
            edxresponse.status_code = 500
            edxresponse.ErrMsg = "Please check the config varibles in config.yml."
            return edxresponse

            try:
                conn = mysql.connector.connect(user=mysql_user, password=mysql_pwd, host=mysql_server, database=database_name)
            except Exception as e:
                print("@MySQL cONNCSTION@: ",type(e),e)
                edxresponse.status_code = 500
                edxresponse.ErrMsg = "Please check conn."
                return edxresponse

        return conn

    def post_mysqlUserCustomData(self, con, user_data):
        pass

    def post_mysqlUserProfileData(self, con, user_data):
        """
        Function: post_mysqlUserProfileData
        Output: Response
        Description: The function post user profile detail to Open EdX MySQL database.
        """
        edxMysqlresponse = Response()

        cursor = con.cursor()

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

        try:
           # Executing the SQL command
           cursor.execute(sql, data)
           # Commit your changes in the database
           con.commit()
        except:
           # Rolling back in case of error
           con.rollback()
           edxMysqlresponse.status_code = 404
           edxMysqlresponse.ErrMsg = "Undefine Error. " + str(e)
           return edxMysqlresponse

        print("Data inserted")
        # Closing the connection
        con.close()

        edxMysqlresponse.status_code = 201
        return edxMysqlresponse

    def post_userMySQLData(self, user_data):
        """
        Function: post_userMySQLData
        Output: Response
        Description: The function post user registration detail to Open EdX MySQL database.
        """
        # Connect to the edxapp MySQL database.
        con = self.mysql_connection('edxapp')

        # post user Profile Data
        response = self.post_mysqlUserProfileData(self, con, user_ID, user_data)
        print("@edxe@ *** Return from post_mysqlUserProfileData: ", response)

        # response = self.post_mysqlUserCustomData(self, con, user_ID, user_data)
        # print("@edxe@ *** Return from post_mysqlUserCustomData: ", response)


        print("@edxe@ *** Return from post_userProfileData: ", response)
        return response

    # def mongo_connection(self, database_name):
    #     """
    #     Function: mysql_connection
    #     Output: MySQL connection
    #     Description: The function connect to the Open EdX MySQL Server.
    #     """
    #     # Read config.yml File
    #     try:
    #         config_dict = self.read_yml('config.yml')
    #         if type(config_dict)== Response:
    #             return config_dict
    #     except FileNotFoundError as e:
    #         print("55@edxe@: ",type(e),e)
    #         edxresponse.status_code = 500
    #         edxresponse.ErrMsg = "Please check config.yml file not found."
    #         return edxresponse
    #     except Exception as e:
    #         print("55@edxe@: ",type(e),e)
    #         edxresponse.status_code = 500
    #         edxresponse.ErrMsg = "Unable to read file config.yml."
    #         return edxresponse
    #
    #     # Read config.yml File varibles
    #     try:
    #         mongo_server = config_dict['mongo_server']
    #         mongo_pwd = config_dict['mongo_pwd']
    #         mongo_user = config_dict['mongo_user']
    #         mongo_port = config_dict['mongo_port']
    #         mongo_authSource = config_dict['mongo_authSource']
    #     except KeyError as e:
    #         print("62@edxe@: ",type(e),e)
    #         edxresponse.status_code = 500
    #         edxresponse.ErrMsg = "Please check some config varibles are not set in config.yml."
    #         return edxresponse
    #     except Exception as e:
    #         print("68@edxe@: ",type(e),e)
    #         edxresponse.status_code = 500
    #         edxresponse.ErrMsg = "Please check the config varibles in config.yml."
    #         return edxresponse
    #
    #     conn = "" #mysql.connector.connect(user=mysql_user, password=mysql_pwd, host=mysql_server, database=database_name)
    #     return conn
    #
    # def post_mongoUserData(self, user_data):
    #     pass
    # def post_userMongoData(self, user_data):
    #     pass
    #
    def post_RegisterUserDetail(self, user_data):
        """
        Function: post_RegisterUserDetail
        Output: Response
        Description: The function post user registration detail to Open EdX.
        """

        # post user MySQL Data
        edxresponse = self.post_userMySQLData(user_data)
        print("@edxe@ *** Return from post_userMySQLData: ", response)

        # # post user mongodb Data
        # response = self.post_userMongoData(user_data)
        # print("@edxe@ *** Return from post_userMongoData: ", response)
        return edxresponse

    def RegisterUserDetail(self, method, user_data):
        """
        Function: RegisterUserDetail
        Output: Response
        Description: The function perform CRUD operation on user registration detail to the Open EdX.
        """
        # try:

        if method == "POST":
            print("in post")
            # edxresponse = self.post_RegisterUserDetail(user_data)
        else:
            edxresponse.status_code = 405
            edxresponse.ErrMsg = "Method Not Allowed. " + str(e)
            return edxresponse

        edxresponse.status_code = 201
        return edxresponse



# def main(argv):
#     lms_server_details = "http://10.129.103.92/"
#     cms_server_details = "http://10.129.103.92:18010/"
#     login_url = lms_server_details + "login"
#     url = cms_server_details + "course/course-v1:edX+DemoX+Demo_Course?format = json"
#     #response = call_url(url, "GET", login_url, True)
#     post_url = cms_server_details + "course/"
#     course_data = {
#         "org": "MOOC",
#         "run": "19-20",
#         "display_name": "Mooc course through code 11",
#         "number": "M111"}
#     data = json.dumps(course_data)
#     response = call_url(post_url, "POST", True, data)

# if __name__ == "__main__":
#     main(sys.argv[1:])

# # end main
