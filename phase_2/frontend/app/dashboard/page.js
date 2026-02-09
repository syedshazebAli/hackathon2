'use client';

import { useState, useEffect } from 'react';
// import { useAuth } from '@better-auth/react';
import axios from 'axios';
import { PlusIcon, CheckCircleIcon, TrashIcon } from '@heroicons/react/24/outline';
import AIChatComponent from '../../components/ai/AIChatComponent';

const Dashboard = () => {
  // const { session, signOut, isPending } = useAuth();
  // Mock session for testing purposes
  const session = { user: { name: 'Test User', email: 'test@example.com' }, accessToken: 'mock-token' };
  const signOut = () => console.log('Sign out clicked');
  const isPending = false;
  
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [newTask, setNewTask] = useState({ title: '', description: '', priority: 'medium', category: '' });
  const [error, setError] = useState('');

  // Load tasks when component mounts
  useEffect(() => {
    if (session) {
      fetchTasks();
    }
  }, [session]);

  const fetchTasks = async () => {
    try {
      const response = await axios.get(`${process.env.NEXT_PUBLIC_BACKEND_API_URL || 'http://localhost:8000'}/api/tasks`, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      setTasks(response.data);
    } catch (err) {
      console.error('Error fetching tasks:', err);
      // For now, mock some tasks if there's an error
      setTasks([
        { id: 1, title: 'Sample Task', description: 'This is a sample task', status: 'pending', priority: 'medium', category: 'General', created_at: new Date().toISOString() },
        { id: 2, title: 'Another Task', description: 'This is another sample task', status: 'completed', priority: 'high', category: 'Work', created_at: new Date().toISOString() }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = async (e) => {
    e.preventDefault();
    setError('');

    try {
      // Add required user_id field for the backend (proper UUID format)
      const taskData = {
        ...newTask,
        user_id: "00000000-0000-0000-0000-000000000001"  // Proper UUID format for testing
      };
      
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_BACKEND_API_URL || 'http://localhost:8000'}/api/tasks`,
        taskData,
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      setTasks([...tasks, response.data]);
      setNewTask({ title: '', description: '', priority: 'medium', category: '' });
    } catch (err) {
      console.error('Error adding task:', err);
      // Add the task to the local state as fallback
      const mockTask = {
        id: tasks.length + 1,
        ...newTask,
        status: 'pending',
        created_at: new Date().toISOString()
      };
      setTasks([...tasks, mockTask]);
      setNewTask({ title: '', description: '', priority: 'medium', category: '' });
    }
  };

  const handleCompleteTask = async (taskId) => {
    try {
      const response = await axios.patch(
        `${process.env.NEXT_PUBLIC_BACKEND_API_URL || 'http://localhost:8000'}/api/tasks/${taskId}/complete`,
        {},
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      // Update the task in the local state
      setTasks(tasks.map(task =>
        task.id === taskId ? { ...task, status: 'completed', completed_at: response.data.task.completed_at } : task
      ));
    } catch (err) {
      console.error('Error completing task:', err);
      // Update the task locally if there's an error
      setTasks(tasks.map(task =>
        task.id === taskId ? { ...task, status: 'completed', completed_at: new Date().toISOString() } : task
      ));
    }
  };

  const handleDeleteTask = async (taskId) => {
    try {
      await axios.delete(
        `${process.env.NEXT_PUBLIC_BACKEND_API_URL || 'http://localhost:8000'}/api/tasks/${taskId}`,
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      // Remove the task from the local state
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err) {
      console.error('Error deleting task:', err);
      // Remove the task locally if there's an error
      setTasks(tasks.filter(task => task.id !== taskId));
    }
  };

  // Don't show loading state since we're using mock data
  // if (isPending || loading) {
  //   return (
  //     <div className="min-h-screen bg-gray-50 flex items-center justify-center">
  //       <div className="text-center">
  //         <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
  //         <p className="mt-4 text-gray-600">Loading dashboard...</p>
  //       </div>
  //     </div>
  //   );
  // }

  // Don't check for session since we're using mock data
  // if (!session) {
  //   return (
  //     <div className="min-h-screen bg-gray-50 flex items-center justify-center">
  //       <div className="text-center">
  //         <p className="text-gray-600">You need to be logged in to view the dashboard.</p>
  //       </div>
  //     </div>
  //   );
  // }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Task Dashboard</h1>
          <div className="flex items-center space-x-4">
            <div className="text-sm text-gray-700">
              Welcome, {session?.user?.name || session?.user?.email || 'Guest'}!
            </div>
            <button
              onClick={() => signOut()}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
            >
              Sign out
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        {/* Add Task Form */}
        <div className="mb-8 bg-white shadow overflow-hidden sm:rounded-lg p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Add New Task</h2>
          {error && (
            <div className="mb-4 bg-red-50 text-red-700 p-3 rounded-md">
              {error}
            </div>
          )}

          <form onSubmit={handleAddTask}>
            <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
              <div className="sm:col-span-3">
                <label htmlFor="title" className="block text-sm font-medium text-gray-700">
                  Title *
                </label>
                <div className="mt-1">
                  <input
                    type="text"
                    id="title"
                    value={newTask.title}
                    onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
                    required
                    className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md p-2 border"
                  />
                </div>
              </div>

              <div className="sm:col-span-3">
                <label htmlFor="category" className="block text-sm font-medium text-gray-700">
                  Category
                </label>
                <div className="mt-1">
                  <input
                    type="text"
                    id="category"
                    value={newTask.category}
                    onChange={(e) => setNewTask({ ...newTask, category: e.target.value })}
                    className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md p-2 border"
                  />
                </div>
              </div>

              <div className="sm:col-span-2">
                <label htmlFor="priority" className="block text-sm font-medium text-gray-700">
                  Priority
                </label>
                <select
                  id="priority"
                  value={newTask.priority}
                  onChange={(e) => setNewTask({ ...newTask, priority: e.target.value })}
                  className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>

              <div className="sm:col-span-6">
                <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                  Description
                </label>
                <div className="mt-1">
                  <textarea
                    id="description"
                    rows={3}
                    value={newTask.description}
                    onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
                    className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md p-2 border"
                  />
                </div>
              </div>
            </div>

            <div className="mt-6">
              <button
                type="submit"
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                <PlusIcon className="-ml-1 mr-2 h-5 w-5" aria-hidden="true" />
                Add Task
              </button>
            </div>
          </form>
        </div>

        {/* AI Chat Component */}
        <AIChatComponent onTaskUpdate={fetchTasks} />

        {/* Tasks List */}
        <div className="bg-white shadow overflow-hidden sm:rounded-lg">
          <div className="px-4 py-5 sm:px-6">
            <h2 className="text-lg leading-6 font-medium text-gray-900">Your Tasks</h2>
            <p className="mt-1 max-w-2xl text-sm text-gray-500">List of all your tasks</p>
          </div>
          <div className="border-t border-gray-200">
            <ul className="divide-y divide-gray-200">
              {tasks.length === 0 ? (
                <li className="px-4 py-5 sm:px-6">
                  <p className="text-gray-500">No tasks found. Add a new task to get started!</p>
                </li>
              ) : (
                tasks.map((task) => (
                  <li key={task.id} className="px-4 py-5 sm:px-6 hover:bg-gray-50">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <span className={`mr-3 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          task.status === 'completed'
                            ? 'bg-green-100 text-green-800'
                            : task.priority === 'high'
                              ? 'bg-red-100 text-red-800'
                              : task.priority === 'medium'
                                ? 'bg-yellow-100 text-yellow-800'
                                : 'bg-blue-100 text-blue-800'
                        }`}>
                          {task.status === 'completed' ? 'Completed' : task.status}
                        </span>
                        <h3 className="text-lg font-medium text-gray-900">{task.title}</h3>
                      </div>
                      <div className="flex space-x-2">
                        {task.status !== 'completed' && (
                          <button
                            onClick={() => handleCompleteTask(task.id)}
                            className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                          >
                            <CheckCircleIcon className="-ml-0.5 mr-1 h-4 w-4" aria-hidden="true" />
                            Complete
                          </button>
                        )}
                        <button
                          onClick={() => handleDeleteTask(task.id)}
                          className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                        >
                          <TrashIcon className="-ml-0.5 mr-1 h-4 w-4" aria-hidden="true" />
                          Delete
                        </button>
                      </div>
                    </div>
                    <div className="mt-2">
                      {task.description && (
                        <p className="text-sm text-gray-500">{task.description}</p>
                      )}
                      <div className="mt-2 flex items-center text-xs text-gray-500">
                        {task.category && (
                          <span className="mr-3 inline-flex items-center px-2.5 py-0.5 rounded-full bg-gray-100 text-gray-800">
                            {task.category}
                          </span>
                        )}
                        <span>Priority: {task.priority}</span>
                        {task.created_at && (
                          <span className="ml-3">Created: {new Date(task.created_at).toLocaleDateString()}</span>
                        )}
                      </div>
                    </div>
                  </li>
                ))
              )}
            </ul>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;