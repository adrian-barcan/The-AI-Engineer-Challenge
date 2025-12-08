# Troubleshooting "Failed to fetch" and 404 Errors

## Common Issues and Solutions

### Issue 1: 404 Error on API Routes

**Symptoms:** Getting 404 errors when accessing `/api/chat` or other API endpoints.

**Possible Causes:**
1. Vercel routing not configured correctly
2. Python function not being recognized
3. Handler not exported correctly

**Solutions:**

1. **Verify `vercel.json` configuration:**
   - Ensure `api/index.py` is listed in the `builds` section
   - Check that routes are configured to route `/api/(.*)` to `/api/index.py`

2. **Check function logs in Vercel:**
   - Go to Vercel Dashboard → Your Project → Functions tab
   - Look for errors in the Python function logs
   - Check if the function is being invoked

3. **Verify handler export:**
   - The `handler` variable must be exported at the module level
   - It should be: `handler = Mangum(app)`

4. **Test the API endpoint directly:**
   ```bash
   curl https://your-app.vercel.app/api/
   ```
   Should return: `{"status": "ok"}`

### Issue 2: "Failed to fetch" Error

**Symptoms:** Frontend shows "Failed to fetch" when trying to send messages.

**Possible Causes:**
1. CORS issues
2. API endpoint not reachable
3. Network errors
4. API function not deployed correctly

**Solutions:**

1. **Check browser console:**
   - Open browser DevTools (F12)
   - Check the Network tab for failed requests
   - Look at the Console tab for error messages

2. **Verify API is accessible:**
   ```bash
   # Test the root endpoint
   curl https://your-app.vercel.app/api/
   
   # Test the chat endpoint
   curl -X POST https://your-app.vercel.app/api/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello"}'
   ```

3. **Check CORS configuration:**
   - The API has CORS enabled for all origins (`*`)
   - If you need to restrict, update `api/index.py`

4. **Verify environment variables:**
   - Ensure `OPENAI_API_KEY` is set in Vercel
   - Redeploy after adding environment variables

### Issue 3: Routing Not Working

**Symptoms:** Requests to `/api/*` return 404 or don't reach the Python function.

**Solutions:**

1. **Check Vercel build logs:**
   - Go to Vercel Dashboard → Deployments
   - Click on the latest deployment
   - Check build logs for Python function errors

2. **Verify file structure:**
   ```
   /
   ├── api/
   │   └── index.py  ← Must exist here
   ├── frontend/
   └── vercel.json
   ```

3. **Try alternative routing:**
   If the current routing doesn't work, try updating `vercel.json`:
   ```json
   {
     "routes": [
       {
         "src": "/api/(.*)",
         "dest": "/api/index.py"
       }
     ]
   }
   ```

### Issue 4: Python Dependencies Not Installing

**Symptoms:** Function fails with import errors.

**Solutions:**

1. **Ensure `requirements.txt` exists:**
   - Must be in the project root
   - Must include all dependencies including `mangum`

2. **Check Python version:**
   - Vercel uses Python 3.12 by default
   - Can be specified in `vercel.json`: `"PYTHON_VERSION": "3.12"`

3. **Verify dependencies:**
   ```txt
   fastapi>=0.121.2
   mangum>=0.18.0
   openai>=1.0.0
   python-dotenv>=1.0.0
   ```

## Debugging Steps

1. **Check Vercel Function Logs:**
   - Dashboard → Project → Functions → `api/index.py`
   - Look for invocation logs and errors

2. **Test API directly:**
   ```bash
   # Health check
   curl https://your-app.vercel.app/api/
   
   # Chat endpoint
   curl -X POST https://your-app.vercel.app/api/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "test"}'
   ```

3. **Check browser network tab:**
   - See the exact request being made
   - Check response status and headers
   - Look for CORS errors

4. **Verify deployment:**
   - Ensure latest code is deployed
   - Check that `vercel.json` is committed
   - Verify all files are in the repository

## Quick Fix Checklist

- [ ] `requirements.txt` includes `mangum>=0.18.0`
- [ ] `api/index.py` exports `handler = Mangum(app)`
- [ ] `vercel.json` routes `/api/(.*)` to `/api/index.py`
- [ ] `OPENAI_API_KEY` is set in Vercel environment variables
- [ ] Project has been redeployed after changes
- [ ] Frontend uses relative URL `/api/chat` (not absolute)

## Still Not Working?

1. Check Vercel's function logs for detailed error messages
2. Verify the Python function is being built (check build logs)
3. Try accessing the API endpoint directly (bypassing the frontend)
4. Check if there are any Vercel-specific limitations or quotas
