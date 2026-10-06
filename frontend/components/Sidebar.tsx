"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";

export default function Sidebar() {
  const router = useRouter();

  function handleLogout() {
    localStorage.removeItem("access_token");
    router.push("/login");
  }

  return (
    <aside className="flex h-screen w-64 flex-col border-r bg-white p-5">
      <h1 className="mb-8 text-xl font-bold">
        AI Knowledge Platform
      </h1>

      <nav className="flex flex-col gap-2">
        <Link
          href="/chat"
          className="rounded-lg px-4 py-3 hover:bg-gray-100"
        >
          💬 Chat
        </Link>

        <Link
          href="/documents"
          className="rounded-lg px-4 py-3 hover:bg-gray-100"
        >
          📄 Documents
        </Link>

        <Link
          href="/history"
          className="rounded-lg px-4 py-3 hover:bg-gray-100"
        >
          🕘 Chat History
        </Link>

        <Link
          href="/research"
          className="rounded-lg px-4 py-3 hover:bg-gray-100"
        >
          🔎 Research
        </Link>
      </nav>

      <div className="mt-auto">
        <button
          onClick={handleLogout}
          className="w-full rounded-lg px-4 py-3 text-left text-red-600 hover:bg-red-50"
        >
          🚪 Logout
        </button>
      </div>
    </aside>
  );
}
