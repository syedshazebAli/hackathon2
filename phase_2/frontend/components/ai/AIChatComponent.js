'use client';

import { useState, useRef, useEffect } from 'react';
// import { useAuth } from '@better-auth/react';
import axios from 'axios';

const AIChatComponent = ({ onTaskUpdate }) => {
  // const { session } = useAuth();
  // Mock session for testing
  const session = { accessToken: 'mock-token' };
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message to chat
    const userMessage = { role: 'user', content: inputValue, timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Send request to AI endpoint
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_BACKEND_API_URL || 'http://localhost:8000'}/api/ai/chat`,
        {
          message: inputValue,
          user_id: "mock-user-id"  // Add a mock user ID
        },
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      // Add AI response to chat
      const aiMessage = { 
        role: 'ai', 
        content: response.data.response_message, 
        intent: response.data.intent,
        timestamp: new Date() 
      };
      
      setMessages(prev => [...prev, aiMessage]);
      
      // Trigger task update if needed based on AI response
      if (response.data.intent === 'create_task' && onTaskUpdate) {
        onTaskUpdate(); // Refresh task list
      }
    } catch (error) {
      console.error('Error processing AI request:', error);
      // Mock AI response for testing
      const mockResponse = {
        data: {
          response_message: `I understood your request: "${inputValue}". This is a mock response.`,
          intent: 'unknown'
        }
      };
      
      // Add AI response to chat
      const aiMessage = { 
        role: 'ai', 
        content: mockResponse.data.response_message, 
        intent: mockResponse.data.intent,
        timestamp: new Date() 
      };
      
      setMessages(prev => [...prev, aiMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-4 mb-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">AI Task Assistant</h3>
      
      <div className="border border-gray-200 rounded-lg h-64 overflow-y-auto p-4 mb-4 bg-gray-50">
        {messages.length === 0 ? (
          <div className="h-full flex items-center justify-center text-gray-500">
            Ask me to create, update, or manage your tasks using natural language!
          </div>
        ) : (
          <div className="space-y-3">
            {messages.map((msg, index) => (
              <div 
                key={index} 
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div 
                  className={`max-w-[80%] rounded-lg px-4 py-2 ${
                    msg.role === 'user' 
                      ? 'bg-blue-500 text-white' 
                      : 'bg-gray-200 text-gray-800'
                  }`}
                >
                  <div className="text-sm">{msg.content}</div>
                  {msg.intent && (
                    <div className="text-xs opacity-75 mt-1">Intent: {msg.intent}</div>
                  )}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-200 text-gray-800 rounded-lg px-4 py-2 max-w-[80%]">
                  <div className="flex space-x-2">
                    <div className="w-2 h-2 bg-gray-600 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-600 rounded-full animate-bounce delay-100"></div>
                    <div className="w-2 h-2 bg-gray-600 rounded-full animate-bounce delay-200"></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="flex space-x-2">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask me to create or manage tasks..."
          disabled={isLoading}
          className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={!inputValue.trim() || isLoading}
          className="bg-blue-500 text-white rounded-lg px-4 py-2 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
        >
          Send
        </button>
      </form>
      
      <div className="mt-3 text-sm text-gray-500">
        Examples: "Create a task to buy groceries", "Mark my workout as completed", "Show my tasks"
      </div>
    </div>
  );
};

export default AIChatComponent;