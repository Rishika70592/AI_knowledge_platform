"use client";

import { useEffect, useState } from "react";
import Sidebar from "../../components/Sidebar";
import { API_URL } from "../../lib/api";

type Chat = {
  id?: string;
  question?: string;
  answer?: string;
  created_at?: string;
};

export default function HistoryPage() {
  const [chats, setChats] = useState<Chat[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadHistory() {
    const token = localStorage.getItem("access_token");

    if (!token) {
      setError("Please login first.");
      setLoading(false);
      return;
    }

    try {
      const response = await fetch(
        `${API_URL}/chat/history`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error("Failed to load chat history.");
      }

      const data = await response.json();

      console.log("Chat history:", data);

      setChats(data);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Failed to load history."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadHistory();
  }, []);

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />

      <main className="flex-1 p-8">
        <div className="mx-auto max-w-5xl">

          <h1 className="text-3xl font-bold">
            Chat History
          </h1>

          <p className="mt-2 text-gray-600">
            View your previous questions and answers.
          </p>

          {loading && (
            <p className="mt-8 text-gray-500">
              Loading history...
            </p>
          )}

          {error && (
            <div className="mt-8 rounded-xl bg-red-50 p-4 text-red-700">
              {error}
            </div>
          )}

          {!loading && !error && chats.length === 0 && (
            <div className="mt-8 rounded-2xl border bg-white p-8 text-center">
              <p className="text-gray-500">
                No conversations yet.
              </p>
            </div>
          )}

          {!loading && chats.length > 0 && (
            <div className="mt-8 space-y-4">
              {chats.map((chat, index) => (
                <div
                  key={chat.id ?? index}
                  className="rounded-2xl border bg-white p-6 shadow-sm"
                >
                  <div>
                    <p className="text-sm font-medium text-gray-500">
                      Question
                    </p>

                    <p className="mt-2 font-medium">
                      {chat.question ?? "No question"}
                    </p>
                  </div>

                  <div className="mt-5 border-t pt-5">
                    <p className="text-sm font-medium text-gray-500">
                      Answer
                    </p>

                    <p className="mt-2 whitespace-pre-wrap leading-7 text-gray-700">
                      {chat.answer ?? "No answer"}
                    </p>
                  </div>

                  {chat.created_at && (
                    <p className="mt-4 text-xs text-gray-400">
                      {new Date(
                        chat.created_at
                      ).toLocaleString()}
                    </p>
                  )}
                </div>
              ))}
            </div>
          )}

        </div>
      </main>
    </div>
  );
}
