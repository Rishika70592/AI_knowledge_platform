"use client";

import { FormEvent, useState } from "react";
import { apiRequest } from "../../lib/api";
import { useRouter } from "next/navigation";
import router from "next/router";
import Link from "next/link";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    try {
      setLoading(true);
      setMessage("");

      const response = await apiRequest("/auth/login", {
        method: "POST",
        body: JSON.stringify({
          email,
          password,
        }),
      });

      const data = await response.json();

      // Temporarily save the JWT.
      localStorage.setItem("access_token", data.access_token);

      setMessage("Login successful!");
      setTimeout(() => {
  router.push("/chat");
}, 1000);
      console.log("Login response:", data);
    } catch (error) {
      setMessage(
        error instanceof Error ? error.message : "Login failed"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center p-6">
      <div className="w-full max-w-md rounded-2xl border p-8 shadow-lg">
        <h1 className="mb-2 text-3xl font-bold">
          Welcome back
        </h1>

        <p className="mb-8 text-gray-600">
          Sign in to your AI Knowledge Platform
        </p>

        <form onSubmit={handleLogin} className="space-y-5">
          <div>
            <label className="mb-2 block text-sm font-medium">
              Email
            </label>

            <input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="you@example.com"
              required
              className="w-full rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-black"
            />
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium">
              Password
            </label>

            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="••••••••"
              required
              className="w-full rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-black"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-black px-4 py-3 font-medium text-white disabled:opacity-50"
          >
            {loading ? "Signing in..." : "Sign in"}
          </button>
        </form>

        
<p className="mt-6 text-center text-sm text-gray-600">
  Don't have an account?{" "}
  <Link
    href="/register"
    className="font-medium text-black underline"
  >
    Create account
  </Link>
</p>
      </div>
    </main>
  );
}
