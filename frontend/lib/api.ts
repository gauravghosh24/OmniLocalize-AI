import axios from "axios";

export const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15 * 60 * 1000,
});

export function downloadUrl(type: "text" | "audio", filename: string): string {
  return `${API_BASE_URL}/api/download/${type}/${encodeURIComponent(filename)}`;
}

export function audioPreviewUrl(filename: string): string {
  return `${API_BASE_URL}/api/preview/audio/${encodeURIComponent(filename)}`;
}
