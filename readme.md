# fastAPI & datadog logging 
this is a simple example of using fastAPI with datadog for logging. the goal of this example script is to only capture ALL logs/messages generated from the fastAPI that you would normally see say in a terminal window, and pushing them directly to datadog via their API services. this process described here does not use a datadog agent, so no external dependencies outside of the python (fastAPI) application for the server. it also outputs/creates a local app.log file 

## to do: 
currently have also a very basic filter for making sure that normal consol messages that may contain 400-599 status messages are flagged as errors, which would normally not be flagged as errors because they are just the consol messages and not per say a user defined log action throwing an error that would be added to a logger 

## running
- go in and modify the .env.example file with your key and descriptions 
- to run the app:  `python main.py`  

## examples of what gets logged:
```
2023-02-19 11:19:39,079 [24179] [INFO] Starting the app logging...
2023-02-19 11:19:39,083 [24179] [DEBUG] Using selector: KqueueSelector
2023-02-19 11:19:39,092 [24179] [ERROR] Started server process [24179]
2023-02-19 11:19:39,299 [24179] [INFO] Waiting for application startup.
2023-02-19 11:19:39,363 [24179] [INFO] Application startup complete.
```

```
2023-02-19 11:15:34,174 [22291] [WARNING] Handling item request #3 doesnt like!
2023-02-19 11:15:34,299 [22291] [ERROR] 127.0.0.1:57329 - "GET /items/3 HTTP/1.1" 418
```