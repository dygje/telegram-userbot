# Sistem Auto Posting Telegram – Userbot MTProto - Qwen Code Context

## FUNGSI UTAMA WAJIB

### 1. Otentikasi (WAJIB)
- Harus menggunakan akun pengguna asli (non-bot)
- Harus terhubung ke server Telegram melalui MTProto API
- Proses login wajib memakai nomor telepon dan OTP
- Jika 2FA diaktifkan, sistem wajib mendukung input kata sandi 2FA
- TMA wajib menyediakan form setup awal untuk memasukkan dan memperbarui:
  • Telegram API ID
  • Telegram API Hash
  • Nomor telepon Telegram
- Data ini harus disimpan dalam bentuk terenkripsi, hanya dapat diakses/diubah oleh Admin/Superuser
- Perubahan harus memicu reload sesi otomatis tanpa menghentikan sistem

### 2. Manajemen Grup (WAJIB)
- Harus dikelola melalui TMA (Telegram Management Application)
- Developer wajib menyediakan fitur tambah, edit, dan hapus daftar grup
- Format grup yang wajib didukung:
  • Link grup: t.me/groupname
  • Username: @groupname
  • ID grup: -100xxxxxxxxxx
- Sistem harus memungkinkan penambahan banyak grup sekaligus (satu grup per baris)

### 3. Manajemen Pesan (WAJIB)
- Harus dikelola melalui TMA
- Pengguna harus dapat membuat, mengedit, dan menghapus daftar pesan
- Pesan yang dikirim wajib dalam format teks murni tanpa media

### 4. Konfigurasi (WAJIB)
- Semua pengaturan (jeda pesan, jeda siklus, dsb.) harus dapat diubah real-time melalui TMA
- Perubahan konfigurasi harus berlaku tanpa menghentikan sistem
- Perubahan API ID, API Hash, atau nomor telepon melalui TMA harus memicu proses login ulang dan reload sesi secara otomatis

### 5. Pengiriman Pesan Otomatis (WAJIB)
- Sistem hanya boleh mengirim pesan ke grup yang tidak masuk blacklist
- Wajib melakukan pembersihan blacklist sementara di awal setiap siklus
- Harus mengirim pesan teks sesuai daftar pesan yang disiapkan
- Wajib menerapkan jeda acak 5–10 detik antar pesan
- Wajib menerapkan jeda acak 1,1–1,3 jam antar siklus

### 6. Manajemen Blacklist Otomatis (WAJIB)
- Sistem wajib menambahkan ke blacklist permanen bila terjadi kesalahan:
  ChatForbidden, ChatIdInvalid, UserBlocked, PeerIdInvalid,
  ChannelInvalid, UserBannedInChannel, ChatWriteForbidden, ChatRestricted
- Sistem wajib menambahkan ke blacklist sementara bila terjadi:
  • SlowModeWait: catat durasi slow mode dan lewati grup
  • FloodWait: catat durasi tunggu dari Telegram dan lanjutkan setelah selesai
- Blacklist sementara harus dihapus otomatis setelah durasi berakhir
- Pembersihan blacklist sementara harus dijalankan di awal setiap siklus

### 7. Praktik Modern & Pemeliharaan (WAJIB)
- Kode harus mengikuti Clean Architecture dan Python modern (async, typing, dataclass, Pydantic)
- Harus menerapkan linting, formatting, desain modular, dan pengujian menyeluruh
- Harus mengenkripsi kredensial, mengisolasi sesi, dan menyimpan audit log
- Wajib memiliki mekanisme retry, graceful shutdown, monitoring, dan fallback strategy
- Harus mendukung Docker, prinsip 12-Factor App, dan pipeline CI/CD
- Antarmuka TMA wajib responsif, mendukung status real-time, role-based access, dan mode gelap

## Alur Kerja Wajib
1. Setup awal: input API ID, API Hash, dan nomor telepon melalui TMA
2. Otentikasi akun pengguna dengan OTP (dan 2FA bila ada)
3. Pengaturan daftar grup melalui TMA
4. Pembuatan dan pengaturan pesan melalui TMA
5. Konfigurasi pengaturan pengiriman
6. Pengiriman pesan otomatis sesuai jadwal
7. Manajemen blacklist otomatis selama proses
8. Pemeliharaan dan pemantauan sistem

## Stack Teknologi Wajib
- Backend: Python 3.11+ menggunakan PyroFork (MTProto client) dan FastAPI sebagai framework backend/TMA API
- Frontend (TMA Web UI): React + TypeScript dengan Next.js dan Tailwind CSS untuk antarmuka web responsif dan real-time

