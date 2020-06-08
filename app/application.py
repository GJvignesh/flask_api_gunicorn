#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 17:01:09 2020

@author: vgopalja
"""

from flask import Flask
from flask import request
import requests     # importing the requests library
import os
import properties as conf
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO,  # Logging configuration
                    format='%(asctime)s::%(levelname)s::%(funcName)s::%(message)s')


@app.route("/")
def home():
    return "Touched Gunicorn"


@app.route("/ping")
def ping():
    return "running"


def get_bearer():
    """ Logic to get the bearer """
    token_url = conf.token_url
    data = conf.bearer_data
    logging.info("Login to " + token_url + " to get token")
    try:
        token_response = requests.post(url=token_url, data=data)  # making post call to anypoint
        logging.info(token_response)
        token_response_json = token_response.json()  # extracting response text
        bearer = token_response_json["access_token"]  # parsing bearer frm json
        return bearer
    except ValueError:
        logging.info("Parsing response as JSON failed")
    except Exception as e:
        logging.info(str(e))


@app.route("/newdeploy", methods=["POST"])
def newdeploy():
    return_response = ""
    return_response_code = conf.bad_req

    # Using try to handle file opertaion Exceptions
    try:
        # Getting all the details from the incoming headers
        Env_Id = request.headers.get("X-Anypnt-Env-Id")
        Org_Id = request.headers["X-Anypnt-Org-Id"]
        artifactName = request.headers["artifactName"]
        targetId = request.headers["targetId"]
        logging.info("Incoming Headers")
        logging.info(request.headers)

        # Calling bearer method to get the bearer
        bearer = get_bearer()

        # Deploy URL
        deploy_url = conf.deploy_url

        if bearer is not None:
            # data to be sent to token_url
            deploy_headers = {
                "x-anypnt-env-id": Env_Id,
                "x-anypnt-org-id": Org_Id,
                "Authorization": "bearer "+bearer
                }

            # 'Content-Type': "multipart/form-data",
            payload = {
                "artifactName": artifactName,
                "targetId": targetId
                }

            # pulling the incoming file
            incoming_file = request.files.get('file')
            # fetching the file name
            file_name = incoming_file.filename
            logging.info("Reading incoming deployment file -" +file_name)
            # Saving the file to local
            incoming_file.save(file_name)


            # Opening the saved file in byte format
            file = open(file_name, "rb")

            # Creating byte stream
            files = {"file":  file}

            logging.info("Calling Anypoint URL for deployment: "+deploy_url)
            # sending post request and saving response as response object
            deploy_response = requests.post(url=deploy_url, headers=deploy_headers,
                                        data=payload,
                                        files=files)
            file.close()

            # removing the saved file
            # removing the saved file
            os.remove(os.path.join(file_name))

            return_response = deploy_response.json()
            logging.info(return_response)

            return_response_code = deploy_response.status_code
        else:
            return_response = conf.auth_error
            return_response_code = conf.bad_req
            logging.info(return_response)

    except FileNotFoundError:

        return_response = conf.file_missing
        # print(return_response)
        logging.info(return_response)

    except KeyError:

        return_response = conf.header_missing
        # print(return_response)
        logging.info(return_response)

    except Exception as e:

        return_response = str(e)
        logging.info(return_response)

    return return_response, return_response_code


@app.route("/redeploy", methods=["POST"])
def redeploy():
    return_response = ""
    return_response_code = conf.bad_req

    # Using try to handle file operation Exceptions
    try:
        # Getting all the details from the incoming headers
        Env_Id = request.headers.get("X-Anypnt-Env-Id")
        Org_Id = request.headers["X-Anypnt-Org-Id"]
        id_ = request.headers["id"]
        logging.info("Incoming Headers")
        logging.info(request.headers)

        # Calling bearer method to get the bearer
        bearer = get_bearer()

        # RE-Deploy URL
        redeploy_url = conf.deploy_url+"/"+id_

        # data to be sent to token_url
        redeploy_headers = {
                "x-anypnt-env-id": Env_Id,
                "x-anypnt-org-id": Org_Id,
                "Authorization": "bearer "+bearer
                }

        # pulling the incoming file
        incoming_file = request.files.get('file')
        # fetching the file name
        file_name = incoming_file.filename
        logging.info("Reading incoming deployment file -" +file_name)
        # Saving the file to local
        incoming_file.save(file_name)
        # Opening the saved file in byte format
        file = open(file_name, "rb")

        # Creating byte stream
        files = {"file":  file}

        logging.info("Calling Anypoint URL for RE-deployment: " + redeploy_url)
        # sending patch request and saving response as response object
        redeploy_response = requests.patch(url=redeploy_url,
                                           headers=redeploy_headers,
                                           files=files)
        file.close()

        # removing the saved file
        os.remove(os.path.join(file_name))

        return_response = redeploy_response.json()
        logging.info(return_response)

        return_response_code = redeploy_response.status_code

    except FileNotFoundError:

        return_response = conf.file_missing
        print(return_response)
        logging.info(return_response)

    except KeyError:

        return_response = conf.redeploy_header_missing
        print(return_response)
        logging.info(return_response)

    except Exception as e:

        return_response = str(e)
        print(return_response)
        logging.info(return_response)

    return return_response, return_response_code

if __name__ == "__main__":
    app.run(host='0.0.0.0')
