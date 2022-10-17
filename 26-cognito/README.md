# Cognito 
    
## User Pool

User Pool needs at least 1 App Client configured - it holds authentication method, login page URL ("Hosted UI"), etc.  
Cognito App Client -> `Hosted UI` can return JWT tokens (so called "implicit grant") or one-time-use exchangable code ("authorization code grant"):
- token is returned in Hosted UI callback URL as "fragment" (text after "#") `id_token` and can only be accessed by javascript in the browser
- code is returned in Hosted UI callback URL as query parameter `code` and must be exchanged for token like this:
  ```sh
    curl -X POST 'https://upload-file-cognitto-s3.auth.us-east-1.amazoncognito.com/oauth2/token' \
    -H "Content-Type: application/x-www-form-urlencoded"   \
    -d "grant_type=authorization_code&client_id=1mqmk61lcfeolsg379msgdaev8&code=50c22963-a83c-452a-acaa-e5e5c5401688&redirect_uri=https://l4fugofqzzs276ytsm6vh7kvqy0epcui.lambda-url.us-east-1.on.aws"  
    ```
    **Note:** 
    - POST request is sent to the Client App's Hosted UI URL
    - header and `grant_type` is always the same
    - `client_id` is the User Pool Client App ID
    - `code` is what you received as query parameter in callback from Hosted UI login page
    - `redirect_uri` must match `Callback URL` defined in App client settings
### App client

Create Cognito user pool App Client as following:
- unselect option: `Generate client secret` - no need to provide the SECRET_HASH when logging in
- select option: `Enable username password based authentication` - allow to login with username and password

Then configure the App Client as following:
- `Allowed OAuth Flows`: only select `Authorization code grant` - Hosted UI login page returns one-time-use code in query param of callback url, that code must be exchanged for JWT in Cognito by backend
- `Allowed OAuth Scopes`: select all scopes

### awscli

- list user pools
    ```sh
    awscli --profile=udemy cognito-idp list-user-pools --max-results=10
    ```

    ```json
    {
        "UserPools": [
            {
                "Id": "us-east-1_FwiWPsn3Q",
                "Name": "upload-file-cognito-s3",
                "LambdaConfig": {},
                "LastModifiedDate": 1664788960.663,
                "CreationDate": 1664788960.663
            },
            {
                "Id": "us-east-1_OrdL79wqb",
                "Name": "DemoPool",
                "LambdaConfig": {},
                "LastModifiedDate": 1649356626.311,
                "CreationDate": 1649356626.311
            }
        ]
    }
    ```

