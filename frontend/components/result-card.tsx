"use client";

import { Check, Clipboard, Download, FileText } from "lucide-react";
import { useState } from "react";

import { downloadUrl } from "@/lib/api";
import type { LocalizeResult } from "@/lib/types";

export function ResultCard({ result }: { result: LocalizeResult }) {
  const [copied, setCopied] = useState(false);

  async function copyText() {
    await navigator.clipboard.writeText(result.translated_text);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1800);
  }

  return (
    <article className="overflow-hidden rounded-2xl border border-white/10 bg-slate-950/50 shadow-2xl shadow-black/15 backdrop-blur">
      <header className="flex items-center justify-between border-b border-white/8 px-5 py-4">
        <div className="flex gap-2">
          <p className="text-base font-semibold text-white">{result.language}</p>
          <p className="text-xs uppercase tracking-[0.18em] text-indigo-300">{result.language_code}</p>
        </div>
        <span className="rounded-full border border-emerald-300/20 bg-emerald-300/10 px-2.5 py-1 text-xs font-medium text-emerald-200">Complete</span>
      </header>
      <div className="space-y-4 p-5">
        <div className="max-h-56 overflow-y-auto rounded-xl border border-white/8 bg-black/20 p-4 text-sm leading-7 whitespace-pre-wrap text-slate-300">
          {result.translated_text}
        </div>
        <div>
          <button className="inline-flex items-center justify-center gap-1.5 rounded-lg border border-white/10 bg-white/[0.04] px-2 py-2.5 text-xs font-medium text-slate-200 transition hover:bg-white/[0.1]" onClick={copyText} type="button">
            {copied ? <Check className="text-emerald-300" size={14} /> : <Clipboard size={14} />}
            {copied ? "Copied" : "Copy"}
          </button>
          <a className="inline-flex items-center justify-center gap-1.5 rounded-lg border border-white/10 bg-white/[0.04] px-2 py-2.5 text-xs font-medium text-slate-200 transition hover:bg-white/[0.1]" download={result.text_file} href={downloadUrl("text", result.text_file)}>
            <FileText size={14} /> Text <Download size={13} />
          </a>
        </div>
      </div>
    </article>
  );
}
