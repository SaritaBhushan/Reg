# import sys
import requests
import json
import yaml
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404

import logging


logger = logging.getLogger(__name__)

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': '/tmp/debug.log'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
})


class urlError(Exception):
    """Exception indicating that url address or port is not valid"""
    pass

class Response:
    def __init__(self):
        self.status_code = 0
        self.ErrMsg = ""
        self.Message = ""

class RegisterUserDetail:
    # def __init__(self):
    #     edxresponse = Response()

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

    def post_user(self, user_data):
        """
        Function: post_course
        Output: Response
        Description: The function post course to Open EdX.
        """
        # try:
        edxresponse = Response()
        #print("\n@edxe@** post_course in service:")
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

        try:
            lms_server_ip = config_dict['openedx_lms_server_ip']
            cms_server_ip = config_dict['openedx_cms_server_ip']
            lms_port = config_dict['openedx_lms_port']
            cms_port = config_dict['openedx_cms_port']

            lms_server_details = "http://" + lms_server_ip + ":" + lms_port + "/"
            cms_server_details = "http://" + cms_server_ip + ":" + cms_port + "/"
            login_dict = {
                "url": lms_server_details, #+ "login",
                "email": config_dict['login_email'],
                "password": config_dict['login_password']
                }
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

        post_dict = {
            "url": cms_server_details + "course/",
            "lms_server_ip": lms_server_ip,
            "cms_server_ip": cms_server_ip,
            "lms_port": lms_port,
            "cms_port": cms_port,
            }

        # post_url = cms_server_details + "course/"
        #print("\n@edxe@*@*")
        course_data = self.map_coursedata(course_data)
        #print("\n@edxe@*@@*")
        # data = json.dumps(course_data)
        response = self.call_url(post_dict, "POST", login_dict, True, course_data)
        print("@edxe@ *** Return from call url: ", response)
        return response
        # except Exception as e:
        #     print("Exception in edx_services:", e.message)
        #     return e

    def enroll_student(self, course_data):
        """
        Function: enroll_student
        Output: Response
        Description: Enroll the student, who is enrolled on Swayam, to a course on Open EdX.
        """
        print("\n@edxe@** enroll in service:")
        edxresponse = Response()
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
        try:
            lms_server_ip = course_data['platform']
            lms_port = config_dict['openedx_lms_port']

            lms_server_details = "http://" + lms_server_ip + ":" + lms_port + "/"


            logger.info("Enrollment server is: %s", lms_server_details)
            print("Enrollment on",lms_server_details)

            #cms_server_details = "http://" + cms_server_ip + ":" + cms_port + "/"
            login_dict = {
                "url": lms_server_details, #+ "login",
                "email": config_dict['login_email'],
                "password": config_dict['login_password']
                }
        except KeyError as e:
            print("622@edxe@: ",type(e),e)
            edxresponse.status_code = 500
            edxresponse.ErrMsg = "Please check some config varibles are not set in config.yml."
            return edxresponse
        except Exception as e:
            print("68@edxe@: ",type(e),e)
            edxresponse.status_code = 500
            edxresponse.ErrMsg = "Please check the config varibles in config.yml."
            return edxresponse



        # config_dict = self.read_yml('config.yml')

        #post_url = lms_server_details+"/api/enrollment/v1/enrollment/"+course_data["coursename"]+","+course_data["username"]
        # data = json.dumps(course_data)
        response = self.call_url(lms_server_details+":enrollment", "POST", login_dict, True, course_data)
        #print("@edxe@call url output",response)

        #print("call url output",edxresponse.status_code)

        #AYP This works in case of error in authentication
        #if edxresponse.status_code != 200:
        #   print("@edxe@Error is:",response["message"])
        return response

    def map_enrolldata(self, data):
        #print ("1##@##",data)
        try:
            data = json.loads(data)
        except Exception as e:
            print(e)

        #print ("2##@##",data)
        edx_data = {
        "org": data["coursename"],
        "run": data["username"]
        }
        #print ("3##@##",edx_data)
        course_data = json.dumps(edx_data)
        #print ("4##@##",course_data)
        return course_data

    def map_userdata(self, data):
        #print ("1##@##",data)
        try:
            data = json.loads(data)
        except Exception as e:
            print(e)

        #print ("2##@##",data)
        edx_data = {
        "org": data["display_org_with_default"],
        "run": data["course_run"],
        "display_name": data["display_name"],
        "number": data["display_number_with_default"]
        }
        #print ("3##@##",edx_data)
        course_data = json.dumps(edx_data)
        #print ("4##@##",course_data)
        return course_data

    def call_url(self, url_dict, method, login_dict, is_auth = False, data = None):
        edxresponse = Response()
        try:
            #print("@edxe@@session")
            session = requests.session()
            #print("@edxe@@session created",session)
        except Exception as e:
            print("86@edx:call url@: ",type(e),e)
            edxresponse.status_code = 500
            edxresponse.ErrMsg = "Unable to create a session on OpenedX."
            return edxresponse

        outdict = {}
        #abc = {}
        if is_auth == True:
            print("url is", url_dict)
            if 'enrollment' in url_dict:
            #if 'enrollment' in url_dict["url"]:
                status = self.authenticate1(login_dict, session)
            else:
                status = self.authenticate(login_dict, session)
                #print("@edxe@RETURN FROM authenticate", status)

            #print("@edxe@:") #Returned from authenticate",status['login_response'].status_code, status['login_response'].message)
            #print(status['login_response'].status_code)
            # print(status['login_response'].ErrMsg)
            if status['login_response'].status_code != 200: # or status['login_response'].json().get('success') != True:
                # print(status['login_response'].json())
                #print(status['login_response'].json().get('success')
                #if 'enrollment' in url_dict["url"]:
                if 'enrollment' in url_dict:
                    print("Failed to authenticate user", status['login_response'].json().get('value'))
                    # edxresponse.status_code = 479
                    # edxresponse.ErrMsg = "Failed to authenticate user."
                    # return edxresponse
                    abc = {"status_code": 479,"message":"Failed to authenticate user"}
                    outdict["message"] = "Failed to authenticate user"
                    outdict["status_code"] = 479
                    return outdict
                else:
                    print("@edx210@")
                    # edxresponse.status_code = 500
                    # edxresponse.ErrMsg = "Please change either the authenticate details or services of Open EdX."
                    return status['login_response'] #response

                #AYPreturn status
                #return abc

        #should this be the name as in urls.py, instead of the url?
        #if 'enrollment' in url_dict["url"]:
        if 'enrollment' in url_dict:
            #enrollment API
            #url = url_dict["url"].split(":")
            url = url_dict.split(":")
            print ("Enrollment server is>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",url)
            newcookie = status["login_response"].cookies['csrftoken']

            response = self.enroll(session, url[0]+":"+url[1], method,data["coursename"],newcookie, status["login_response"])
            print("@edxe@Call enrollment API",response)
            #return response.json()
            return response
        else:
            #for urls other than enrollment, leave original flow as it is
            print("Pass")
            pass

        response = self.get_response(session, url_dict, method, data)
        #print("@edxe@@@@@@@@@",dir(response),"\n",response, response.reason )
        print("@edxe@********** Sucess End of Call url. ********")
        return response

    def get_response(self, session, url_dict, method, data = None):
        edxresponse = Response()
        url = url_dict["url"]
        lms_server_ip =  url_dict["lms_server_ip"]
        cms_server_ip = url_dict["cms_server_ip"]
        lms_port = url_dict["lms_port"]
        cms_port = url_dict["cms_port"]
        referer ="http://" + cms_server_ip +":" + cms_port + "/home/"

        print("url in get response",url," method", method)

        if  method == "GET":
            server_response = session.get(url)
            return server_response

        elif method == "POST":
            print("in post.")
            cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(session.cookies))
            csrftoken = requests.utils.dict_from_cookiejar(cookies)['csrftoken']
            headers = {'X-CSRFToken': csrftoken,
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux86_64; rv:65.0) Gecko/20100101Firefox/65.0',
            'Accept': 'application/json, text/javascript, */*;q = 0.01',
            'Accept-Language': 'en-US,en;q = 0.5',
            'Referer': referer, #'http://10.129.103.92:18010/home/',
            'Content-Type': 'application/json;charset = utf-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection':'keep-alive'}
            print("data",data)

            try:
                server_response = session.post(url,
                    data = data,
                    headers = headers,
                    cookies = cookies)
            except requests.exceptions.ConnectionError as e:
                print("@edxe@Exception ConnectionError in post course:",e)
                edxresponse.status_code = 500
                edxresponse.ErrMsg = "Provide valid edX URL and port number."
                return Response
            except Exception as e:
                print("@edxe@131@edxe@: ",type(e),e)
                print("@edxe@35345Exception in post course:",e)
                errmsg = "Provide valid edx url."
                edxresponse.status_code = 500
                edxresponse.ErrMsg = errmsg
                return Response #({"status_code":  status.HTTP_500_INTERNAL_SERVER_ERROR, "error_code": "invalid_server", "message": errmsg})

            print("@edxe@@#$ post server_response", server_response)
            return server_response

    def enroll(self,session, server, method,course, newcookie,resp_cookie):

        outdict = {}
        config_dict = self.read_yml('config.yml')
        course_mode = config_dict['course_mode']
        print("Course mode from config.yml", course_mode)

        cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(session.cookies))
        csrftoken = requests.utils.dict_from_cookiejar(cookies)['csrftoken']

        s = server.replace("http://","")
        referrer = server + 'courses/'+course+'/about'
        #print("Referrer is ", referrer)
        headers_step3 = {
                'Content-Type': 'application/json',
                'Host': s,
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
                'Accept': 'application/json, text/javascript, */*;q = 0.01',
                'Accept-Language': 'en-US,en;q = 0.5',
                'X-CSRFToken': newcookie,
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': referrer,
                'DNT': '1',
                'Connection': 'keep-alive',
                }


        #print("Value in Headers_step3:", headers_step3)
        data_step3 = {'mode': course_mode, 'course_details':{'course_id': course}, 'enrollment_attributes':[{'namespace': 'credit','name': 'provider_id','value': 'hogwarts'}]}
        #print(data_step3)
        #incorrect server for testing of error condition(Invalid URL), remove after testing.
        step3_url = server+'/api/enrollment/v1/enrollment'
        #print("Open edX Endpoint for enrollment",step3_url)
        #print("Cookie for enrollment", resp_cookie.cookies)
        try:
            response_step3 = requests.post(step3_url, headers = headers_step3, cookies = resp_cookie.cookies, data = json.dumps(data_step3))
        except requests.exceptions.RequestException as e:
            print("Enrollment: Could not connect", e)
            outdict["message"] = "Server error. Please retry."
            outdict["status_code"] = 500
            return Response(outdict,status = 500)
        except Exception as e:
            print("Enrollment: Other error", e)
            outdict["message"] = "Server error. Please retry."
            outdict["status_code"] = 501
            return Response(outdict,status = 500)

        print("User enrolled.", response_step3)
        print("Output message is:",response_step3.text)

        #return response_step3 # this has the response json of open edx enrollment api - do we need anything from this?
        outdict["message"] = "Enrollment success"
        outdict["status_code"] = 201

        return outdict

    def authenticate(self, login_dict, sessioninfo):
        edxresponse = Response()
        login_url = login_dict['url'] + "login"
        session_login_url = login_dict['url'] + 'login_ajax'
        login_email = login_dict['email']
        login_password = login_dict['password']

        #print(sessioninfo, login_url)
        #print("@edxe@authenticate", sessioninfo, login_url)

        try:
            resp_get_login = sessioninfo.get(login_url)
            #print("@edxe@@resp_get_login:",resp_get_login, type(resp_get_login))
            #print("@edxe@358",dir(resp_get_login),"\n",resp_get_login.reason)#, resp_get_login.content)

        except Exception as e:
            print("157@edxe@: ",type(e),e)
            edxresponse.status_code = 500
            edxresponse.ErrMsg = "Unable to collect information about the current session."
            return {"login_response":edxresponse}

        #print("@edxe@resp_get_login Response:",resp_get_login.status_code)

        if(resp_get_login.status_code != 200):
            edxresponse.status_code = 500
            if(resp_get_login.status_code == 502):
                print("502")
                edxresponse.ErrMsg = "Open edX Bad Gateway."
            else:
                edxresponse.ErrMsg = "Unable to login on Open edX."
            return {"login_response":edxresponse}


        try:
            csrftoken = resp_get_login.cookies['csrftoken']
            #print("@edxe@@csrftoken:",csrftoken)
        except Exception as e:
            print("165@edxe@: ",type(e),e)
            edxresponse.status_code = 500
            edxresponse.ErrMsg = "Unable to generate csrftoken to given credential."
            return {"login_response":edxresponse}

        #print(csrftoken)

        payload = {'csrfmiddlewaretoken':csrftoken,
            'email':login_email,
            'password':login_password}

        #print("@edxe@Login payload", login_email, login_password)

        try:
            cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(sessioninfo.cookies))
            #print("@edxe@@cookies:",cookies)
        except Exception as e:
            print("165@edxe@: ",type(e),e)
            edxresponse.status_code = 500
            edxresponse.ErrMsg = "Unable to generate cookie to given credential."
            return {"login_response":edxresponse}

        try:
            resp_login = sessioninfo.post(session_login_url,
                data = payload,
                headers = dict(Referer = session_login_url),
                cookies = cookies)
            print("@edxe@409",resp_login, resp_login.reason, resp_login.content)
            #@edxe@409 OK b'{\n  "redirect_url": null, \n  "success": true\n}'
        except Exception as e:
            # print("@edxe@This error", e)
            # outdict["message"] = "Authentication failed."
            # outdict["status_code"] = 777
            # return Response(outdict,status = 777)
            print("364@edxe@: ",type(e),e)
            edxresponse.status_code = 500
            edxresponse.ErrMsg = "Open edX authentication fail."
            return {"login_response":edxresponse}

        try:
            #print("424@edxe@: ",dir(resp_login))
            #print("421@edxe@: ",resp_login.status_code, str(resp_login.json().get('value')))
            issucess = resp_login.json().get('success')
            #print("427@edxe@: ", issucess)
            if(resp_login.status_code != 200 or issucess == False):
                print("in if")
                edxresponse.status_code = 500
                reason = str(resp_login.json().get('value'))
                edxresponse.ErrMsg = "Open edX authentication fail due to " + reason #Email or password is incorrect."
                #print("425@edxe@:REturn ")
                return {"login_response":edxresponse}
        except Exception as e:
            # print("@edxe@This error", e)
            # outdict["message"] = "Authentication failed."
            # outdict["status_code"] = 777
            # return Response(outdict,status = 777)
            print("431@edxe@: ",type(e),e)
            edxresponse.status_code = 500
            edxresponse.ErrMsg = "Open edX authentication fail."
            return {"login_response":edxresponse}


        #print("@edxe@before return",sessioninfo,"\n login_response",resp_login)
        return {"login_response":resp_login}

    def authenticate1(self, login_dict, sessioninfo):
        edxresponse = Response()
        login_url = login_dict['url'] + "login"
        session_login_url = login_dict['url'] + 'login_ajax'
        login_email = login_dict['email']
        login_password = login_dict['password']


        #print(sessioninfo, login_url)
        #print("@edxe@authenticate", sessioninfo, login_url)

        try:
            resp_get_login = sessioninfo.get(login_url)
            #print("@edxe@@resp_get_login:",resp_get_login, type(resp_get_login))
        except Exception as e:
            print("157@edxe@: ",type(e),e)
            edxresponse.status_code = 500
            edxresponse.ErrMsg = "Unable to collect information about the current session."
            return {"login_response":edxresponse}

        #print("@edxe@resp_get_login Response:",resp_get_login.status_code)

        if(resp_get_login.status_code != 200):
            edxresponse.status_code = 500
            if(resp_get_login.status_code == 502):
                print("@edxe@502")
                edxresponse.ErrMsg = "Open edX Bad Gateway."
            else:
                edxresponse.ErrMsg = "Unable to login on Open edX."
            return {"login_response":edxresponse}


        try:
            csrftoken = resp_get_login.cookies['csrftoken']
            #print("@edxe@@csrftoken:",csrftoken)
        except Exception as e:
            print("165@edxe@: ",type(e),e)
            edxresponse.status_code = 500
            edxresponse.ErrMsg = "Unable to generate csrftoken to given credential."
            return {"login_response":edxresponse}

        #print(csrftoken)

        payload = {'csrfmiddlewaretoken':csrftoken,
            'email':login_email,
            'password':login_password}

        #print("@edxe@Login payload", login_email, login_password)

        try:
            cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(sessioninfo.cookies))
            #print("@edxe@@cookies:",cookies)
        except Exception as e:
            print("165@edxe@: ",type(e),e)
            edxresponse.status_code = 500
            edxresponse.ErrMsg = "Unable to generate cookie to given credential."
            return {"login_response":edxresponse}

        try:
            resp_login = sessioninfo.post(session_login_url,
                data = payload,
                headers = dict(Referer = session_login_url),
                cookies = cookies)
        except Exception as e:
            print("@edxe@This error", e)
            outdict["message"] = "Authentication failed."
            outdict["status_code"] = 777
            return Response(outdict,status = 777)

        #print("before return",sessioninfo,"\n login_response",resp_login)
        return {"login_response":resp_login}

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
