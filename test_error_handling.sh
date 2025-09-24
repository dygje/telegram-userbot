#!/bin/bash

# Skrip Pengujian Error Handling Telegram Userbot
echo "=== Memulai Pengujian Error Handling Telegram Userbot ==="

# Memulai backend
echo "1. Memulai backend..."
cd /workspaces/telegram-userbot/backend
TELEGRAM_API_ID=123456 TELEGRAM_API_HASH=test_hash PHONE_NUMBER=+1234567890 SESSION_STRING=test_session_string SECRET_KEY=test_secret_key_for_testing_purposes_only DATABASE_URL=sqlite+aiosqlite:///./test_telegram_bot.db NEXT_PUBLIC_API_URL=http://localhost:8000 uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/backend_error.log 2>&1 &
BACKEND_PID=$!

# Tunggu backend siap
echo "2. Menunggu backend siap..."
sleep 10

# Cek kesehatan API
echo "3. Menguji kesehatan API..."
HEALTH=$(curl -s http://localhost:8000/health)
if [[ "$HEALTH" == *"healthy"* ]]; then
    echo "✓ API health check berhasil"
else
    echo "✗ API health check gagal"
    kill $BACKEND_PID
    exit 1
fi

# Pengujian endpoint yang tidak ada
echo "4. Menguji endpoint yang tidak ada..."
NONEXISTENT_ENDPOINT_RESPONSE=$(curl -s -w "%{http_code}" http://localhost:8000/api/v1/nonexistent)
HTTP_CODE=$(echo "$NONEXISTENT_ENDPOINT_RESPONSE" | tail -c 4)
if [[ $HTTP_CODE -eq 404 ]]; then
    echo "✓ Penanganan endpoint tidak ada berhasil (404 Not Found)"
else
    echo "✗ Penanganan endpoint tidak ada gagal (HTTP $HTTP_CODE)"
fi

# Pengujian method yang tidak didukung
echo "5. Menguji method yang tidak didukung..."
UNSUPPORTED_METHOD_RESPONSE=$(curl -s -w "%{http_code}" -X PUT http://localhost:8000/api/v1/groups)
HTTP_CODE=$(echo "$UNSUPPORTED_METHOD_RESPONSE" | tail -c 4)
if [[ $HTTP_CODE -eq 405 ]]; then
    echo "✓ Penanganan method tidak didukung berhasil (405 Method Not Allowed)"
else
    echo "✗ Penanganan method tidak didukung gagal (HTTP $HTTP_CODE)"
fi

# Pengujian request body yang tidak valid
echo "6. Menguji request body yang tidak valid..."
INVALID_BODY_RESPONSE=$(curl -s -w "%{http_code}" -X POST http://localhost:8000/api/v1/groups -H "Content-Type: application/json" -d '{"invalid_field": "value"}')
HTTP_CODE=$(echo "$INVALID_BODY_RESPONSE" | tail -c 4)
if [[ $HTTP_CODE -eq 422 ]] || [[ $HTTP_CODE -eq 400 ]]; then
    echo "✓ Penanganan request body tidak valid berhasil (HTTP $HTTP_CODE)"
else
    echo "✗ Penanganan request body tidak valid gagal (HTTP $HTTP_CODE)"
fi

# Pengujian penghapusan grup yang tidak ada
echo "7. Menguji penghapusan grup yang tidak ada..."
DELETE_NONEXISTENT_GROUP_RESPONSE=$(curl -s -w "%{http_code}" -X DELETE http://localhost:8000/api/v1/groups/nonexistent_group)
HTTP_CODE=$(echo "$DELETE_NONEXISTENT_GROUP_RESPONSE" | tail -c 4)
if [[ $HTTP_CODE -eq 404 ]] || [[ $HTTP_CODE -eq 200 ]]; then
    echo "✓ Penanganan penghapusan grup tidak ada berhasil (HTTP $HTTP_CODE)"
else
    echo "✗ Penanganan penghapusan grup tidak ada gagal (HTTP $HTTP_CODE)"
fi

# Pengujian penghapusan pesan yang tidak ada
echo "8. Menguji penghapusan pesan yang tidak ada..."
DELETE_NONEXISTENT_MESSAGE_RESPONSE=$(curl -s -w "%{http_code}" -X DELETE http://localhost:8000/api/v1/messages/999999)
HTTP_CODE=$(echo "$DELETE_NONEXISTENT_MESSAGE_RESPONSE" | tail -c 4)
if [[ $HTTP_CODE -eq 404 ]] || [[ $HTTP_CODE -eq 200 ]]; then
    echo "✓ Penanganan penghapusan pesan tidak ada berhasil (HTTP $HTTP_CODE)"
else
    echo "✗ Penanganan penghapusan pesan tidak ada gagal (HTTP $HTTP_CODE)"
fi

# Pengujian update konfigurasi dengan key yang tidak valid
echo "9. Menguji update konfigurasi dengan key yang tidak valid..."
INVALID_CONFIG_KEY_RESPONSE=$(curl -s -w "%{http_code}" -X POST http://localhost:8000/api/v1/config -H "Content-Type: application/json" -d '{"key": "invalid_key", "value": "some_value"}')
HTTP_CODE=$(echo "$INVALID_CONFIG_KEY_RESPONSE" | tail -c 4)
if [[ $HTTP_CODE -eq 200 ]] || [[ $HTTP_CODE -eq 400 ]]; then
    echo "✓ Penanganan update konfigurasi dengan key tidak valid berhasil (HTTP $HTTP_CODE)"
else
    echo "✗ Penanganan update konfigurasi dengan key tidak valid gagal (HTTP $HTTP_CODE)"
fi

# Hentikan backend
echo "10. Menghentikan backend..."
kill $BACKEND_PID
sleep 3

echo "=== Pengujian Error Handling Selesai ==="
echo "Pengujian error handling selesai. Silakan periksa hasil di atas."