# Frontend - Next.js Application

## Overview
The frontend is built with Next.js 15+ using the App Router, with Tailwind CSS for styling. It integrates with Better Auth for authentication and communicates with the FastAPI backend for data management.

## Tech Stack
- Next.js 15+
- React 18+
- TypeScript (optional)
- Tailwind CSS
- Better Auth Client
- Axios/Fetch for API calls

## Directory Structure
```
frontend/
├── app/
│   ├── (auth)/
│   │   ├── sign-in/
│   │   └── sign-up/
│   ├── dashboard/
│   │   └── page.tsx
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── ui/
│   ├── auth/
│   ├── tasks/
│   └── navigation/
├── lib/
│   ├── auth.ts
│   └── api.ts
├── public/
├── styles/
├── package.json
├── tailwind.config.js
├── next.config.js
└── tsconfig.json
```

## Key Features
- Authentication flows (sign in/up)
- Protected routes for authenticated users
- Task management interface
- Responsive design with Tailwind CSS
- Integration with Better Auth
- API communication with backend

## Environment Variables
- `NEXT_PUBLIC_BETTER_AUTH_URL`: Better Auth service URL
- `NEXT_PUBLIC_BACKEND_API_URL`: Backend API URL

## Dependencies
- next
- react
- react-dom
- @better-auth/react
- axios (or fetch)
- tailwindcss
- postcss
- autoprefixer

## Development
- Runs on port 3000
- Uses proxy for API calls to backend
- Hot reloading enabled