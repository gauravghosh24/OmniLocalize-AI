import { Check } from "lucide-react";

import { LANGUAGE_OPTIONS, type LanguageCode } from "@/lib/types";

interface LanguagePickerProps {
  selected: LanguageCode[];
  onChange: (languages: LanguageCode[]) => void;
  disabled?: boolean;
}

export function LanguagePicker({ selected, onChange, disabled = false }: LanguagePickerProps) {
  function toggle(language: LanguageCode) {
    onChange(selected.includes(language) ? selected.filter((item) => item !== language) : [...selected, language]);
  }

  return (
    <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
      {LANGUAGE_OPTIONS.map((language) => {
        const isSelected = selected.includes(language.code);
        return (
          <button
            className={`rounded-xl border px-3 py-3 text-left transition ${
              isSelected
                ? "border-indigo-400/70 bg-indigo-400/10 text-white"
                : "border-white/10 bg-white/[0.03] text-slate-300 hover:border-white/25 hover:bg-white/[0.06]"
            } disabled:cursor-not-allowed disabled:opacity-50`}
            disabled={disabled}
            key={language.code}
            onClick={() => toggle(language.code)}
            type="button"
          >
            <span className="flex items-center justify-between text-sm font-semibold">
              {language.label}
              <span className={`flex h-5 w-5 items-center justify-center rounded-full ${isSelected ? "bg-indigo-400 text-slate-950" : "border border-white/20"}`}>
                {isSelected && <Check size={13} strokeWidth={3} />}
              </span>
            </span>
            <span className="mt-1 block text-xs text-slate-500">{language.nativeName}</span>
          </button>
        );
      })}
    </div>
  );
}
