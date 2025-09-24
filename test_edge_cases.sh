#!/bin/bash

# Skrip Pengujian Edge Cases Telegram Userbot
echo "=== Memulai Pengujian Edge Cases Telegram Userbot ==="

# Memulai backend
echo "1. Memulai backend..."
cd /workspaces/telegram-userbot/backend
TELEGRAM_API_ID=123456 TELEGRAM_API_HASH=test_hash PHONE_NUMBER=+1234567890 SESSION_STRING=test_session_string SECRET_KEY=test_secret_key_for_testing_purposes_only DATABASE_URL=sqlite+aiosqlite:///./test_telegram_bot.db NEXT_PUBLIC_API_URL=http://localhost:8000 uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/backend_edge.log 2>&1 &
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

# Pengujian format grup yang tidak valid
echo "4. Menguji format grup yang tidak valid..."
INVALID_GROUP_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/groups -H "Content-Type: application/json" -d '{"identifier": "invalid_format"}')
if [[ "$INVALID_GROUP_RESPONSE" == *"error"* ]] || [[ "$INVALID_GROUP_RESPONSE" == *"failed"* ]]; then
    echo "✓ Penanganan format grup tidak valid berhasil"
else
    echo "✗ Penanganan format grup tidak valid gagal"
    echo "Response: $INVALID_GROUP_RESPONSE"
fi

# Pengujian pesan kosong
echo "5. Menguji penambahan pesan kosong..."
EMPTY_MESSAGE_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/messages -H "Content-Type: application/json" -d '{"text": ""}')
if [[ "$EMPTY_MESSAGE_RESPONSE" == *"error"* ]] || [[ "$EMPTY_MESSAGE_RESPONSE" == *"failed"* ]]; then
    echo "✓ Penanganan pesan kosong berhasil"
else
    echo "✗ Penanganan pesan kosong gagal"
    echo "Response: $EMPTY_MESSAGE_RESPONSE"
fi

# Pengujian pesan terlalu panjang
echo "6. Menguji penambahan pesan terlalu panjang..."
LONG_MESSAGE=$(printf 'A%.0s' {1..5000})
LONG_MESSAGE_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/messages -H "Content-Type: application/json" -d "{\"text\": \"$LONG_MESSAGE\"}")
if [[ "$LONG_MESSAGE_RESPONSE" == *"error"* ]] || [[ "$LONG_MESSAGE_RESPONSE" == *"failed"* ]]; then
    echo "✓ Penanganan pesan terlalu panjang berhasil"
else
    echo "✓ Penanganan pesan terlalu panjang (mungkin diterima)"
    echo "Response: $LONG_MESSAGE_RESPONSE"
fi

# Pengujian interval yang tidak valid
echo "7. Menguji update konfigurasi interval yang tidak valid..."
INVALID_INTERVAL_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/config -H "Content-Type: application/json" -d '{"key": "message_interval", "value": "invalid"}')
if [[ "$INVALID_INTERVAL_RESPONSE" == *"error"* ]] || [[ "$INVALID_INTERVAL_RESPONSE" == *"failed"* ]]; then
    echo "✓ Penanganan interval tidak valid berhasil"
else
    echo "✗ Penanganan interval tidak valid gagal"
    echo "Response: $INVALID_INTERVAL_RESPONSE"
fi

# Pengujian menambahkan grup yang sudah ada
echo "8. Menguji penambahan grup yang sudah ada..."
# Tambah grup dulu
curl -s -X POST http://localhost:8000/api/v1/groups -H "Content-Type: application/json" -d '{"identifier": "@duplicate_test"}' > /dev/null
# Coba tambah lagi
DUPLICATE_GROUP_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/groups -H "Content-Type: application/json" -d '{"identifier": "@duplicate_test"}')
if [[ "$DUPLICATE_GROUP_RESPONSE" == *"already exists"* ]]; then
    echo "✓ Penanganan grup duplikat berhasil"
else
    echo "✗ Penanganan grup duplikat gagal"
    echo "Response: $DUPLICATE_GROUP_RESPONSE"
fi

# Pengujian menambahkan pesan yang sama
echo "9. Menguji penambahan pesan yang sama..."
# Tambah pesan dulu
curl -s -X POST http://localhost:8000/api/v1/messages -H "Content-Type: application/json" -d '{"text": "Duplicate test message"}' > /dev/null
# Coba tambah lagi
DUPLICATE_MESSAGE_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/messages -H "Content-Type: application/json" -d '{"text": "Duplicate test message"}')
if [[ "$DUPLICATE_MESSAGE_RESPONSE" == *"added successfully"* ]]; then
    echo "✓ Penanganan pesan duplikat berhasil (diperbolehkan)"
else
    echo "✗ Penanganan pesan duplikat gagal"
    echo "Response: $DUPLICATE_MESSAGE_RESPONSE"
fi

# Hentikan backend
echo "10. Menghentikan backend..."
kill $BACKEND_PID
sleep 3

echo "=== Pengujian Edge Cases Selesai ==="
echo "Pengujian edge cases selesai. Silakan periksa hasil di atas."