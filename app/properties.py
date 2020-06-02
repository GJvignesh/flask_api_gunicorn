# Global values for Flask API

token_url =  "https://anypoint.mulesoft.com/accounts/login"

bearer_data = {"username":"pams_apiuser_dev", 
            "password":"Muletest1234"} 

bad_req =  "400 Bad Request"
    
deploy_url = "https://anypoint.mulesoft.com/hybrid/api/v1/applications"

header_missing = "Make sure headers x-anypnt-env-id, \
                x-anypnt-org-id, artifactName, targetId are avaliable"
                
file_missing = "Make sure the file is present"

redeploy_header_missing = "Make sure headers x-anypnt-env-id, id, \
                x-anypnt-org-id are avaliable"
