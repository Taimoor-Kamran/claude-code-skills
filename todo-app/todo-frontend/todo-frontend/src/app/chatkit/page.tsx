"use client";

import { CustomChatWidget } from "@/components/CustomChatWidget";

export default function ChatKitPage() {
  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="p-6 border-b border-gray-200">
            <h1 className="text-2xl font-bold text-gray-900">AI Todo Assistant (Streaming)</h1>
            <p className="text-gray-600 mt-2">
              Chat with the AI assistant to manage your todos using natural language with real-time streaming.
            </p>
          </div>

          <div className="p-6">
            <div className="h-[600px]">
              <CustomChatWidget
                apiUrl={process.env.NEXT_PUBLIC_CHATKIT_URL || "http://localhost:8000/api/v1/chatkit"}
                height="100%"
              />
            </div>
          </div>
        </div>

        <div className="mt-6 bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold mb-3">Examples of commands you can try:</h2>
          <ul className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-gray-600">
            <li className="flex items-start">
              <span className="text-blue-600 mr-2">•</span>
              <span>"Create a todo to buy groceries"</span>
            </li>
            <li className="flex items-start">
              <span className="text-blue-600 mr-2">•</span>
              <span>"List all my todos"</span>
            </li>
            <li className="flex items-start">
              <span className="text-blue-600 mr-2">•</span>
              <span>"Mark todo 1 as complete"</span>
            </li>
            <li className="flex items-start">
              <span className="text-blue-600 mr-2">•</span>
              <span>"Update my shopping todo to have high priority"</span>
            </li>
            <li className="flex items-start">
              <span className="text-blue-600 mr-2">•</span>
              <span>"Delete the meeting todo"</span>
            </li>
            <li className="flex items-start">
              <span className="text-blue-600 mr-2">•</span>
              <span>"Show me incomplete high priority todos"</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}