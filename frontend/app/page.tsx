"use client";

import { AlertCircle, Languages, LoaderCircle, Sparkles } from "lucide-react";
import { type FormEvent, useState } from "react";

import { LanguagePicker } from "@/components/language-picker";
import { ResultCard } from "@/components/result-card";
import { api } from "@/lib/api";
import { type LanguageCode, type LocalizeResponse, type LocalizeResult } from "@/lib/types";

const EXAMPLE_TEXT = "Artificial intelligence is helping teams make information more accessible across languages. A thoughtful localization workflow keeps the original meaning intact while giving every audience a natural way to read and listen.";

export default function Home() {
  const [text, setText] = useState("");
  const [languages, setLanguages] = useState<LanguageCode[]>(["hi", "ta", "fr", "de"]);
  const [results, setResults] = useState<LocalizeResult[]>([]);
  const [error, setError] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setResults([]);
    if (!text.trim()) {
      setError("Add the English text you want to translate.");
      return;
    }
    if (!languages.length) {
      setError("Choose at least one target language.");
      return;
    }

    setIsGenerating(true);
    try {
      const response = await api.post<LocalizeResponse>("/api/localize", {
        text,
        target_languages: languages,
      });
      setResults(response.data.results);
    } catch (requestError) {
      const detail = requestError && typeof requestError === "object" && "response" in requestError
        ? (requestError as { response?: { data?: { detail?: string } } }).response?.data?.detail
        : undefined;
      setError(detail ?? "Could not reach the local translation backend. Confirm it is running at http://localhost:8000.");
    } finally {
      setIsGenerating(false);
    }
  }

  return (
    <main className="mx-auto min-h-screen max-w-7xl px-4 py-8 sm:px-7 lg:px-10 lg:py-12">
      <header className="mb-10 flex flex-col justify-between gap-6 border-b border-white/10 pb-7 sm:flex-row sm:items-end">
        <div>
          <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-indigo-300/20 bg-indigo-300/10 px-3 py-1 text-xs font-semibold tracking-wide text-indigo-200"><Sparkles size={13} /> LOCAL AI WORKSPACE</div>
          <h1 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">OmniLocalize AI</h1>
          <p className="mt-2 max-w-xl text-sm leading-6 text-slate-400 sm:text-base">Local multilingual text translation engine for Indian and European languages</p>
        </div>
        <div className="flex items-center gap-2 text-xs text-slate-400"><span className="h-2 w-2 rounded-full bg-emerald-400 shadow-[0_0_12px_2px_rgba(74,222,128,0.45)]" /> Runs entirely on your machine</div>
      </header>

      <section className="grid gap-7 lg:grid-cols-[minmax(0,1.55fr)_minmax(300px,0.8fr)]">
        <form className="rounded-2xl border border-white/10 bg-slate-950/55 p-5 shadow-2xl shadow-black/20 backdrop-blur sm:p-7" onSubmit={submit}>
          <div className="mb-4 flex items-center justify-between gap-3">
            <label className="flex items-center gap-2 text-sm font-semibold text-white" htmlFor="source-text"><Languages className="text-indigo-300" size={17} /> English source text</label>
            <span className="text-xs text-slate-500">{wordCount.toLocaleString()} words</span>
          </div>
          <textarea className="min-h-72 w-full resize-y rounded-xl border border-white/10 bg-black/20 p-4 text-sm leading-7 text-slate-200 outline-none transition placeholder:text-slate-600 focus:border-indigo-400/70 focus:ring-4 focus:ring-indigo-400/10" disabled={isGenerating} id="source-text" maxLength={50000} onChange={(event) => setText(event.target.value)} placeholder="Paste an article, product update, lesson, or story in English..." value={text} />
          <button className="mt-3 text-xs font-medium text-indigo-300 transition hover:text-indigo-200 disabled:opacity-50" disabled={isGenerating} onClick={() => setText(EXAMPLE_TEXT)} type="button">Use a short example</button>

          <div className="mt-7 border-t border-white/8 pt-6">
            <p className="mb-3 text-sm font-semibold text-white">Target languages</p>
            <LanguagePicker disabled={isGenerating} onChange={setLanguages} selected={languages} />
          </div>
          {error && <div className="mt-6 flex gap-3 rounded-xl border border-rose-400/30 bg-rose-400/10 p-4 text-sm text-rose-100"><AlertCircle className="mt-0.5 shrink-0" size={17} /><p>{error}</p></div>}
          <button className="mt-7 flex w-full items-center justify-center gap-2 rounded-xl bg-indigo-400 px-5 py-3.5 text-sm font-bold text-slate-950 transition hover:bg-indigo-300 disabled:cursor-not-allowed disabled:bg-slate-600 disabled:text-slate-300" disabled={isGenerating} type="submit">
            {isGenerating && <LoaderCircle className="animate-spin" size={18} />}
            {isGenerating ? "Translating Content..." : "Translate Content"}
          </button>
          <p className="mt-3 text-center text-xs text-slate-500">Text-only translation in Version 1.</p>
        </form>

        <aside className="rounded-2xl border border-white/10 bg-white/[0.025] p-6 sm:p-7">
          <p className="text-xs font-bold tracking-[0.2em] text-indigo-300">PIPELINE</p>
          <h2 className="mt-3 text-xl font-semibold text-white">From English to local text.</h2>
          <p className="mt-3 text-sm leading-6 text-slate-400">Your text never leaves this computer. Translation runs through a locally downloaded open-source model.</p>
          <ol className="mt-7 space-y-5">
            {[["01", "Clean & split", "Sentence-aware chunks preserve meaning in long text."], ["02", "Translate", "NLLB creates natural-language translations for each locale."], ["03", "Read and copy", "Review each translation and copy it wherever you need it."]].map(([number, title, description]) => (
              <li className="flex gap-4" key={number}><span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-indigo-400/10 text-xs font-bold text-indigo-200">{number}</span><div><p className="text-sm font-semibold text-slate-200">{title}</p><p className="mt-1 text-xs leading-5 text-slate-500">{description}</p></div></li>
            ))}
          </ol>
        </aside>
      </section>

      {isGenerating && <section className="mt-10 rounded-2xl border border-indigo-300/20 bg-indigo-300/[0.06] p-5 text-sm text-indigo-100"><div className="flex items-center gap-3"><LoaderCircle className="animate-spin" size={18} /><p className="font-semibold">Translating your content. First run may take some time while the model loads.</p></div></section>}

      {results.length > 0 && <section className="mt-10"><div className="mb-5 flex items-end justify-between"><div><p className="text-xs font-bold tracking-[0.2em] text-indigo-300">OUTPUTS</p><h2 className="mt-2 text-2xl font-semibold text-white">Your translated text</h2></div><p className="text-sm text-slate-500">{results.length} complete</p></div><div className="grid gap-5 xl:grid-cols-2">{results.map((result) => <ResultCard key={result.language_code} result={result} />)}</div></section>}
    </main>
  );
}
