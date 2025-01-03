import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Trash2 } from "lucide-react";
import { useEffect, useRef, useState } from "react";

interface Todo {
  id: number;
  title: string;
  description: string;
  is_done: boolean;
}

interface TodoItemProps {
  todo: Todo;
  toggleTodo: (id: number) => void;
  deleteTodo: (id: number) => void;
  saveEdit: (id: number, title: string, description: string) => void;
}

export function TodoItem({ todo, toggleTodo, deleteTodo, saveEdit }: TodoItemProps) {
  const [editing, setEditing] = useState(false);
  const [editingTitle, setEditingTitle] = useState(todo.title);
  const [editingDescription, setEditingDescription] = useState(todo.description);
  const titleInputRef = useRef<HTMLInputElement | null>(null);
  const descriptionInputRef = useRef<HTMLInputElement | null>(null);

  useEffect(() => {
    if (editing) {
      titleInputRef.current?.focus();
    }
  }, [editing]);

  const handleBlur = () => {
    setTimeout(() => {
      if (
        document.activeElement !== titleInputRef.current &&
        document.activeElement !== descriptionInputRef.current
      ) {
        saveEdit(todo.id, editingTitle, editingDescription);
        setEditing(false);
      }
    }, 0);
  };

  return (
    <li className="flex items-center justify-between p-2">
      <Checkbox
        id={`todo-${todo.id}`}
        checked={todo.is_done}
        onCheckedChange={() => toggleTodo(todo.id)}
        className="mr-2"
      />
      <div className="flex flex-col flex-grow">
        {editing ? (
          <>
            <Input
              type="text"
              value={editingTitle}
              onChange={(e) => setEditingTitle(e.target.value)}
              onBlur={handleBlur}
              className="mb-1"
              ref={titleInputRef}
            />
            <Input
              type="text"
              value={editingDescription}
              onChange={(e) => setEditingDescription(e.target.value)}
              onBlur={handleBlur}
              className="mb-1"
              ref={descriptionInputRef}
            />
          </>
        ) : (
          <>
            <label
              htmlFor={`todo-${todo.id}`}
              className={`${todo.is_done ? 'line-through text-gray-500' : ''} ${!todo.title ? 'text-gray-400' : ''}`}
              onClick={() => setEditing(true)}
            >
              {todo.title || "Click to add title"}
            </label>
            <p
              className={`text-sm text-gray-600 truncate ${todo.is_done ? 'line-through' : ''}`}
              onClick={() => setEditing(true)}
            >
              {todo.description}
            </p>
          </>
        )}
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
  );
} 