- login - returns JWT.  `client-id` is the App Client ID
    ```sh
    awscli --profile=udemy  cognito-idp initiate-auth --auth-flow USER_PASSWORD_AUTH --client-id=1mqmk61lcfeolsg379msgdaev8  --auth-parameters USERNAME=admin,PASSWORD=adminadmin
    ```

   ```json
   {
     "ChallengeParameters": {},
     "AuthenticationResult": {
       "AccessToken": "eyJraWQiOiJXU3N5MXROMXd0TERkcTZTM0VpMGdZQWJha1wvRlhpUThqdm1aRVJkRVlwaz0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJlMzBmM2Y2Ni1mZjg3LTRlMGUtOGY1OS0zM2FjNjdhN2MzOTQiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9Gd2lXUHNuM1EiLCJjbGllbnRfaWQiOiIxbXFtazYxbGNmZW9sc2czNzltc2dkYWV2OCIsIm9yaWdpbl9qdGkiOiIwNGM1MTE4ZS1iZjRkLTQ3NDYtODU2NC0wOTQzZTExNGZiNjIiLCJldmVudF9pZCI6ImI2YWE0ODcxLTk4OTMtNGY3Mi04Yzk1LWVhMzllNmRmZDNhNSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE2NjQ3OTgxNDgsImV4cCI6MTY2NDgwMTc0OCwiaWF0IjoxNjY0Nzk4MTQ4LCJqdGkiOiIwOGZkMGI3Ny03ODA4LTQxZmItODU5YS0wMjA4ZTE3YTg2NjAiLCJ1c2VybmFtZSI6ImFkbWluIn0.ZOKg5l9QBs7pfRRqwONHDxzPSSvoES96n4J-Pp_Oe0rsFX2ux-QTsSccrpreCNiKz2W-3_7k6G63WUIGGwziX3p2qNVTxK3Lk9wHE1NvJBxT2qTxCTniGRzT26ldFGPHxmu2tKBJgVAoF3nhx84qbxNqmq-vZD1M0lwtsSw11-gGTuHJ-1G2k8SESNr1y5aPlONQmwcN_9K53T1eRHQz-2zG2CEH9uSYenNgh4vHWCigAJl3gcHVA-80982Pr4a_nt_9t3BGFjEql59-unLk5PnS-70yeRQXpc7X_K5cZr50Czxzu7fznqq6ooNtpkEqp9vwd8iNCBDY49yvd71UiQ",
       "ExpiresIn": 3600,
       "TokenType": "Bearer",
       "RefreshToken": "eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.kJOL1gaYFEwovAqZyeExIk-h8LagVVoKOdUrraMO2XAlsuEso6dQ0-2-HWmPu3kRkcWYomiTunWeqyKIPloWZzNRhGIzwsDgEUmLnj8aUMm2UlXEvIQzZqSAZcTBIjWUfx-3dP27KSOcu3aUKVqFneu2ymkNUoS2ay3uOcq9aQB3aAt9EeS3avuGOoda6GRFz0WpoORm94YyUp0zOLv74Jz7J8b1j7iVwGBAUmAaKPL2k_jEBZlWsiJ0cupyRD30Q3TakBOaJNAoNIAkdobFX6sYHI2xYACe6eZDtpJ3d79la16Ce35F09KqKVNhuSwR_KBYlDcQUGK3qpvX1WySVQ.-h7vgwVzmetCf7Qj.ZuSzF3NGRZ8CpcqrOUAcNX2l45ycuwUA0ew9PwNR8FGviHI8DK9SgZ5c-1R_BzUWBvaQd3Vw-j9C9e25Ub3i2IpEmr4mSvg-CkSGm7dCXrSmrAPWCQJr5novpJfYnsC7iv_m8qzMlPaxWr55PTV_C23axdUPDyjP4dHM4gT62HTf-XXDjCtaWc6xOGbByL0GYX3rkzyuek4khOtfuf9w_OQhofEBzdg5uCplpsV7KqRGb6BcMSyiwbmGYq8Dj-7XNxKx3vVZaEMUi6ebBGWLJNMUSgyV6bzZ46So4bbTdKbZGiaD0KVxbpsxgpTTx4qIxcuOrhLmAxDnAzeVA_zKF8B_wc6wGR8pRsTWByFR2ZeP8aOjQw0tl-D1qDJh9BGQrlJeYe43q_0dyLVGw1qPLDdMmLE1o9DBClH7YDmUtH1KTHevshZGAEsU2vE4GX9mDBeq-3aKAexOftYSmFN5z5G3YdxmvDNG2xEt5MgctyQqochAgsmvkI7HFsLDoV7NtZawVHsEAOQzjX5YLav77iD4ME9gRlkMYrXNMOIQcoA3dXLGYVCcYjupf_G7GVJmrbLPPIMTxQz5btwRvU0IcPRkIP7DA5v06fTzmAItqIr9LiV_S-VPFNHHK8pHRrzBd1MOYZ7zqazWV0qLGr0a3pnYcMICESpLh0q0lLEeKykxnYMYqsFFMC-0a-PP0X5VM-GPHDUf9wisi0Q-NSZGBWe-xBQnjBCesq7uQXv1FMbpJQEioVvrhic7ERu4tnAyDt6SGcV-_10Rc2xiuuLl1fNxbvtrUC-AsdUOkeQwEC-qaqvvLHjki-FDBTjaayqcCAYl9nw-rwez3ZJrLVD2iA7mpz8O_Ldaom068Lq31O9c-UTcr9fKNXWNsNILRI0d-Iw6akCzfCLxipsoY2-ZCMuxb0ft2QwUEdV3kh84C7vHyKAmZ3LS3yiv6tH5OeSylLKEs8tGKENnR9wKRy2JW4h5kO_8aqbY0dPVTJtxiWEPFebtceA7sJsfDjHgNyUcVWfVWHPfChIt1qim2Klqpa9R-R5jDLdFHP4DEeFwtSghNjnK-wCRZT7mFe6GSzRWvq8g5T_6Bt63ap1hpnjCTkuP8WLyoVMQrq-RFI9zkIXYD4-8oH_6CL3VjT2TzvQwc_LiCoWLc0ZiJJoRlISLyl6kneayyrTBVP0Z6NBv4isGbH5Q3U6HFM4D_owjP0LvMcwmbM-B9-2H2GM9HX7uBmJyJjjebDISKCxZItUyy_B8HcQ00ULX8z730DKdu3lfW86T.zLL61yLB271zeXnpuSYL8Q",
       "IdToken": "eyJraWQiOiJuemRyNXFpREJ0dnNlZkpZSnh4dGFmYm9CTTZxS0ZjNnhUS1d0dGlEcW9rPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJlMzBmM2Y2Ni1mZjg3LTRlMGUtOGY1OS0zM2FjNjdhN2MzOTQiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfRndpV1BzbjNRIiwiY29nbml0bzp1c2VybmFtZSI6ImFkbWluIiwib3JpZ2luX2p0aSI6IjA0YzUxMThlLWJmNGQtNDc0Ni04NTY0LTA5NDNlMTE0ZmI2MiIsImF1ZCI6IjFtcW1rNjFsY2Zlb2xzZzM3OW1zZ2RhZXY4IiwiZXZlbnRfaWQiOiJiNmFhNDg3MS05ODkzLTRmNzItOGM5NS1lYTM5ZTZkZmQzYTUiLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTY2NDc5ODE0OCwiZXhwIjoxNjY0ODAxNzQ4LCJpYXQiOjE2NjQ3OTgxNDgsImp0aSI6ImFjYzEwOTdmLTE3YjAtNDJkMi1hYmNkLTM3OTZhZTk1MzRhZiIsImVtYWlsIjoiYWRtaW5AbWF0ZXVzem1pZG9yLmxpbmsifQ.cZyRZci2OEVQ6idfm-4xp4cn1yn6v06nirvlVDgRRaiVfy3As6nnc6fwTZk3-lmRREKmtNrbpN9wzAAFJD2D0Wbxv_Gv13iA8Ofl4kYrLzaCWfD2bJnGfncQMSCNB1SFQ6Qm164kbdfra0gZPr9QpZSnW5ZQ-40v8I288U2IqQK-kT__zLdfGMvfPdawMmX5FoJvkFsy5_39JDofmxd4akTTvLnHqlVI0CQ6d6CGoeYhpMJAIQnhIYzJydQ1AvonmmS07ptsj8KQBqjziexy4D0Hbl9_dWFGMZRUz9VnfNmQqaGKPAnlLw4vHfB6Kk6j-Ee0yP6_psTLlIeF2aZ_Gg"
     }
   }
   ```

