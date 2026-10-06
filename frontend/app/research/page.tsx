"use client";

import { FormEvent, useState } from "react";
import { API_URL } from "../../lib/api";
import Sidebar from "../../components/Sidebar";

interface ResearchResponse {
  question: string;
  answer: string;
}

export default function ResearchPage() {
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
      const response = await fetch(
        `${API_URL}/api/v1/agents/research`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            question: question.trim(),
          }),
        }
      );

      if (!response.ok) {
        const error = await response.text();
        throw new Error(error || "Research request failed");
      }

      const data: ResearchResponse = await response.json();

      setAnswer(data.answer || "No answer was returned.");
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

        {/* Header */}
        <header className="border-b bg-white px-6 py-4">
          <h1 className="text-xl font-bold">
            AI Knowledge Platform
          </h1>
        </header>

        {/* Main content */}
        <div className="mx-auto flex w-full max-w-4xl flex-1 flex-col p-6">

          {/* Answer area */}
          <div className="mb-6 min-h-[500px] flex-1 overflow-y-auto rounded-2xl border bg-white p-6 shadow-sm">

            {/* Empty state */}
            {!answer && !loading && (
              <div className="flex h-full items-center justify-center text-center text-gray-500">
                <div>
                  <h2 className="mb-2 text-2xl font-semibold text-gray-800">
                    AI Research Agent
                  </h2>

                  <p>
                    Ask a question and let the research agent find an answer.
                  </p>
                </div>
              </div>
            )}

            {/* Loading */}
            {loading && (
              <div className="flex items-center gap-2 text-sm text-gray-500">
                <span className="h-2 w-2 animate-pulse rounded-full bg-gray-400" />
                Researching...
              </div>
            )}

            {/* Answer */}
            {answer && (
              <div className="w-full">

                <div className="mb-3 text-sm font-semibold text-gray-500">
                  Research Result
                </div>

                <div className="mb-4 rounded-2xl bg-gray-100 p-5">
                  <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-gray-500">
                    Question
                  </div>

                  <div className="break-words text-[15px] leading-7 text-gray-800">
                    {question}
                  </div>
                </div>

                <div className="rounded-2xl bg-gray-100 p-5">
                  <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-gray-500">
                    AI Research Answer
                  </div>

                  <div className="whitespace-pre-wrap break-words text-[15px] leading-7 text-gray-800">
                    {answer}
                  </div>
                </div>

              </div>
            )}

          </div>

          {/* Research input */}
          <form
            onSubmit={handleSubmit}
            className="flex gap-3 rounded-2xl border bg-white p-3 shadow-sm"
          >
            <input
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="Ask a research question..."
              disabled={loading}
              className="flex-1 rounded-xl px-4 py-3 outline-none"
            />

            <button
              type="submit"
              disabled={loading || !question.trim()}
              className="rounded-xl bg-black px-6 py-3 font-medium text-white disabled:opacity-40"
            >
              {loading ? "Researching..." : "Research"}
            </button>
          </form>

        </div>
      </main>
    </div>
  );
}


