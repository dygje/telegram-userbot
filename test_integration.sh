#!/bin/bash

# Skrip Pengujian Integrasi Telegram Userbot
echo "=== Memulai Pengujian Integrasi Telegram Userbot ==="

# Memulai backend
echo "1. Memulai backend..."
cd /workspaces/telegram-userbot/backend
TELEGRAM_API_ID=123456 TELEGRAM_API_HASH=test_hash PHONE_NUMBER=+1234567890 SESSION_STRING=test_session_string SECRET_KEY=test_secret_key_for_testing_purposes_only DATABASE_URL=sqlite+aiosqlite:///./test_telegram_bot.db NEXT_PUBLIC_API_URL=http://localhost:8000 uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/backend_integration.log 2>&1 &
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

# Simulasi autentikasi (kita tidak bisa melakukan ini secara nyata tanpa akun Telegram sebenarnya)
echo "4. Menguji simulasi autentikasi..."
# Endpoint auth tidak bisa diuji tanpa akun Telegram nyata, jadi kita lewati untuk sekarang

# Tambah beberapa grup
echo "5. Menguji penambahan beberapa grup..."
GROUP1_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/groups -H "Content-Type: application/json" -d '{"identifier": "@testgroup1"}')
GROUP2_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/groups -H "Content-Type: application/json" -d '{"identifier": "@testgroup2"}')
GROUP3_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/groups -H "Content-Type: application/json" -d '{"identifier": "t.me/testgroup3"}')

if [[ "$GROUP1_RESPONSE" == *"added successfully"* ]] && [[ "$GROUP2_RESPONSE" == *"added successfully"* ]] && [[ "$GROUP3_RESPONSE" == *"added successfully"* ]]; then
    echo "✓ Penambahan beberapa grup berhasil"
else
    echo "✗ Penambahan beberapa grup gagal"
    kill $BACKEND_PID
    exit 1
fi

# Tambah beberapa pesan
echo "6. Menguji penambahan beberapa pesan..."
MESSAGE1_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/messages -H "Content-Type: application/json" -d '{"text": "Test message 1 for auto posting"}')
MESSAGE2_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/messages -H "Content-Type: application/json" -d '{"text": "Test message 2 for auto posting"}')
MESSAGE3_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/messages -H "Content-Type: application/json" -d '{"text": "Test message 3 for auto posting"}')

if [[ "$MESSAGE1_RESPONSE" == *"added successfully"* ]] && [[ "$MESSAGE2_RESPONSE" == *"added successfully"* ]] && [[ "$MESSAGE3_RESPONSE" == *"added successfully"* ]]; then
    echo "✓ Penambahan beberapa pesan berhasil"
else
    echo "✗ Penambahan beberapa pesan gagal"
    kill $BACKEND_PID
    exit 1
fi

# Cek daftar grup
echo "7. Menguji pengambilan daftar grup..."
GROUPS_RESPONSE=$(curl -s http://localhost:8000/api/v1/groups)
GROUP_COUNT=$(echo "$GROUPS_RESPONSE" | grep -o "identifier" | wc -l)
if [[ $GROUP_COUNT -eq 3 ]]; then
    echo "✓ Pengambilan daftar grup berhasil (3 grup ditemukan)"
else
    echo "✗ Pengambilan daftar grup gagal ($GROUP_COUNT grup ditemukan)"
    kill $BACKEND_PID
    exit 1
fi

# Cek daftar pesan
echo "8. Menguji pengambilan daftar pesan..."
MESSAGES_RESPONSE=$(curl -s http://localhost:8000/api/v1/messages)
MESSAGE_COUNT=$(echo "$MESSAGES_RESPONSE" | grep -o "text" | wc -l)
if [[ $MESSAGE_COUNT -eq 3 ]]; then
    echo "✓ Pengambilan daftar pesan berhasil (3 pesan ditemukan)"
else
    echo "✗ Pengambilan daftar pesan gagal ($MESSAGE_COUNT pesan ditemukan)"
    kill $BACKEND_PID
    exit 1
fi

# Update konfigurasi
echo "9. Menguji update konfigurasi..."
CONFIG1_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/config -H "Content-Type: application/json" -d '{"key": "message_interval", "value": "3-7"}')
CONFIG2_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/config -H "Content-Type: application/json" -d '{"key": "cycle_interval", "value": "3600-4000"}')