## API Gateway integration

Cognito Authorizer expects header "Authorization: Bearer <id_token>" to let the request through.  
https://mydeveloperplanet.com/2022/01/25/how-to-secure-aws-api-gateway-with-cognito-user-pool/

### Test Cognito Authorizer
Use `IdToken` from `awscli --profile=udemy  cognito-idp initiate-auth ...` response as Authorization Token -> Authorization (header):

```
Bearer eyJraWQiOiJuemRyNXFpREJ0dnNlZkpZSnh4dGFmYm9CTTZxS0ZjNnhUS1d0dGlEcW9rPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJlMzBmM2Y2Ni1mZjg3LTRlMGUtOGY1OS0zM2FjNjdhN2MzOTQiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfRndpV1BzbjNRIiwiY29nbml0bzp1c2VybmFtZSI6ImFkbWluIiwib3JpZ2luX2p0aSI6ImQwNDM2YzQ0LWFlNjktNDc5MC1hZmE3LWQxYzA0MDQxNDc1ZCIsImF1ZCI6IjFtcW1rNjFsY2Zlb2xzZzM3OW1zZ2RhZXY4IiwiZXZlbnRfaWQiOiI5ZDMwYzNkNy1mOGNmLTRmY2UtYjY1NS0xODNiM2ZhODRlMzkiLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTY2NDc5ODAxNiwiZXhwIjoxNjY0ODAxNjE2LCJpYXQiOjE2NjQ3OTgwMTYsImp0aSI6IjQwNmFhNjg5LTk0NTUtNGYzMy1iNTE3LTgwOTYwNjBkNDA5MiIsImVtYWlsIjoiYWRtaW5AbWF0ZXVzem1pZG9yLmxpbmsifQ.WieY9mybNYrqmX7TJMIud9Buo8iczIH93axCMsq4E3G2F0gvriYCzvbY1i1ogNWchXLaLl5zYIMeFFfYzgXywy-OU_SWpMt773BwVsH7r7DwWFqEryIG4TBrwvuqE1Lx-yJYSEsQt_VeczbG_bA7KxJbL_lo9kN5SXqUVQZZBqy6bZSVdFTDyvF0AIic0PxqtjNHSO6yrtZGeaigaHBc0EpeO-kXoK06DqXr8VIP7UTFVpJfN3d8v7m32DDVU7ScyDPZkj6uBdkYW-0sBy7RblvTBLs7ykapzmGvQPPGGk1-4Yak4cmIw-yygYlmOhDFRl926m_8drBdFOnN3fdDdQ
```
```json
{
  "aud": "1mqmk61lcfeolsg379msgdaev8",
  "auth_time": "1664798016",
  "cognito:username": "admin",
  "email": "admin@mateuszmidor.link",
  "email_verified": "true",
  "event_id": "9d30c3d7-f8cf-4fce-b655-183b3fa84e39",
  "exp": "Mon Oct 03 12:53:36 UTC 2022",
  "iat": "Mon Oct 03 11:53:36 UTC 2022",
  "iss": "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_FwiWPsn3Q",
  "jti": "406aa689-9455-4f33-b517-8096060d4092",
  "origin_jti": "d0436c44-ae69-4790-afa7-d1c04041475d",
  "sub": "e30f3f66-ff87-4e0e-8f59-33ac67a7c394",
  "token_use": "id"
}
```

