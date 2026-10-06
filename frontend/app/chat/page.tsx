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

    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || loading) {
      return;
    }

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
          Accept: "text/event-stream",
        },
        body: JSON.stringify({
          question: trimmedQuestion,
          top_k: 5,
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();

        let errorMessage = "Request failed.";

        try {
          const errorData = JSON.parse(errorText);

          errorMessage =
            errorData?.detail ||
            errorData?.message ||
            errorData?.error ||
            errorMessage;
        } catch {
          if (errorText) {
            errorMessage = errorText;
          }
        }

        throw new Error(errorMessage);
      }

      if (!response.body) {
        throw new Error("The server returned an empty response.");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");

      let accumulated = "";
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();

        if (done) {
          break;
        }

        buffer += decoder.decode(value, {
          stream: true,
        });

        /*
         * SSE data is line based.
         *
         * Keep the last incomplete line in `buffer`.
         * This is important because a network chunk can split
         * anywhere, even in the middle of a line.
         */
        const lines = buffer.split(/\r?\n/);

        buffer = lines.pop() ?? "";

        for (const line of lines) {
          if (!line.startsWith("data:")) {
            continue;
          }

          /*
           * SSE normally uses:
           *
           * data: hello
           *
           * We remove ONLY the `data:` prefix and ONE optional
           * separator space.
           *
           * We deliberately DO NOT use `.trim()`.
           */
          let data = line.slice(5);

          if (data.startsWith(" ")) {
            data = data.slice(1);
          }

          if (data === "[DONE]") {
            continue;
          }

          /*
           * If the backend sends JSON strings, decode them.
           * Otherwise use the text directly.
           */
          try {
            const parsed = JSON.parse(data);

            if (typeof parsed === "string") {
              data = parsed;
            } else if (parsed?.answer) {
              data = parsed.answer;
            } else if (parsed?.content) {
              data = parsed.content;
            }
          } catch {
            // Normal text. Nothing to do.
          }

          if (!data) {
            continue;
          }

          accumulated += data;
          setAnswer(accumulated);
        }
      }

      /*
       * Flush the TextDecoder.
       */
      buffer += decoder.decode();

      /*
       * Process a final SSE line if one exists.
       */
      if (buffer.startsWith("data:")) {
        let data = buffer.slice(5);

        if (data.startsWith(" ")) {
          data = data.slice(1);
        }

        if (data && data !== "[DONE]") {
          try {
            const parsed = JSON.parse(data);

            if (typeof parsed === "string") {
              data = parsed;
            } else if (parsed?.answer) {
              data = parsed.answer;
            } else if (parsed?.content) {
              data = parsed.content;
            }
          } catch {
            // Normal text.
          }

          accumulated += data;
          setAnswer(accumulated);
        }
      }

      if (!accumulated) {
        setAnswer("The server returned an empty answer.");
      }
    } catch (error) {
      console.error("ASK ERROR:", error);

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
              type="text"
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="Ask a question..."
              disabled={loading}
              className="flex-1 rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-black"
            />

            <button
              type="submit"
              disabled={loading || !question.trim()}
              className="rounded-xl bg-black px-6 py-3 font-medium text-white disabled:cursor-not-allowed disabled:opacity-40"
            >
              {loading ? "Thinking..." : "Ask"}
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}
