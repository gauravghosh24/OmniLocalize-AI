export type LanguageCode = "hi" | "ta" | "fr" | "de";
export interface LocalizeResult {
  language: string;
  language_code: LanguageCode;
  translated_text: string;
  text_file: string;
  audio_file: null;
  audio_error: string;
}

export interface LocalizeResponse {
  status: "success";
  results: LocalizeResult[];
}

export const LANGUAGE_OPTIONS: Array<{ code: LanguageCode; label: string; nativeName: string }> = [
  { code: "hi", label: "Hindi", nativeName: "हिन्दी" },
  { code: "ta", label: "Tamil", nativeName: "தமிழ்" },
  { code: "fr", label: "French", nativeName: "Français" },
  { code: "de", label: "German", nativeName: "Deutsch" },
];