## Project Structure
```
telegram-userbot/
├── .github/                 # GitHub configurations (workflows, templates)
├── backend/                 # Backend source code
│   ├── alembic/             # Database migrations
│   ├── app/                 # Main application code
│   │   ├── api/             # API routes and endpoints
│   │   ├── core/            # Core application logic
│   │   ├── models/          # Database models
│   │   ├── schemas/         # Pydantic schemas for validation
│   │   ├── services/        # Business logic services
│   │   ├── utils/           # Utility functions
│   │   ├── __init__.py      # Package initializer
│   │   └── main.py          # Application entry point
│   ├── tests/               # Unit and integration tests
│   ├── alembic.ini          # Alembic configuration
│   └── requirements.txt     # Python dependencies
├── docs/                    # Documentation files
│   ├── CHANGELOG.md         # Changelog
│   ├── CODE_OF_CONDUCT.md   # Code of conduct
│   ├── CONTRIBUTING.md      # Contribution guidelines
│   ├── DEVELOPMENT.md       # Development guidelines
│   ├── DOCUMENTATION.md     # Detailed documentation
│   ├── PRODUCTION.md        # Production deployment guide
│   └── SECURITY.md          # Security guidelines
├── frontend/                # Frontend source code
│   ├── pages/               # Page components (Next.js pages)
│   ├── styles/              # Global styles
│   ├── package.json         # Node.js dependencies and scripts
│   └── ...                  # Other frontend configuration files
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile               # Docker configuration for backend
├── .env.example             # Example environment variables
├── .gitignore               # Git ignore patterns
├── LICENSE                  # License file
├── QWEN.md                  # Qwen Code CLI context
├── README.md                # Project documentation
└── ...                      # Other project files
```

## Development Guidelines

### Backend Development
- Language: Python 3.11+
- MTProto Client: PyroFork
- Backend Framework: FastAPI
- API: Telegram MTProto API
- Session Management: Encrypted session storage
- Event System: PyroFork event handlers
- Database: SQLite (local) or PostgreSQL (production)
- Authentication: JWT for TMA

### Frontend Development
- Framework: React + TypeScript + Next.js
- Styling: Tailwind CSS
- UI Components: Responsive and real-time
- Access Control: Role-based access
- Theme: Dark mode support

### Security Practices
- Store API credentials in encrypted form
- Never commit sensitive data to the repository
- Use secure session storage for persistent login
- Validate all user inputs and event data
- Implement role-based access control (RBAC)
- Use HTTPS for all communications

### AI Assistance Instructions

### Code Generation Preferences
- Generate idiomatic Python code following PyroFork and FastAPI patterns
- Generate React components with TypeScript and Tailwind CSS
- Include comprehensive error handling and logging
- Provide clear comments for complex logic
- Use type hints consistently
- Follow Clean Architecture principles

### Explanation Style
- Provide detailed explanations with code examples
- Link to relevant PyroFork, FastAPI, React, and Next.js documentation
- Explain both the "how" and "why" of implementations
- Include best practices and security considerations
- Reference Clean Architecture patterns

### Focus Areas
1. Telegram MTProto API integration with PyroFork
2. FastAPI backend development for TMA
3. React frontend development with Next.js
4. Clean Architecture implementation
5. Security best practices for userbots
6. Docker deployment and 12-Factor App principles
7. Automated blacklist management
8. Session management and authentication
9. Real-time status updates in TMA Web UI

## Environment Variables
The following environment variables are required:
- `TELEGRAM_API_ID`: Telegram API ID
- `TELEGRAM_API_HASH`: Telegram API Hash
- `PHONE_NUMBER`: User's phone number (first run only)
- `SESSION_STRING`: Persistent session string (after run)
- `SECRET_KEY`: Secret key for JWT authentication
- `DATABASE_URL`: Database connection string (SQLite/PostgreSQL)

## Tools and Dependencies
- pyrofork: MTProto client library
- fastapi: Backend framework
- react: Frontend library
- next.js: React framework
- tailwindcss: CSS framework
- python-dotenv: Environment variable management
- pytest: Testing framework
- black: Code formatting
- flake8: Linting
- mypy: Type checking

## Git Workflow
- Branch naming: feature/feature-name or bugfix/issue-name
- Commit format: type(scope): description
- Pull requests required for all changes
- Code review mandatory for core functionality