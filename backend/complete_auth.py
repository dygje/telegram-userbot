#!/usr/bin/env python3
"""
Script untuk menyelesaikan proses otentikasi Telegram menggunakan kode yang dikirim
"""
import asyncio
import os
from pyrogram import Client

async def complete_authentication():
    """
    Fungsi untuk menyelesaikan otentikasi dengan kode yang telah dikirim
    """
    try:
        # Ambil informasi dari environment variables atau dari input user
        api_id = os.environ.get("TELEGRAM_API_ID") or input("Enter your API ID: ")
        api_hash = os.environ.get("TELEGRAM_API_HASH") or input("Enter your API HASH: ")
        phone_number = os.environ.get("PHONE_NUMBER") or input("Enter your phone number: ")
        
        # Buat klien Pyrogram dengan nomor telepon
        client = Client(
            "new_session",
            api_id=int(api_id),
            api_hash=api_hash,
            phone_number=phone_number,
        )

        # Hubungkan ke Telegram
        await client.connect()

        # Kirim kode otentikasi
        sent_code = await client.send_code(phone_number)
        phone_code_hash = sent_code.phone_code_hash
        print(f"Kode otentikasi telah dikirim ke {phone_number}")
        print(f"Phone code hash: {phone_code_hash}")

        # Masukkan kode yang diterima di aplikasi Telegram
        phone_code = input("Enter the code you received: ")

        # Verifikasi kode otentikasi
        me = await client.sign_in(
            phone_number, phone_code_hash, phone_code
        )

        print(
            f"Berhasil masuk sebagai: {me.first_name} (@{me.username if me.username else 'N/A'})"
        )

        # Dapatkan session string
        session_string = await client.export_session_string()
        print(f"Session string: {session_string}")

        # Simpan session string ke file
        with open("session.txt", "w") as f:
            f.write(session_string)

        print("Session string telah disimpan ke file session.txt")

        await client.disconnect()

        return session_string

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        # Jika terjadi error karena kode salah, kita perlu menangani khusus
        if "PHONE_CODE_INVALID" in str(e).upper():
            print("Kode otentikasi yang dimasukkan salah. Silakan coba lagi.")
        elif "PHONE_CODE_EXPIRED" in str(e).upper():
            print("Kode otentikasi telah kedaluwarsa. Harap kirim kode baru.")
        return None


if __name__ == "__main__":
    asyncio.run(complete_authentication())