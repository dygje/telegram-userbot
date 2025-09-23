// Type definitions for Telegram Userbot TMA

export interface Group {
  id: number;
  identifier: string;
  name: string;
}

export interface Message {
  id: number;
  text: string;
}

export interface BlacklistedChat {
  id: number;
  chat_id: string;
  reason: string;
  is_permanent: boolean;
  expiry_time: string | null;
}

export interface Config {
  id: number;
  key: string;
  value: string;
  description: string;
}

export interface UserbotStatus {
  running: boolean;
  user_info: {
    id: number;
    username: string;
    first_name: string;
    last_name: string;
    phone_number: string;
  } | null;
  message: string;
}

export interface AuthResponse {
  phone_code_hash: string;
}

export interface ApiResponse<T> {
  message: string;
  data?: T;
}