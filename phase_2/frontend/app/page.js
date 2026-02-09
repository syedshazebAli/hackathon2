'use client';

import { useEffect, useState } from 'react';
// import { useAuth } from '@better-auth/react';
import Link from 'next/link';

export default function Home() {
  // const { session, signIn, signOut } = useAuth();
  // Mock session for testing
  const session = null;
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Check if user is authenticated
    if (typeof window !== 'undefined') {
      setLoading(false);
    }
  }, []);

  if (loading) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>;
  }

  if (!session) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-md">
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Welcome to Task Manager
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Sign in to manage your tasks securely
          </p>
        </div>

        <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
          <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
            <div className="space-y-4">
              <Link href="/dashboard">
                <button
                  className="w-full flex justify-center items-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  Access Dashboard (Demo Mode)
                </button>
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // If user is authenticated, redirect to dashboard
  if (session) {
    // Using next/navigation router for redirect
    if (typeof window !== 'undefined') {
      window.location.href = '/dashboard';
    }
    return <div>Redirecting to dashboard...</div>;
  }
}