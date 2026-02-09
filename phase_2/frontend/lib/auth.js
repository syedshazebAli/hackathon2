// lib/auth.js
// import { createAuthClient } from '@better-auth/client';

// const authClient = createAuthClient({
//   baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:8888',
//   // Add any additional configuration here
// });

// Export a mock auth client for now
const authClient = {
  signIn: () => Promise.resolve({ success: true }),
  signOut: () => Promise.resolve(),
  getSession: () => Promise.resolve(null),
};

export default authClient;