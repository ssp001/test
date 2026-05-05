## Ai Agent tutor

🌚🌚 
this is the main ai of the project that can intercat with stdent can chat with student and help with study stuff

# Tech Stack

```
pyresilience
agno
fastapi[standard]
sqlalchemy
ddgs
Groq
openai
pytest
```

# Folder strucher 
- app/
api
config
core
monitor
routers
service
tem
utils

- api: this is the main api endpoint of the project i used fastapi for this endpoint buliding.
- config : this is the config file like how should be data flowed in endpoint. 
- core : in this we have the main core abstraction and logic of the ai. 
- monitor : all logs will apear here we have one log file for our core absrtractions 
- routes : main roures of all the api
- service : main interation for our api endpoint
- tem : there is a tem file where ai data will be soterd as a temporary memory.


- To run fastapi server run:-
```bash
fastapi dev app\api\api_endpoint.py
```

# monitoring

- i have added monitoring for this project using grafana and promentues



