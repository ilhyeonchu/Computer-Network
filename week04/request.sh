#!/bin/bash

curl -X 'GET' 'http://localhost:8000/' -H 'accept: application/json'; echo;
curl -X 'GET' 'http://localhost:8000/paste/0' -H 'accept: application/json'; echo;
curl -X 'GET' 'http://localhost:8000/paste/1' -H 'accept: application/json'; echo;

curl -X 'PUT' 'http://localhost:8000/paste/0' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"content": "First PUT for 0"}'; echo;
curl -X 'PUT' 'http://localhost:8000/paste/1' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"content": "Second PUT for 1"}'; echo;

curl -X 'DELETE' 'http://localhost:8000/paste/0' -H 'accept: application/json'; echo;
curl -X 'DELETE' 'http://localhost:8000/paste/1' -H 'accept: application/json'; echo;

curl -X 'POST' 'http://localhost:8000/paste/' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"content": "First post"}'; echo;
curl -X 'POST' 'http://localhost:8000/paste/' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"content": "Second post"}'; echo;

curl -X 'GET' 'http://localhost:8000/paste/0' -H 'accept: application/json'; echo;
curl -X 'GET' 'http://localhost:8000/paste/1' -H 'accept: application/json'; echo;

curl -X 'PUT' 'http://localhost:8000/paste/0' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"content": "First PUT for 0"}'; echo;
curl -X 'PUT' 'http://localhost:8000/paste/1' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"content": "Second PUT for 1"}'; echo;

curl -X 'DELETE' 'http://localhost:8000/paste/0' -H 'accept: application/json'; echo;

curl -X 'GET' 'http://localhost:8000/paste/0' -H 'accept: application/json'; echo;
curl -X 'GET' 'http://localhost:8000/paste/1' -H 'accept: application/json'; echo;
