// API service for todo app backend
import { Todo, TodoCreate, TodoUpdate, TodoListResponse, AgentResponse, AgentRequest } from '@/types/todo';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';

// Todo API functions
export const todoApi = {
  // Get all todos
  getTodos: async (params?: {
    skip?: number;
    limit?: number;
    search?: string;
    completed?: boolean;
    priority?: string;
    date_from?: string;
    date_to?: string;
  }): Promise<TodoListResponse> => {
    const searchParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          searchParams.append(key, String(value));
        }
      });
    }

    const response = await fetch(`${API_BASE_URL}/todos/?${searchParams}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch todos: ${response.statusText}`);
    }
    return response.json();
  },

  // Create a new todo
  createTodo: async (todoData: TodoCreate): Promise<Todo> => {
    const response = await fetch(`${API_BASE_URL}/todos/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(todoData),
    });

    if (!response.ok) {
      throw new Error(`Failed to create todo: ${response.statusText}`);
    }
    return response.json();
  },

  // Get a specific todo by ID
  getTodo: async (id: number): Promise<Todo> => {
    const response = await fetch(`${API_BASE_URL}/todos/${id}/`);
    if (!response.ok) {
      throw new Error(`Failed to fetch todo: ${response.statusText}`);
    }
    return response.json();
  },

  // Update a todo
  updateTodo: async (id: number, todoData: TodoUpdate): Promise<Todo> => {
    const response = await fetch(`${API_BASE_URL}/todos/${id}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(todoData),
    });

    if (!response.ok) {
      throw new Error(`Failed to update todo: ${response.statusText}`);
    }
    return response.json();
  },

  // Delete a todo
  deleteTodo: async (id: number): Promise<void> => {
    const response = await fetch(`${API_BASE_URL}/todos/${id}/`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      throw new Error(`Failed to delete todo: ${response.statusText}`);
    }
  },

  // Toggle todo completion status
  toggleTodo: async (id: number): Promise<Todo> => {
    const response = await fetch(`${API_BASE_URL}/todos/${id}/toggle/`, {
      method: 'POST',
    });

    if (!response.ok) {
      throw new Error(`Failed to toggle todo: ${response.statusText}`);
    }
    return response.json();
  },
};

// Agent API functions
export const agentApi = {
  // Chat with the AI agent
  chat: async (message: string): Promise<AgentResponse> => {
    const response = await fetch(`${API_BASE_URL}/agent/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error(`Failed to chat with agent: ${response.statusText}`);
    }
    return response.json();
  },

  // Setup agent (if needed)
  setup: async (): Promise<{ message: string }> => {
    const response = await fetch(`${API_BASE_URL}/agent/setup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({}),
    });

    if (!response.ok) {
      throw new Error(`Failed to setup agent: ${response.statusText}`);
    }
    return response.json();
  },
};