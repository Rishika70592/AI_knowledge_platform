"use client";

import { useState } from "react";
import { apiRequest } from "../../lib/api";


export default function TestApiPage() {
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  async function testBackend() {
    try {
      setLoading(true);
      setResult("");

      const response = await apiRequest("/health");
      const data = await response.json();

      setResult(JSON.stringify(data, null, 2));
    } catch (error) {
      setResult(
        error instanceof Error
          ? error.message
          : "Something went wrong"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center p-8">
      <div className="w-full max-w-xl rounded-xl border p-8 shadow-sm">
        <h1 className="mb-2 text-2xl font-bold">
          AI Knowledge Platform
        </h1>

        <p className="mb-6 text-gray-600">
          FastAPI connection test
        </p>

        <button
          onClick={testBackend}
          disabled={loading}
          className="rounded-lg bg-black px-5 py-2.5 text-white disabled:opacity-50"
        >
          {loading ? "Testing..." : "Test FastAPI"}
        </button>

        {result && (
          <pre className="mt-6 overflow-auto rounded-lg bg-gray-100 p-4 text-sm">
            {result}
          </pre>
        )}
      </div>
    </main>
  );
}
