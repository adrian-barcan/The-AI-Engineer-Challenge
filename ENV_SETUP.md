# Setting Environment Variables in Vercel

## Method 1: Vercel Dashboard (Recommended)

1. **Navigate to your project:**
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click on your project name

2. **Open Settings:**
   - Click on the **Settings** tab in the top navigation

3. **Go to Environment Variables:**
   - In the left sidebar, click on **Environment Variables**

4. **Add the OpenAI API Key:**
   - Click **Add New** button
   - Enter the following:
     - **Key**: `OPENAI_API_KEY`
     - **Value**: Your OpenAI API key (starts with `sk-`)
     - **Environment**: Select all three:
       - ✅ Production
       - ✅ Preview  
       - ✅ Development
   - Click **Save**

5. **Redeploy your application:**
   - Go to the **Deployments** tab
   - Click the three dots (⋯) on your latest deployment
   - Select **Redeploy**
   - Or simply push a new commit to trigger a new deployment

## Method 2: Vercel CLI

### Install Vercel CLI (if not already installed):
```bash
npm install -g vercel
```

### Login to Vercel:
```bash
vercel login
```

### Link your project (if not already linked):
```bash
vercel link
```

### Set the environment variable:
```bash
vercel env add OPENAI_API_KEY
```

When prompted:
- Enter your OpenAI API key value
- Select environments: Production, Preview, Development (select all)

### Verify the variable was added:
```bash
vercel env ls
```

### Redeploy:
```bash
vercel --prod
```

## Method 3: Using Vercel CLI with .env.local (for local development)

1. **Create a `.env.local` file in your project root:**
   ```bash
   OPENAI_API_KEY=sk-your-key-here
   ```

2. **Push to Vercel:**
   ```bash
   vercel env pull .env.local
   ```

   Or manually add via dashboard/CLI as shown above.

## Getting Your OpenAI API Key

1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click **Create new secret key**
4. Copy the key (you'll only see it once!)
5. Paste it into Vercel as described above

## Important Notes

⚠️ **Security:**
- Never commit your API keys to Git
- Always use environment variables
- The `.env.local` file should be in `.gitignore` (which it already is)

⚠️ **After Adding Variables:**
- You **must redeploy** for changes to take effect
- Environment variables are only available at build/runtime, not during development unless you set them locally

⚠️ **Variable Naming:**
- Use `OPENAI_API_KEY` exactly as shown (case-sensitive)
- The API code looks for this specific variable name

## Verifying It Works

After setting the variable and redeploying:

1. **Test the API endpoint:**
   ```bash
   curl https://your-app.vercel.app/api/
   ```
   Should return: `{"status": "ok"}`

2. **Test the chat endpoint:**
   ```bash
   curl -X POST https://your-app.vercel.app/api/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello"}'
   ```
   Should return a JSON response with a reply (not an error about missing API key)

3. **Check function logs:**
   - Go to Vercel Dashboard → Your Project → Functions tab
   - Check for any errors related to missing API keys

## Troubleshooting

### Variable not working after deployment?
- ✅ Make sure you selected all environments (Production, Preview, Development)
- ✅ Redeploy after adding the variable
- ✅ Check the variable name is exactly `OPENAI_API_KEY` (case-sensitive)
- ✅ Verify the key is valid by testing it locally first

### Getting "OPENAI_API_KEY not configured" error?
- Check Vercel function logs for more details
- Ensure the variable is set for the correct environment
- Try redeploying the project

### Need to update the key?
- Go to Environment Variables in Vercel dashboard
- Click on `OPENAI_API_KEY`
- Click **Edit** and update the value
- Redeploy your application
