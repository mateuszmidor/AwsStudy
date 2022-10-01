# Example of plain LAMBDA integration - a calculator with just "+" operation

## Lambda function

```python
import json

def lambda_handler(event, context):
    try:
        params = event["queryStringParameters"] # this will work for both, API Gateway Lambda integration and direct Lambda URL call
        a = int(params['a'])
        b = int(params['b'])
    except:
        return http200(html) # missing parameters - show the calculator page     
        
    result = f"<b>result: {a+b}</b>"
    return http200(result) # show the results page
    
def http200(body):
    return {
        "statusCode": 200,
        "isBase64Encoded": False,
        "headers": {
            "Content-Type": "text/html"
        },
        "body": body
    }
    
html= '''
<form action="?">
    <label for="a">a:</label><br>
    <input type="number" id="a" name="a" value="3"><br>
    <label for="b">b:</label><br>
    <input type="number" id="b" name="b" value="5"><br><br>
    <input type="submit" value="Submit">
</form>
'''
```

## API Gateway - GET method

### 1. Method Request

- add parameters "a" and "b" in `URL Query String Parameters` as non-required 
- make other sections empty (HTTP Request Headers, Request Body, SDK Settings)

### 2. Integration request

- uncheck `Use Lambda Proxy integration`
- all sections empty except for Mapping Templates:
  - `When there are no templates defined (recommended)`
  - `application/json`:
    ```velocity
    {
        #set($has_a = $input.params("a") != "")
        #set($has_b = $input.params("b") != "")
        "queryStringParameters": {
            #if($has_a and $has_b)
            "a": $input.params("a"),
            "b": $input.params("b") 
            #end
        }
    }
    ```

### 3. Integration response

- Header Mappings (the ticks "`" are important)
    ```text
    Content-Type 'text/html'
    ```

- Mapping Templates
  - text/html  
    ```velocity
    $input.path('$.body')
    ```

### 4. Method response

Leave as is.