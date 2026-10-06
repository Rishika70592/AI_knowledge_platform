"use client";

import { FormEvent, useState } from "react";
import { API_URL } from "../../lib/api";
import Sidebar from "../../components/Sidebar";

export default function ChatPage() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!question.trim()) return;

    const token = localStorage.getItem("access_token");

    if (!token) {
      setAnswer("Please login first.");
      return;
    }

    setLoading(true);
    setAnswer("");

    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          question: question.trim(),
          top_k: 5,
        }),
      });

      if (!response.ok) {
        const error = await response.text();
        throw new Error(error || "Request failed");
      }

      if (!response.body) {
        throw new Error("Streaming is not supported by this response.");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let accumulated = "";

      while (true) {
        const { value, done } = await reader.read();

        if (done) break;

        const chunk = decoder.decode(value, {
          stream: true,
        });

        const lines = chunk.split("\n");

        for (const line of lines) {
          if (!line.startsWith("data:")) continue;

          const data = line.slice(5).trim();

          if (!data || data === "[DONE]") continue;

          accumulated += data;
          setAnswer(accumulated);
        }
      }
    } catch (error) {
      setAnswer(
        error instanceof Error
          ? `Error: ${error.message}`
          : "Something went wrong."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen bg-gray-50">
    <Sidebar />

    <main className="flex flex-1 flex-col">
      <header className="border-b bg-white px-6 py-4">
        <h1 className="text-xl font-bold">
          AI Knowledge Platform
        </h1>
      </header>

      <div className="mx-auto flex w-full max-w-4xl flex-1 flex-col p-6">
        <div className="mb-6 min-h-[500px] flex-1 overflow-y-auto rounded-2xl border bg-white p-6 shadow-sm">

          {!answer && !loading && (
            <div className="flex h-full items-center justify-center text-center text-gray-500">
              <div>
                <h2 className="mb-2 text-2xl font-semibold text-gray-800">
                  Ask your knowledge base
                </h2>

                <p>
                  Ask a question about your uploaded documents.
                </p>
              </div>
            </div>
          )}

          {answer && (
  <div className="w-full">
    <div className="mb-3 text-sm font-semibold text-gray-500">
      AI Answer
    </div>

    <div className="max-w-full overflow-hidden rounded-2xl bg-gray-100 p-5">
      <div className="whitespace-pre-wrap break-words text-[15px] leading-7 text-gray-800">
        {answer}
        {loading && (
          <span className="ml-1 inline-block animate-pulse">
            ▌
          </span>
        )}
      </div>
    </div>
  </div>
)}


        {loading && !answer && (
  <div className="mt-4 flex items-center gap-2 text-sm text-gray-500">
    <span className="h-2 w-2 animate-pulse rounded-full bg-gray-400" />
    AI is thinking...
  </div>
)}

        </div>

        <form
          onSubmit={handleSubmit}
          className="flex gap-3 rounded-2xl border bg-white p-3 shadow-sm"
        >
          <input
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Ask a question..."
            disabled={loading}
            className="flex-1 rounded-xl px-4 py-3 outline-none"
          />

          <button
            type="submit"
            disabled={loading || !question.trim()}
            className="rounded-xl bg-black px-6 py-3 font-medium text-white disabled:opacity-40"
          >
            {loading ? "Thinking..." : "Ask"}
          </button>
        </form>
      </div>
      
    </main>
     </div>
  );
}
