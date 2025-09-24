#!/usr/bin/env python3
"""
Script untuk proses otentikasi Telegram lengkap
"""
import asyncio
import os
from pyrogram import Client

async def authenticate_telegram():
    """
    Fungsi untuk melakukan otentikasi Telegram dari awal
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

        # Mulai klien - ini akan mengirim kode otentikasi
        await client.start()

        print(f"Kode otentikasi telah dikirim ke {phone_number}")

        # Ambil informasi pengguna setelah otentikasi
        me = await client.get_me()
        print(
            f"Berhasil masuk sebagai: {me.first_name} (@{me.username if me.username else 'N/A'})"
        )

        # Dapatkan session string untuk digunakan nanti
        session_string = await client.export_session_string()
        print(f"Session string: {session_string}")

        # Simpan session string ke file atau environment untuk digunakan nanti
        with open("session.txt", "w") as f:
            f.write(session_string)

        # Jangan hentikan klien jika ingin melanjutkan menggunakan sesi ini
        # await client.stop()

        return client, session_string

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return None, None


if __name__ == "__main__":
    asyncio.run(authenticate_telegram())