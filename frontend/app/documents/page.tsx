"use client";

import { useEffect, useState } from "react";
import Sidebar from "../../components/Sidebar";
import { API_URL } from "../../lib/api";

type Document = {
  id?: string;
  filename?: string;
  file_name?: string;
  name?: string;
  created_at?: string;
};

export default function DocumentsPage() {
  const [file, setFile] = useState<File | null>(null);
  const [documents, setDocuments] = useState<Document[]>([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [loadingDocuments, setLoadingDocuments] = useState(true);

  async function loadDocuments() {
    const token = localStorage.getItem("access_token");

    if (!token) {
      setMessage("Please login first.");
      setLoadingDocuments(false);
      return;
    }

    try {
      const response = await fetch(`${API_URL}/documents`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to load documents.");
      }

      const data = await response.json();

      console.log("Documents:", data);

      setDocuments(data);
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Failed to load documents."
      );
    } finally {
      setLoadingDocuments(false);
    }
  }

  useEffect(() => {
    loadDocuments();
  }, []);

  async function handleUpload() {
    if (!file) {
      setMessage("Please select a PDF first.");
      return;
    }

    const token = localStorage.getItem("access_token");

    if (!token) {
      setMessage("Please login first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      setMessage("");

      const response = await fetch(
        `${API_URL}/documents/upload`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        }
      );

      if (!response.ok) {
        const error = await response.text();
        throw new Error(error || "Upload failed.");
      }

      const data = await response.json();

      console.log("Upload response:", data);

      setMessage("Document uploaded successfully!");
      setFile(null);

      await loadDocuments();
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Upload failed."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />

      <main className="flex-1 p-8">
        <div className="mx-auto max-w-5xl">

          <h1 className="text-3xl font-bold">
            Documents
          </h1>

          <p className="mt-2 text-gray-600">
            Manage your knowledge base documents.
          </p>

          {/* Upload */}
          <div className="mt-8 rounded-2xl border bg-white p-8 shadow-sm">
            <h2 className="text-xl font-semibold">
              Upload PDF
            </h2>

            <input
              type="file"
              accept=".pdf,application/pdf"
              onChange={(event) => {
                setFile(event.target.files?.[0] || null);
                setMessage("");
              }}
              className="mt-6 block w-full rounded-lg border p-3"
            />

            {file && (
              <p className="mt-3 text-sm text-gray-600">
                Selected: {file.name}
              </p>
            )}

            <button
              onClick={handleUpload}
              disabled={!file || loading}
              className="mt-5 rounded-lg bg-black px-6 py-3 font-medium text-white disabled:opacity-40"
            >
              {loading ? "Uploading..." : "Upload Document"}
            </button>

            {message && (
              <p className="mt-5 rounded-lg bg-gray-100 p-4 text-sm">
                {message}
              </p>
            )}
          </div>

          {/* Documents */}
          <div className="mt-8 rounded-2xl border bg-white p-8 shadow-sm">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold">
                Your Documents
              </h2>

              <button
                onClick={loadDocuments}
                className="rounded-lg border px-4 py-2 text-sm hover:bg-gray-50"
              >
                Refresh
              </button>
            </div>

            {loadingDocuments ? (
              <p className="mt-6 text-gray-500">
                Loading documents...
              </p>
            ) : documents.length === 0 ? (
              <p className="mt-6 text-gray-500">
                No documents uploaded yet.
              </p>
            ) : (
              <div className="mt-6 space-y-3">
                {documents.map((document, index) => (
                  <div
                    key={document.id ?? index}
                    className="flex items-center justify-between rounded-xl border p-4"
                  >
                    <div>
                      <p className="font-medium">
                        {document.filename ??
                          document.file_name ??
                          document.name ??
                          "Document"}
                      </p>

                      {document.created_at && (
                        <p className="mt-1 text-sm text-gray-500">
                          {new Date(
                            document.created_at
                          ).toLocaleString()}
                        </p>
                      )}
                    </div>

                    <span className="rounded-full bg-green-100 px-3 py-1 text-xs font-medium text-green-700">
                      Uploaded
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>

        </div>
      </main>
    </div>
  );
}
