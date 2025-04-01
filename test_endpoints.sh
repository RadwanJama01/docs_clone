#!/bin/bash

BASE_URL=http://127.0.0.1:5000

echo "🚀 Adding user..."
curl -s -X POST $BASE_URL/user/add \
-H "Content-Type: application/json" \
-d '{"username": "radwan", "email": "rad@example.com", "password": "securepass"}'
echo -e "\n------------------------------------"

echo "🔐 Logging in..."
curl -s -X POST $BASE_URL/user/login \
-H "Content-Type: application/json" \
-d '{"email": "rad@example.com", "password": "securepass"}'
echo -e "\n------------------------------------"

echo "📋 Fetching all users..."
curl -s -X GET $BASE_URL/user/all \
-w "\nStatus Code: %{http_code}\n"
echo "------------------------------------"
