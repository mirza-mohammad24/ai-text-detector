import { useState } from "react";
import { AlertCircle, CheckCircle, Brain, Search, X} from 'lucide-react';
function App() {
  //State variables
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  //Connect with the python backend and post the user input and get back the result
  const handleAnalyze = async () => {
    //do post with empty text
    if (!text.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // The FETCH Request
      const response = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text }),
      });

      if (!response.ok) throw new Error("Backend Refused to Connect");

      const data = await response.json();

      //populate the result state if received anything from backend
      setResult(data);
    } catch (err) {
      setError("Check if the backend is up and serving!");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  //Highlighting the specific words flagged by Rabin-Karp
  const renderHighlightedText = () => {

    if (!result || !result.matches.length)
      return <p className="text-gray-600">{text}</p>;

    const regex = new RegExp(`(${result.matches.join("|")})`, "gi");
    const parts = text.split(regex);

    return (
      <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
        {parts.map((part, i) =>
          result.matches.some(
            (match) => match.toLowerCase() === part.toLowerCase()) ?
            (
            <span
              key={i}
              className="bg-red-200 text-red-800 font-bold px-1 rounded border border-red-300"
            >
              {part}
            </span>
            ) : 
            (part),
        )}
      </p>
    );
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans selection:bg-indigo-100 selection:text-indigo-700 pb-20">
      {/* HEADER */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Brain className="w-8 h-8 text-indigo-600" />
            <h1 className="text-xl font-bold bg-clip-text text-transparent bg-linear-to-r from-indigo-600 to-violet-600">
              AI Text Detector
            </h1>
          </div>
          <span className="text-xs font-medium px-3 py-1 bg-slate-100 rounded-full text-slate-500">
            Rabin-Karp Algorithm
          </span>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-10 grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* LEFT COLUMN: Input Section */}
        <section className="flex flex-col gap-4">
          <div className="bg-white p-1 rounded-2xl shadow-sm border border-slate-200 focus-within:ring-2 focus-within:ring-indigo-500 transition-all">
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Paste your text here to analyze..."
              className="w-full h-96 p-6 rounded-xl resize-none outline-none text-slate-700 placeholder:text-slate-400 text-lg leading-relaxed"
            />
          </div>

          <div className="flex items-center justify-between">
            <button
              onClick={() => {
                setText("");
                setResult(null);
              }}
              className="flex items-center gap-2 text-slate-500 hover:text-slate-700 transition-colors px-4 py-2"
            >
              <X className="w-4 h-4" /> Clear
            </button>

            <button
              onClick={handleAnalyze}
              disabled={loading || !text}
              className={`flex items-center gap-2 px-8 py-3 rounded-xl font-semibold text-white transition-all transform active:scale-95 shadow-lg shadow-indigo-200 ${
                loading || !text
                  ? "bg-slate-300 cursor-not-allowed shadow-none"
                  : "bg-indigo-600 hover:bg-indigo-700"
              }`}
            >
              {loading ? (
                <>Processing...</>
              ) : (
                <>
                  <Search className="w-5 h-5" /> Analyze Text
                </>
              )}
            </button>
          </div>

          {error && (
            <div className="flex items-center gap-3 p-4 bg-red-50 text-red-700 rounded-xl border border-red-100 animate-in fade-in slide-in-from-top-2">
              <AlertCircle className="w-5 h-5 shrink-0" />
              <p className="text-sm font-medium">{error}</p>
            </div>
          )}
        </section>

        {/* RIGHT COLUMN: Results Section */}
        <section className="relative">
          {result ? (
            <div className="flex flex-col gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
              {/* SCORE CARD */}
              <div
                className={`p-8 rounded-2xl border-2 flex flex-col items-center justify-center text-center shadow-sm ${
                  result.score > 50
                    ? "bg-red-50 border-red-100 text-red-900"
                    : "bg-emerald-50 border-emerald-100 text-emerald-900"
                }`}
              >
                <div className="text-sm font-bold tracking-wider opacity-70 mb-2 uppercase">
                  AI Likelihood Score
                </div>
                <div className="text-6xl font-black mb-4 tracking-tight">
                  {result.score}%
                </div>
                <div
                  className={`inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-sm font-bold ${
                    result.score > 50
                      ? "bg-red-200 text-red-800"
                      : "bg-emerald-200 text-emerald-800"
                  }`}
                >
                  {result.score > 50 ? (
                    <AlertCircle className="w-4 h-4" />
                  ) : (
                    <CheckCircle className="w-4 h-4" />
                  )}
                  {result.verdict}
                </div>
              </div>

              {/* DETAILED ANALYSIS */}
              <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden flex flex-col h-96">
                <div className="bg-slate-50 px-6 py-4 border-b border-slate-200 flex justify-between items-center">
                  <h3 className="font-bold text-slate-700">
                    Detailed Analysis
                  </h3>
                  <span className="text-xs bg-slate-200 text-slate-600 px-2 py-1 rounded">
                    {result.matches.length} Patterns Found
                  </span>
                </div>
                <div className="p-6 overflow-y-auto custom-scrollbar">
                  {renderHighlightedText()}
                </div>
              </div>
            </div>
          ) : (
            // EMPTY STATE PLACEHOLDER
            <div className="h-full flex flex-col items-center justify-center text-slate-400 border-2 border-dashed border-slate-200 rounded-2xl bg-slate-50/50">
              <Brain className="w-16 h-16 mb-4 opacity-20" />
              <p className="font-medium">Waiting for analysis...</p>
              <p className="text-sm opacity-60">Paste text and hit Analyze</p>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App