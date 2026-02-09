# Deployment Instructions

## Option 1: Streamlit Community Cloud (Recommended)
This is the **easiest and best way** to host Streamlit apps, especially those using machine learning libraries like TensorFlow. It is free and optimized for Streamlit.

1. **Push your code to GitHub.**
   - Create a new repository on GitHub.
   - Run the following commands in your project folder:
     ```bash
     git init
     git add .
     git commit -m "Initial commit"
     git branch -M main
     git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
     git push -u origin main
     ```

2. **Deploy via Streamlit.**
   - Go to [share.streamlit.io](https://share.streamlit.io).
   - Click "New app".
   - Select your GitHub repository, branch (`main`), and file (`app.py`).
   - Click **Deploy**.

Streamlit Cloud will automatically install dependencies from `requirements.txt` and verify your app works.

---

## Option 2: Render (Good alternative)
If you prefer a full server environment:
1. Create a `render.yaml` or just connect your GitHub repo to Render.
2. Select "Web Service".
3. Use the following settings:
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port 10000 --server.address 0.0.0.0`
4. Deploy.

---

## Why not Vercel?
While Vercel is great for frontend apps (Next.js, React), it has limitations for Python Streamlit apps:
- **Serverless Limits:** Vercel functions have strict execution time limits (10-60s), which can interrupt long-running ML predictions.
- **WebSocket Support:** Streamlit relies heavily on WebSockets for real-time updates, which are not natively supported in Vercel Serverless Functions.
- **Size Constraints:** TensorFlow and other ML libraries can exceed Vercel's function size limits (50MB compressed / 250MB uncompressed).

If you absolutely must use Vercel, you would likely need to rewrite the application as a Flask/FastAPI backend API + a separate frontend, which is significantly more complex. We recommend sticking with Streamlit Cloud or Render for the best experience.
