
## About the Project
I was going through Zapier's most popular projects and saw one that did something simialr with Twilio and an Email. I decided i'd make my own version that could do the same thing with minial setup time. All you have to do is write a few lines of code to get everythig oing.

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

The only package you need outisde of everything that comes with Python3 is the requests library.

### Quick Start
I'll show you how to get a quick example started. You will need something like ngork to open a quick and easy public tunnel for your project.
1. Create a folder for your project
2. Install FastAPI, Uvicorn, and TwilioToEmail
```sh
pip3 install fastapi uvicorn TwilioToEmail
```

3. Make a Python file to run FastAPI
```python
from fastapi import FastAPI, Request
from TwilioToEmail import SmsMessage
from TwilioToEmail import Email

@app.post("/")
async def root():
    #pass the request body into a var, then decode the body
    request_body = await request.body()
    request_body = request_body.decode()

    #create the SmsMessage class from TwilioToEmail
    twilio_message = SmsMessage(request_body.split("&"))

    #create the Emailclass from TwilioToEmail, then call the send_email() function
    email = Email("recievers_email", "senders_email","subject_line")
    #now simply pass the SmsMessage object into the send_email() function
    email.send(twilio_message)

    #return HTTP response 200
    return(200)
```

4. 


<!-- ROADMAP -->
<!-- ## Roadmap
