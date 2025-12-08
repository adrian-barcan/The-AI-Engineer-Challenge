# Mental Coach Frontend

A modern, responsive Next.js frontend for the Mental Coach AI application. This frontend provides a beautiful chat interface that connects to the FastAPI backend.

## Features

- 🎨 Modern, beautiful UI with gradient design
- 💬 Real-time chat interface
- 📱 Fully responsive design (mobile-friendly)
- ⚡ Fast and optimized with Next.js
- 🎯 Type-safe with TypeScript

## Prerequisites

Before running the frontend, make sure you have:

- Node.js 18+ installed
- npm or yarn package manager
- The FastAPI backend running (see main README for backend setup)

## Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Running Locally

1. Make sure your FastAPI backend is running on `http://localhost:8000` (default).

2. Start the Next.js development server:
   ```bash
   npm run dev
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:3000
   ```

4. You should see the Mental Coach chat interface. Start chatting!

## Configuration

The frontend is configured to connect to the FastAPI backend automatically. By default, it connects to:
- Local development: `http://localhost:8000`

If your backend is running on a different URL, you can set the `NEXT_PUBLIC_API_URL` environment variable:

1. Create a `.env.local` file in the `frontend` directory:
   ```bash
   NEXT_PUBLIC_API_URL=http://your-backend-url:8000
   ```

2. Restart the development server.

## Building for Production

To create a production build:

```bash
npm run build
```

To start the production server:

```bash
npm start
```

## Deployment

This frontend is designed to be deployed on Vercel. The project includes a `vercel.json` configuration file in the root directory that handles routing.

### Deploying to Vercel

1. Install Vercel CLI globally (if not already installed):
   ```bash
   npm install -g vercel
   ```

2. From the project root, run:
   ```bash
   vercel
   ```

3. Follow the prompts to deploy your application.

4. Make sure to set the `NEXT_PUBLIC_API_URL` environment variable in your Vercel project settings to point to your deployed backend URL.

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout component
│   ├── page.tsx            # Main chat page
│   ├── page.module.css     # Styles for the chat page
│   └── globals.css         # Global styles
├── package.json            # Dependencies and scripts
├── tsconfig.json           # TypeScript configuration
├── next.config.js          # Next.js configuration
└── README.md              # This file
```

## Troubleshooting

### Backend Connection Issues

If you're having trouble connecting to the backend:

1. Verify the backend is running: Check `http://localhost:8000` in your browser
2. Check CORS settings: The backend should have CORS enabled (it does by default)
3. Verify the API URL: Make sure `NEXT_PUBLIC_API_URL` is set correctly if using a custom URL

### Port Already in Use

If port 3000 is already in use, Next.js will automatically try the next available port. Check the terminal output for the actual port number.

## Technologies Used

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **CSS Modules** - Scoped styling
- **React Hooks** - State management

## License

This project is part of The AI Engineer Challenge.
