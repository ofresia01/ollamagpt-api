#!/bin/bash

# Test the root endpoint
echo "Testing the root endpoint..."
curl -X GET "http://127.0.0.1:8000/" -H "accept: application/json"
echo -e "\n"

# Test the chat endpoint with sample prompts
echo "Testing the chat endpoint with sample prompts..."
curl -X POST "http://127.0.0.1:8000/chat" -H "accept: application/json" -H "Content-Type: application/json" -d '{"prompt": "Hello, LLM!"}'
echo -e "\n"

curl -X POST "http://127.0.0.1:8000/chat" -H "accept: application/json" -H "Content-Type: application/json" -d '{"prompt": "How are you?"}'
echo -e "\n"

curl -X POST "http://127.0.0.1:8000/chat" -H "accept: application/json" -H "Content-Type: application/json" -d '{"prompt": "Tell me a joke."}'
echo -e "\n"