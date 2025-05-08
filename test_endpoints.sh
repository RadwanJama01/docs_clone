#!/bin/bash

BASE_URL=http://127.0.0.1:5000
USER_EMAIL="rad@example.com"
USERNAME="radwan"
PASSWORD="securepass"
NOTE_ID=1
OWNER_ID=1  # assuming the user created gets ID = 1
CREATED_AT="2025-04-09T00:00:00"

echo -e "\n🎯 STARTING FULL API TEST SUITE...\n"

# ----------------------------
echo "🚀 Adding user..."
curl -s -X POST $BASE_URL/user/add \
-H "Content-Type: application/json" \
-d "{\"username\": \"$USERNAME\", \"email\": \"$USER_EMAIL\", \"password\": \"$PASSWORD\"}" \
-w "\nStatus Code: %{http_code}\n"
echo "------------------------------------"

# ----------------------------
echo "🔐 Logging in..."
curl -s -X POST $BASE_URL/user/login \
-H "Content-Type: application/json" \
-d "{\"email\": \"$USER_EMAIL\", \"password\": \"$PASSWORD\"}" \
-w "\nStatus Code: %{http_code}\n"
echo "------------------------------------"

# ----------------------------
echo "📝 Creating a note..."
curl -s -X POST $BASE_URL/note/create \
-H "Content-Type: application/json" \
-d "{
  \"id\": $NOTE_ID,
  \"owner\": $OWNER_ID,
  \"created_at\": \"$CREATED_AT\",
  \"title\": \"Test Note from Script\",
  \"content\": \"This note was created during a test run 🚀\"
}" \
-w "\nStatus Code: %{http_code}\n"
echo "------------------------------------"

# ----------------------------
echo "📥 Fetching created note..."
curl -s -X GET $BASE_URL/note/$NOTE_ID \
-w "\nStatus Code: %{http_code}\n"
echo "------------------------------------"

# ----------------------------
echo "✏️ Updating note..."
curl -s -X PUT $BASE_URL/note/$NOTE_ID/update \
-H "Content-Type: application/json" \
-d '{"title": "Updated Title", "content": "Updated note content for collab test"}' \
-w "\nStatus Code: %{http_code}\n"
echo "------------------------------------"

# ----------------------------
echo "🔄 Fetching updated note..."
curl -s -X GET $BASE_URL/note/$NOTE_ID \
-w "\nStatus Code: %{http_code}\n"
echo "------------------------------------"

# ----------------------------
echo "🗑️ Deleting note..."
curl -s -X DELETE $BASE_URL/note/$NOTE_ID/delete \
-w "\nStatus Code: %{http_code}\n"
echo "------------------------------------"

# ----------------------------
echo "❌ Confirming note deletion..."
curl -s -X GET $BASE_URL/note/$NOTE_ID \
-w "\nStatus Code: %{http_code}\n"
echo "------------------------------------"

# ----------------------------
echo "📋 Fetching all users..."
curl -s -X GET $BASE_URL/user/all \
-w "\nStatus Code: %{http_code}\n"
echo "------------------------------------"

echo -e "\n✅ ALL TESTS COMPLETED!\n"