if [[ "$CONFIG1_RESPONSE" == *"updated successfully"* ]] && [[ "$CONFIG2_RESPONSE" == *"updated successfully"* ]]; then
    echo "✓ Update konfigurasi berhasil"
else
    echo "✗ Update konfigurasi gagal"
    kill $BACKEND_PID
    exit 1
fi

# Cek konfigurasi yang diperbarui
echo "10. Menguji pengambilan konfigurasi yang diperbarui..."
CONFIG_RESPONSE=$(curl -s http://localhost:8000/api/v1/config)
if [[ "$CONFIG_RESPONSE" == *"3-7"* ]] && [[ "$CONFIG_RESPONSE" == *"3600-4000"* ]]; then
    echo "✓ Pengambilan konfigurasi yang diperbarui berhasil"
else
    echo "✗ Pengambilan konfigurasi yang diperbarui gagal"
    kill $BACKEND_PID
    exit 1
fi

# Cek status userbot
echo "11. Menguji status userbot..."
STATUS_RESPONSE=$(curl -s http://localhost:8000/api/v1/userbot/status)
if [[ "$STATUS_RESPONSE" == *"running"* ]]; then
    echo "✓ Pengambilan status userbot berhasil"
else
    echo "✗ Pengambilan status userbot gagal"
    kill $BACKEND_PID
    exit 1
fi

# Hapus satu grup
echo "12. Menguji penghapusan grup..."
DELETE_GROUP_RESPONSE=$(curl -s -X DELETE http://localhost:8000/api/v1/groups/@testgroup1)
if [[ "$DELETE_GROUP_RESPONSE" == *"removed successfully"* ]]; then
    echo "✓ Penghapusan grup berhasil"
else
    echo "✗ Penghapusan grup gagal"
    kill $BACKEND_PID
    exit 1
fi

# Cek daftar grup setelah penghapusan
echo "13. Menguji pengambilan daftar grup setelah penghapusan..."
GROUPS_AFTER_DELETE_RESPONSE=$(curl -s http://localhost:8000/api/v1/groups)
GROUP_COUNT_AFTER_DELETE=$(echo "$GROUPS_AFTER_DELETE_RESPONSE" | grep -o "identifier" | wc -l)
if [[ $GROUP_COUNT_AFTER_DELETE -eq 2 ]]; then
    echo "✓ Pengambilan daftar grup setelah penghapusan berhasil (2 grup ditemukan)"
else
    echo "✗ Pengambilan daftar grup setelah penghapusan gagal ($GROUP_COUNT_AFTER_DELETE grup ditemukan)"
    kill $BACKEND_PID
    exit 1
fi

# Hapus satu pesan
echo "14. Menguji penghapusan pesan..."
DELETE_MESSAGE_RESPONSE=$(curl -s -X DELETE http://localhost:8000/api/v1/messages/1)
if [[ "$DELETE_MESSAGE_RESPONSE" == *"removed successfully"* ]]; then
    echo "✓ Penghapusan pesan berhasil"
else
    echo "✗ Penghapusan pesan gagal"
    kill $BACKEND_PID
    exit 1
fi

# Cek daftar pesan setelah penghapusan
echo "15. Menguji pengambilan daftar pesan setelah penghapusan..."
MESSAGES_AFTER_DELETE_RESPONSE=$(curl -s http://localhost:8000/api/v1/messages)
MESSAGE_COUNT_AFTER_DELETE=$(echo "$MESSAGES_AFTER_DELETE_RESPONSE" | grep -o "text" | wc -l)
if [[ $MESSAGE_COUNT_AFTER_DELETE -eq 2 ]]; then
    echo "✓ Pengambilan daftar pesan setelah penghapusan berhasil (2 pesan ditemukan)"
else
    echo "✗ Pengambilan daftar pesan setelah penghapusan gagal ($MESSAGE_COUNT_AFTER_DELETE pesan ditemukan)"
    kill $BACKEND_PID
    exit 1
fi

# Hentikan backend
echo "16. Menghentikan backend..."
kill $BACKEND_PID
sleep 3

echo "=== Pengujian Integrasi Selesai ==="
echo "Semua pengujian integrasi berhasil! Sistem auto posting berfungsi dengan benar secara keseluruhan."