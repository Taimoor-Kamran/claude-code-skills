// Todo-related types

export interface Todo {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  due_date?: string;
  created_at: string;
  updated_at: string;
}

export interface TodoCreate {
  title: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high';
  due_date?: string;
  completed?: boolean;
}

export interface TodoUpdate {
  title?: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high';
  due_date?: string;
  completed?: boolean;
}

export interface TodoListResponse {
  todos: Todo[];
  total: number;
}

export interface AgentResponse {
  response: string;
}

export interface AgentRequest {
  message: string;
}

export type Priority = 'low' | 'medium' | 'high';