## Hosted UI callback handler for authorization code

Exchange `code` received in url query param for JWT and decode the JWT:

```python
import json
import urllib3
import base64
import traceback

HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}

# Cognito User Pool App Client specific
HOSTED_UI_URL = "https://upload-file-cognitto-s3.auth.us-east-1.amazoncognito.com/oauth2/token" # this is the App Client Hosted UI url + "/oauth2/token"
REDIRECT_URL = "https://l4fugofqzzs276ytsm6vh7kvqy0epcui.lambda-url.us-east-1.on.aws" # this is this lambda url - the callback handler 
APP_CLIENT_ID = "1mqmk61lcfeolsg379msgdaev8" # Cognito User Pool App Client ID that is used for authorization
POST_DATA = f"grant_type=authorization_code&client_id={APP_CLIENT_ID}&redirect_uri={REDIRECT_URL}&code=%s" # code exchange request payload

def lambda_handler(event, context):
    try:
        cognito_code = event['queryStringParameters']["code"]
        response = exchange_code_for_tokens(cognito_code)
        jwt_str = response["id_token"]
        jwt = jwt_decode(jwt_str)
        return {
            'statusCode': 200,
            'body': jwt
        }
    except Exception as e:
        return {
            'statusCode': 200,
            'body': {"error": repr(e), "traceback": traceback.format_exc(), "event": event, "code_exchange_response": str(response)}
        }
    

def exchange_code_for_tokens(code):
    data = POST_DATA % code
    http = urllib3.PoolManager()
    r = http.urlopen('POST', HOSTED_UI_URL, headers=HEADERS, body=data)
    json_response = r.data.decode("utf-8" ) 
    return json.loads(json_response)
    
def jwt_decode(jwt_str):
    jwt_sections = jwt_str.split(".")[0:2]  # header & payload
    
    items = []
    for section in jwt_sections:
        padded_section = section + "=" * (-len(section) % 4)
        json_str = base64.b64decode(padded_section)
        dic = json.loads(json_str)
        items.append(dic)
    return {"header" : items[0], "payload" : items[1]}
```

## Hosted UI callback handler for authorization token 

```python
import traceback


def lambda_handler(event, context):
    try:
        return {
            'statusCode': 200,
            "headers": {
                'Content-Type': 'text/html',
            },
            'body': HTML,
        }
    except Exception as e:
        return {
            'statusCode': 200,
            'body': {"error": repr(e), "traceback": traceback.format_exc(), "event": event}
        }
    
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <script>
        function run() {
            hash = window.location.hash;
            start = hash.indexOf("id_token");
            end = hash.indexOf("&", start);
            id_token = hash.substring(start+9, end)
            document.getElementById("demo").innerHTML = id_token;
          }
    </script>
</head>
<body onload="run()" >
    <h1>Cognito User Pools with implicit grant</h1>
    <p>Login response id_token:</p>
    <p id="demo">My first paragraph.</p>
</body>
</html> 
'''
```