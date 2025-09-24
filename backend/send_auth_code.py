#!/usr/bin/env python3
"""
Script untuk menginisialisasi otentikasi Telegram dan mengirim kode
"""
import asyncio
import os
from dotenv import load_dotenv
from app.core.telegram_auth import TelegramAuth

# Load environment variables
load_dotenv()

async def initialize_and_send_code():
    """
    Fungsi untuk menginisialisasi otentikasi dan mengirim kode ke nomor telepon
    """
    try:
        # Ambil informasi dari environment variables atau dari input user
        api_id = os.environ.get("TELEGRAM_API_ID") or input("Enter your API ID: ")
        api_hash = os.environ.get("TELEGRAM_API_HASH") or input("Enter your API HASH: ")
        phone_number = os.environ.get("PHONE_NUMBER") or input("Enter your phone number: ")
        
        # Inisialisasi autentikasi
        auth = TelegramAuth(
            int(api_id),
            api_hash,
            phone_number,
        )

        # Mulai klien untuk mengirim kode
        await auth.start_client()

        # Kirim kode otentikasi
        phone_code_hash = await auth.send_code()

        print(f"Kode otentikasi telah dikirim ke {phone_number}")
        print(f"Phone code hash: {phone_code_hash}")

        # Kita tidak perlu menghentikan klien di sini jika kita ingin melanjutkan proses otentikasi
        # await auth.stop_client()

        return auth, phone_code_hash

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return None, None


if __name__ == "__main__":
    asyncio.run(initialize_and_send_code())