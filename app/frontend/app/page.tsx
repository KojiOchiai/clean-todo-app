"use client"

import { Login } from '@/components/Login'
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Checkbox } from "@/components/ui/checkbox"
import { Input } from "@/components/ui/input"
import { LogOut, Trash2 } from 'lucide-react'
import { useEffect, useState } from 'react'

interface Todo {
  id: number;
  text: string;
  completed: boolean;
}

export default function App() {
  const [todos, setTodos] = useState<Todo[]>([])
  const [newTodo, setNewTodo] = useState('')
  const [token, setToken] = useState<string | null>(null)
  const tokenUrl = process.env.NODE_ENV === 'production' 
    ? '/token' 
    : 'http://localhost:8000/token';

  useEffect(() => {
    const storedToken = localStorage.getItem('authToken');
    setToken(storedToken);
  }, []);

  const handleLogin = async (username: string, password: string) => {
    try {

      const response = await fetch(tokenUrl, {
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
      const token = data.token;

      // save token to local storage
      localStorage.setItem('authToken', token);
      setToken(token);

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

  const addTodo = () => {
    if (newTodo.trim() !== '') {
      setTodos([...todos, { id: Date.now(), text: newTodo, completed: false }])
      setNewTodo('')
    }
  }

  const toggleTodo = (id: number) => {
    setTodos(todos.map(todo =>
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    ))
  }

  const deleteTodo = (id: number) => {
    setTodos(todos.filter(todo => todo.id !== id))
  }

  if (!token) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100">
        <Login onLogin={handleLogin} />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-100 flex items-stretch justify-center py-12 px-4 sm:px-6 lg:px-8">
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
        <div className="flex mb-4">
          <Input
            type="text"
            value={newTodo}
            onChange={(e) => setNewTodo(e.target.value)}
            placeholder="Enter a new task"
            className="flex-grow mr-2"
          />
          <Button onClick={addTodo}>Add</Button>
        </div>
        <ul className="space-y-2">
          {todos.map(todo => (
            <li key={todo.id} className="flex items-center justify-between p-2 border rounded">
              <div className="flex items-center">
                <Checkbox
                  id={`todo-${todo.id}`}
                  checked={todo.completed}
                  onCheckedChange={() => toggleTodo(todo.id)}
                  className="mr-2"
                />
                <label
                  htmlFor={`todo-${todo.id}`}
                  className={`${todo.completed ? 'line-through text-gray-500' : ''}`}
                >
                  {todo.text}
                </label>
              </div>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => deleteTodo(todo.id)}
                aria-label="Remove Tasks"
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </li>
          ))}
        </ul>
      </Card>
    </div>
  )
}

