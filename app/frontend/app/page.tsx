"use client"

import { Login } from '@/components/Login'
import { TodoItem } from '@/components/TodoItem'
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { LogOut } from 'lucide-react'
import { useCallback, useEffect, useState } from 'react'

interface Todo {
  id: number;
  title: string;
  description: string;
  is_done: boolean;
}

export default function App() {
  const [todos, setTodos] = useState<Todo[]>([])
  const [token, setToken] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [newTodoId, setNewTodoId] = useState<number | null>(null)
  const apiUrl = process.env.NODE_ENV === 'production' 
    ? '' 
    : 'http://localhost:8000';

  const fetchTodos = useCallback(async (authToken: string) => {
    try {
      const response = await fetch(`${apiUrl}/todos`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${authToken}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch todos');
      }

      const data = await response.json();
      setTodos(data.reverse());
    } catch (error) {
      alert(`Error fetching todos: ${(error as Error).message}`);
    }
  }, [apiUrl]);

  useEffect(() => {
    const storedToken = localStorage.getItem('authToken');
    setToken(storedToken);
    setLoading(false);

    if (storedToken) {
      fetchTodos(storedToken);
    }
  }, [fetchTodos]);

  const handleLogin = async (username: string, password: string) => {
    try {
      const response = await fetch(`${apiUrl}/token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          username,
          password,
        }),
      });

      if (!response.ok) {
        const errorMessage = await response.text();
        throw new Error(errorMessage);
      }

      const data = await response.json();
      const token = data.access_token;

      // save token to local storage
      localStorage.setItem('authToken', token);
      setToken(token);
      fetchTodos(token);

    } catch (error) {
      const errorMessage = (error as Error).message;
      alert(`Login failed. Please check your username and password. Error: ${errorMessage}`);
    }
  };

  const handleLogout = () => {
    // Clear the todo list on logout to protect user privacy
    localStorage.removeItem('authToken');
    setToken(null);
    setTodos([])
  }

  const addTodo = async () => {
    // Create a new empty Todo item
    const newTodoItem = {
      id: Date.now(), // temporary id
      title: '',
      description: '',
      is_done: false
    };

    // Add the new empty Todo to the list and set it to editing mode
    setTodos([newTodoItem, ...todos]);
    setNewTodoId(newTodoItem.id);

    // Send request to server to add new empty todo
    try {
      const response = await fetch(`${apiUrl}/todos`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ title: '', description: '', is_done: false })
      });

      if (!response.ok) {
        throw new Error('Failed to add todo');
      }

      const data = await response.json();
      // Replace the temporary Todo with the one from the server
      setTodos([data.todo, ...todos.filter(todo => todo.id !== newTodoItem.id)]);
      setNewTodoId(data.todo.id);
      
    } catch (error) {
      alert(`Error adding todo: ${(error as Error).message}`);
    }
  };

  const toggleTodo = async (id: number) => {
    const todo = todos.find(todo => todo.id === id);
    if (!todo) return;

    try {
      const response = await fetch(`${apiUrl}/todos/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ is_done: !todo.is_done })
      });

      if (!response.ok) {
        throw new Error('Failed to update todo');
      }

      setTodos(todos.map(todo =>
        todo.id === id ? { ...todo, is_done: !todo.is_done } : todo
      ));
    } catch (error) {
      alert(`Error updating todo: ${(error as Error).message}`);
    }
  }

  const deleteTodo = async (id: number) => {
    try {
      const response = await fetch(`${apiUrl}/todos/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to delete todo');
      }

      setTodos(todos.filter(todo => todo.id !== id));
    } catch (error) {
      alert(`Error deleting todo: ${(error as Error).message}`);
    }
  }

  const saveEdit = async (id: number, title: string, description: string) => {
    try {
      const response = await fetch(`${apiUrl}/todos/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ title, description })
      });

      if (!response.ok) {
        throw new Error('Failed to update todo');
      }

      setTodos(todos.map(todo =>
        todo.id === id ? { ...todo, title, description } : todo
      ));
    } catch (error) {
      alert(`Error updating todo: ${(error as Error).message}`);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100">
        <p>Loading...</p>
      </div>
    )
  }

  if (!token) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100">
        <Login onLogin={handleLogin} />
      </div>
    )
  }

  return (
    <div
      className="
        min-h-screen bg-gray-100 flex items-stretch 
        justify-center py-12 px-4 sm:px-6 lg:px-8
      "
    >
      <Card className="max-w-md w-full p-6">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-2xl font-bold">Todo App</h1>
          <Button
            variant="outline"
            size="sm"
            onClick={handleLogout}
            className="flex items-center"
          >
            <LogOut className="mr-2 h-4 w-4" />
            Logout
          </Button>
        </div>
        <Button
          onClick={addTodo}
          className="
            mb-4 w-full text-gray-600 bg-gray-200 hover:bg-gray-300 
            focus:ring-2 focus:ring-gray-400
          "
        >
          Add Todo
        </Button>
        <ul className="space-y-2">
          {todos.map(todo => (
            <TodoItem
              key={todo.id}
              todo={todo}
              toggleTodo={toggleTodo}
              deleteTodo={deleteTodo}
              saveEdit={saveEdit}
              editing={todo.id === newTodoId}
            />
          ))}
        </ul>
      </Card>
    </div>
  )
}

