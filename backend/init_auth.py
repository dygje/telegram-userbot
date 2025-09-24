#!/usr/bin/env python3
"""
Script untuk inisialisasi otentikasi Telegram
"""
import asyncio
import os
from pyrogram import Client

async def send_auth_code():
    """
    Fungsi untuk mengirim kode otentikasi ke nomor telepon
    """
    # Ambil informasi dari environment variables atau dari input user
    api_id = os.environ.get("TELEGRAM_API_ID") or input("Enter your API ID: ")
    api_hash = os.environ.get("TELEGRAM_API_HASH") or input("Enter your API HASH: ")
    phone_number = os.environ.get("PHONE_NUMBER") or input("Enter your phone number: ")
    
    # Buat klien Pyrogram dengan nomor telepon
    client = Client(
        "new_session",
        api_id=int(api_id),
        api_hash=api_hash,
        phone_number=phone_number
    )

    # Hubungkan ke Telegram
    await client.connect()
    
    # Kirim kode otentikasi
    sent_code = await client.send_code(phone_number)
    phone_code_hash = sent_code.phone_code_hash
    print(f"Kode otentikasi telah dikirim ke {phone_number}")
    print(f"Phone code hash: {phone_code_hash}")

    await client.disconnect()

    return phone_code_hash

if __name__ == "__main__":
    asyncio.run(send_auth_code())
