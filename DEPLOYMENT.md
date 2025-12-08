# Deployment Guide for Vercel

This guide explains how to deploy both the Next.js frontend and FastAPI backend to Vercel.

## Prerequisites

1. A Vercel account (sign up at [vercel.com](https://vercel.com))
2. Vercel CLI installed globally:
   ```bash
   npm install -g vercel
   ```
3. Your project pushed to a GitHub repository (recommended)

## Project Structure

The project is organized as follows:
```
/
├── frontend/          # Next.js application
├── api/              # FastAPI backend
│   └── index.py      # FastAPI app with Mangum handler
├── vercel.json       # Vercel configuration
└── pyproject.toml    # Python dependencies
```

## Configuration Files

### vercel.json
This file configures Vercel to:
- Build the Next.js frontend from the `frontend/` directory
- Deploy the FastAPI backend as a Python serverless function
- Route `/api/*` requests to the Python backend
- Route all other requests to the Next.js frontend

### API Handler
The `api/index.py` file uses Mangum to wrap the FastAPI app, making it compatible with Vercel's serverless function runtime.

## Deployment Steps

### Option 1: Deploy via Vercel CLI (Recommended for Testing)

1. **Login to Vercel:**
   ```bash
   vercel login
   ```

2. **Deploy from project root:**
   ```bash
   vercel
   ```
   
   Follow the prompts:
   - Link to existing project or create new one
   - Confirm project settings
   - Deploy to production (or preview)

3. **Set Environment Variables:**
   After deployment, you'll need to set environment variables in the Vercel dashboard:
   - Go to your project settings
   - Navigate to "Environment Variables"
   - Add the following:
     - `OPENAI_API_KEY`: Your OpenAI API key
     - `NEXT_PUBLIC_API_URL`: Leave empty (the frontend will use relative URLs)

### Option 2: Deploy via GitHub Integration (Recommended for Production)

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Configure Vercel deployment"
   git push origin main
   ```

2. **Import project in Vercel:**
   - Go to [vercel.com/new](https://vercel.com/new)
   - Import your GitHub repository
   - Vercel will auto-detect the configuration from `vercel.json`

3. **Configure Environment Variables:**
   - In project settings → Environment Variables, add:
     - `OPENAI_API_KEY`: Your OpenAI API key
     - `NEXT_PUBLIC_API_URL`: Leave empty (or set to your Vercel domain if needed)

4. **Deploy:**
   - Vercel will automatically deploy on every push to your main branch
   - You can also trigger manual deployments from the dashboard

## Environment Variables

### Required Variables

- **OPENAI_API_KEY**: Your OpenAI API key (required for the backend)
  - Get one at: https://platform.openai.com/api-keys

### Optional Variables

- **NEXT_PUBLIC_API_URL**: API base URL (usually not needed - frontend uses relative URLs)
  - If your frontend and API are on different domains, set this to your API domain
  - Example: `https://your-app.vercel.app`

## How It Works

1. **Frontend (Next.js):**
   - Built from the `frontend/` directory
   - Served as a static site with server-side rendering
   - Routes all non-API requests

2. **Backend (FastAPI):**
   - Deployed as a Python serverless function
   - Handles all `/api/*` routes
   - Uses Mangum to adapt FastAPI to Vercel's serverless runtime

3. **Routing:**
   - Requests to `/api/*` → Python serverless function (`api/index.py`)
   - All other requests → Next.js frontend

## Troubleshooting

### API Routes Not Working

1. **Check vercel.json routing:**
   - Ensure `/api/(.*)` routes to `/api/index.py`
   - Verify the file path is correct

2. **Check environment variables:**
   - Ensure `OPENAI_API_KEY` is set in Vercel dashboard
   - Redeploy after adding environment variables

3. **Check function logs:**
   - Go to Vercel dashboard → Your project → Functions tab
   - Check for errors in the Python function logs

### Frontend Can't Connect to API

1. **Check API URL configuration:**
   - The frontend uses relative URLs by default
   - If needed, set `NEXT_PUBLIC_API_URL` in Vercel environment variables

2. **Check CORS settings:**
   - The API is configured to allow all origins (`*`)
   - If you need to restrict, update `api/index.py`

### Build Failures

1. **Python dependencies:**
   - Ensure `pyproject.toml` includes all required packages
   - Vercel will install dependencies automatically

2. **Node.js dependencies:**
   - Ensure `frontend/package.json` is correct
   - Vercel will run `npm install` automatically

## Post-Deployment

After successful deployment:

1. **Test the API:**
   - Visit `https://your-app.vercel.app/api/` (should return `{"status": "ok"}`)
   - Test the chat endpoint via the frontend

2. **Update frontend API URL (if needed):**
   - If your frontend needs an absolute URL, set `NEXT_PUBLIC_API_URL` in Vercel
   - Otherwise, relative URLs will work automatically

3. **Monitor:**
   - Check Vercel dashboard for function invocations
   - Monitor API usage and costs

## Additional Resources

- [Vercel Python Documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Mangum Documentation](https://mangum.io/)
- [Next.js on Vercel](https://vercel.com/docs/frameworks/nextjs)
