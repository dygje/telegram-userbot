#!/bin/bash

# Skrip Pengujian Fungsional Telegram Userbot
echo "=== Memulai Pengujian Fungsional Telegram Userbot ==="

# Memulai backend
echo "1. Memulai backend..."
cd /workspaces/telegram-userbot/backend
TELEGRAM_API_ID=123456 TELEGRAM_API_HASH=test_hash PHONE_NUMBER=+1234567890 SESSION_STRING=test_session_string SECRET_KEY=test_secret_key_for_testing_purposes_only DATABASE_URL=sqlite+aiosqlite:///./test_telegram_bot.db NEXT_PUBLIC_API_URL=http://localhost:8000 uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/backend.log 2>&1 &
BACKEND_PID=$!

# Tunggu backend siap
echo "2. Menunggu backend siap..."
sleep 10

# Cek kesehatan
echo "3. Menguji kesehatan API..."
HEALTH=$(curl -s http://localhost:8000/health)
if [[ "$HEALTH" == *"healthy"* ]]; then
    echo "✓ API health check berhasil"
else
    echo "✗ API health check gagal"
    kill $BACKEND_PID
    exit 1
fi

# Tambah grup
echo "4. Menguji penambahan grup..."
GROUP_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/groups -H "Content-Type: application/json" -d '{"identifier": "@testgroup1"}')
if [[ "$GROUP_RESPONSE" == *"added successfully"* ]]; then
    echo "✓ Penambahan grup berhasil"
else
    echo "✗ Penambahan grup gagal"
    kill $BACKEND_PID
    exit 1
fi

# Tambah pesan
echo "5. Menguji penambahan pesan..."
MESSAGE_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/messages -H "Content-Type: application/json" -d '{"text": "Test message for auto posting"}')
if [[ "$MESSAGE_RESPONSE" == *"added successfully"* ]]; then
    echo "✓ Penambahan pesan berhasil"
else
    echo "✗ Penambahan pesan gagal"
    kill $BACKEND_PID
    exit 1
fi

# Cek konfigurasi
echo "6. Menguji pengambilan konfigurasi..."
CONFIG_RESPONSE=$(curl -s http://localhost:8000/api/v1/config)
if [[ "$CONFIG_RESPONSE" == *"message_interval"* ]] && [[ "$CONFIG_RESPONSE" == *"cycle_interval"* ]]; then
    echo "✓ Pengambilan konfigurasi berhasil"
else
    echo "✗ Pengambilan konfigurasi gagal"
    kill $BACKEND_PID
    exit 1
fi

# Cek status userbot
echo "7. Menguji status userbot..."
STATUS_RESPONSE=$(curl -s http://localhost:8000/api/v1/userbot/status)
if [[ "$STATUS_RESPONSE" == *"running"* ]]; then
    echo "✓ Pengambilan status userbot berhasil"
else
    echo "✗ Pengambilan status userbot gagal"
    kill $BACKEND_PID
    exit 1
fi

# Hentikan backend
echo "8. Menghentikan backend..."
kill $BACKEND_PID
sleep 3

echo "=== Pengujian Fungsional Selesai ==="
echo "Semua pengujian berhasil! Sistem auto posting berfungsi dengan benar."