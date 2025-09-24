#!/usr/bin/env python3
"""
Script untuk menyelesaikan proses otentikasi Telegram lengkap termasuk 2FA
"""
import asyncio
import os
from pyrogram import Client

async def complete_authentication_with_2fa():
    """
    Fungsi untuk menyelesaikan otentikasi dengan kode dan 2FA jika diperlukan
    """
    # Ambil informasi dari environment variables atau dari input user
    api_id = os.environ.get("TELEGRAM_API_ID") or input("Enter your API ID: ")
    api_hash = os.environ.get("TELEGRAM_API_HASH") or input("Enter your API HASH: ")
    phone_number = os.environ.get("PHONE_NUMBER") or input("Enter your phone number: ")
    
    try:
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

        # Masukkan kode yang diterima di aplikasi Telegram
        phone_code = input("Enter the code you received: ")

        try:
            # Coba masuk dengan kode otentikasi
            me = await client.sign_in(phone_number, phone_code_hash, phone_code)
            
            print(f"Berhasil masuk sebagai: {me.first_name} (@{me.username if me.username else 'N/A'})")
            
        except Exception as e:
            # Jika gagal, cek apakah perlu 2FA
            if "SESSION_PASSWORD_NEEDED" in str(e).upper():
                print("Diperlukan otentikasi 2FA")
                
                # Masukkan password 2FA
                password_2fa = input("Enter your 2FA password: ")
                
                # Verifikasi dengan password 2FA
                me = await client.check_password(password_2fa)
                
                print(f"Berhasil masuk dengan 2FA sebagai: {me.first_name} (@{me.username if me.username else 'N/A'})")
            else:
                raise e

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
        return None

if __name__ == "__main__":
    asyncio.run(complete_authentication_with_2fa())
