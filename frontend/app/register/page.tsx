"use client";

import { FormEvent, useState } from "react";
import { apiRequest } from "../../lib/api";
import { useRouter } from "next/navigation";
import router from "next/router";
import Link from "next/link";

export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleRegister(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (password !== confirmPassword) {
      setMessage("Passwords do not match.");
      return;
    }

    try {
      setLoading(true);
      setMessage("");

      const response = await apiRequest("/auth/register", {
        method: "POST",
        body: JSON.stringify({
          email,
          password,
        }),
      });

      const data = await response.json();

      console.log("Register response:", data);

      setMessage("Registration successful! You can now log in.");

      setTimeout(() => {
      router.push("/login");
}, 1000);
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Registration failed."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-gray-50 p-6">
      <div className="w-full max-w-md rounded-2xl border bg-white p-8 shadow-lg">

        <h1 className="mb-2 text-3xl font-bold">
          Create account
        </h1>

        <p className="mb-8 text-gray-600">
          Create your AI Knowledge Platform account
        </p>

        <form onSubmit={handleRegister} className="space-y-5">

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
              minLength={6}
              className="w-full rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-black"
            />
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium">
              Confirm password
            </label>

            <input
              type="password"
              value={confirmPassword}
              onChange={(event) =>
                setConfirmPassword(event.target.value)
              }
              placeholder="••••••••"
              required
              minLength={6}
              className="w-full rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-black"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-black px-4 py-3 font-medium text-white disabled:opacity-50"
          >
            {loading ? "Creating account..." : "Create account"}
          </button>

        </form>

        <p className="mt-6 text-center text-sm text-gray-600">
  Already have an account?{" "}
  <Link
    href="/login"
    className="font-medium text-black underline"
  >
    Sign in
  </Link>
</p>


      </div>
    </main>
  );
}
