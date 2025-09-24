#!/bin/bash

# Skrip Pengujian Performance Telegram Userbot
echo "=== Memulai Pengujian Performance Telegram Userbot ==="

# Memulai backend
echo "1. Memulai backend..."
cd /workspaces/telegram-userbot/backend
TELEGRAM_API_ID=123456 TELEGRAM_API_HASH=test_hash PHONE_NUMBER=+1234567890 SESSION_STRING=test_session_string SECRET_KEY=test_secret_key_for_testing_purposes_only DATABASE_URL=sqlite+aiosqlite:///./test_telegram_bot.db NEXT_PUBLIC_API_URL=http://localhost:8000 uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/backend_performance.log 2>&1 &
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

# Pengujian waktu respons API
echo "4. Menguji waktu respons API..."
START_TIME=$(date +%s%3N)
curl -s http://localhost:8000/ > /dev/null
END_TIME=$(date +%s%3N)
RESPONSE_TIME=$((END_TIME - START_TIME))
if [[ $RESPONSE_TIME -lt 1000 ]]; then
    echo "✓ Waktu respons API baik (${RESPONSE_TIME}ms < 1000ms)"
else
    echo "✗ Waktu respons API lambat (${RESPONSE_TIME}ms >= 1000ms)"
fi

# Pengujian throughput dengan concurrent requests
echo "5. Menguji throughput dengan concurrent requests..."
CONCURRENT_REQUESTS=10
TIMEOUT=30

# Fungsi untuk mengirim request
send_request() {
    curl -s -w "%{time_total}" http://localhost:8000/ > /dev/null
}

# Kirim concurrent requests dan ukur waktu
echo "Mengirim $CONCURRENT_REQUESTS concurrent requests..."
START_TIME=$(date +%s%3N)
for i in $(seq 1 $CONCURRENT_REQUESTS); do
    send_request &
done
wait
END_TIME=$(date +%s%3N)
TOTAL_TIME=$((END_TIME - START_TIME))

echo "Total waktu untuk $CONCURRENT_REQUESTS requests: ${TOTAL_TIME}ms"
AVG_TIME=$((TOTAL_TIME / CONCURRENT_REQUESTS))
echo "Rata-rata waktu per request: ${AVG_TIME}ms"

if [[ $AVG_TIME -lt 500 ]]; then
    echo "✓ Throughput concurrent requests baik (rata-rata < 500ms)"
else
    echo "✗ Throughput concurrent requests lambat (rata-rata >= 500ms)"
fi

# Pengujian dengan banyak data
echo "6. Menguji performa dengan banyak data..."

# Tambahkan banyak grup
echo "Menambahkan 50 grup..."
for i in {1..50}; do
    curl -s -X POST http://localhost:8000/api/v1/groups -H "Content-Type: application/json" -d "{\"identifier\": \"@testgroup_$i\"}" > /dev/null
done

# Tambahkan banyak pesan
echo "Menambahkan 50 pesan..."
for i in {1..50}; do
    curl -s -X POST http://localhost:8000/api/v1/messages -H "Content-Type: application/json" -d "{\"text\": \"Test message $i for performance testing\"}" > /dev/null
done

# Ukur waktu untuk mengambil semua grup
echo "Mengukur waktu untuk mengambil semua grup..."
START_TIME=$(date +%s%3N)
GROUPS_RESPONSE=$(curl -s http://localhost:8000/api/v1/groups)
END_TIME=$(date +%s%3N)
GROUPS_FETCH_TIME=$((END_TIME - START_TIME))

GROUP_COUNT=$(echo "$GROUPS_RESPONSE" | grep -o "identifier" | wc -l)
echo "Jumlah grup: $GROUP_COUNT"
echo "Waktu mengambil semua grup: ${GROUPS_FETCH_TIME}ms"

if [[ $GROUPS_FETCH_TIME -lt 2000 ]]; then
    echo "✓ Performa pengambilan grup baik (< 2000ms untuk $GROUP_COUNT grup)"
else
    echo "✗ Performa pengambilan grup lambat (>= 2000ms untuk $GROUP_COUNT grup)"
fi

# Ukur waktu untuk mengambil semua pesan
echo "Mengukur waktu untuk mengambil semua pesan..."
START_TIME=$(date +%s%3N)
MESSAGES_RESPONSE=$(curl -s http://localhost:8000/api/v1/messages)
END_TIME=$(date +%s%3N)
MESSAGES_FETCH_TIME=$((END_TIME - START_TIME))

MESSAGE_COUNT=$(echo "$MESSAGES_RESPONSE" | grep -o "text" | wc -l)
echo "Jumlah pesan: $MESSAGE_COUNT"
echo "Waktu mengambil semua pesan: ${MESSAGES_FETCH_TIME}ms"

if [[ $MESSAGES_FETCH_TIME -lt 2000 ]]; then
    echo "✓ Performa pengambilan pesan baik (< 2000ms untuk $MESSAGE_COUNT pesan)"
else
    echo "✗ Performa pengambilan pesan lambat (>= 2000ms untuk $MESSAGE_COUNT pesan)"
fi

# Pengujian penghapusan batch
echo "7. Menguji penghapusan batch..."

# Ukur waktu untuk menghapus semua grup
echo "Mengukur waktu untuk menghapus semua grup..."
START_TIME=$(date +%s%3N)
# Kita tidak bisa menghapus semua grup sekaligus tanpa ID spesifik, jadi kita skip ini
END_TIME=$(date +%s%3N)
BATCH_DELETE_TIME=$((END_TIME - START_TIME))
echo "Penghapusan batch grup dilewati (tidak ada endpoint batch delete)"

# Hentikan backend
echo "8. Menghentikan backend..."
kill $BACKEND_PID
sleep 3

echo "=== Pengujian Performance Selesai ==="
echo "Pengujian performance selesai. Silakan periksa hasil di atas."