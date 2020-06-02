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

app = Flask(__name__)


@app.route("/")
def home():
    return "Touched Gunicorn"

@app.route("/ping")
def ping():
    return "running"

def get_bearer():
    """ Logic to get the bearer """
    token_url = conf.token_url
    # data to be sent to token_url
    data = conf.bearer_data
    # sending post request and saving response as response object
    token_response = requests.post(url=token_url, data=data)
    # extracting response text
    token_response_json = token_response.json()
    # print(token_response_json)
    bearer = token_response_json["access_token"]
    return bearer

@app.route("/newdeploy", methods=["GET", "POST"])
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
        #print(request.headers)
        # Calling bearer method to get the bearer
        bearer = get_bearer()

        # Deploy URL
        deploy_url = conf.deploy_url

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
        # Saving the file to local
        incoming_file.save(file_name)
        # Opening the saved file in byte format
        file = open(file_name, "rb")

        # Creating byte stream
        files = {"file":  file}

        # sending post request and saving response as response object
        deploy_response = requests.post(url=deploy_url, headers=deploy_headers,
                                        data=payload,
                                        files=files)
        file.close()

        # removing the saved file
        os.remove(os.path.join(file_name))

        return_response = deploy_response.json()

        return_response_code = deploy_response.status_code

    except FileNotFoundError:

        return_response = conf.file_missing
        print(return_response)

    except KeyError:

        return_response = conf.header_missing
        print(return_response)

    except Exception as e:

        return_response = str(e)
        print(return_response)

    return return_response, return_response_code


@app.route("/redeploy", methods=["GET", "POST"])
def redeploy():
    return_response = ""
    return_response_code = conf.bad_req

    # Using try to handle file opertaion Exceptions
    try:
        # Getting all the details from the incoming headers
        Env_Id = request.headers.get("X-Anypnt-Env-Id")
        Org_Id = request.headers["X-Anypnt-Org-Id"]
        id_ = request.headers["id"]

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
        # Saving the file to local
        incoming_file.save(file_name)
        # Opening the saved file in byte format
        file = open(file_name, "rb")

        # Creating byte stream
        files = {"file":  file}

        # sending patch request and saving response as response object
        redeploy_response = requests.patch(url=redeploy_url,
                                           headers=redeploy_headers,
                                           files=files)
        file.close()

        # removing the saved file
        os.remove(os.path.join(file_name))

        return_response = redeploy_response.json()
        return_response_code = redeploy_response.status_code

    except FileNotFoundError:

        return_response = conf.file_missing
        print(return_response)

    except KeyError:

        return_response = conf.redeploy_header_missing
        print(return_response)

    except Exception as e:

        return_response = str(e)
        print(return_response)

    return return_response, return_response_code

if __name__ == "__main__":
    app.run(host='0.0.0.0')
