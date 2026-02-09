# GitHub & Streamlit Deployment Guide

## Step 1: Push to GitHub

### Option A: Using GitHub CLI (Recommended)

```bash
# Authenticate with GitHub (one time)
gh auth login

# Then push
git push origin main
```

### Option B: Using Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name and select `repo` scope
4. Copy the token

Then update your remote:

```bash
git remote set-url origin https://<YOUR_TOKEN>@github.com/Aishu7-5/stroke-prediction-app.git
git push origin main
```

## Step 2: Deploy to Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Click "New app" or "Sign up"
3. Connect your GitHub account
4. Select the repository: `Aishu7-5/stroke-prediction-app`
5. Select the branch: `main`
6. Set the main file path: `app.py`
7. Click "Deploy"

Your app will be live at: `https://share.streamlit.io/Aishu7-5/stroke-prediction-app`

## Step 3: Manage Secrets (If Needed)

1. In Streamlit Cloud dashboard, go to Settings
2. Add any secrets in the "Secrets" section

Your Streamlit app is now configured and ready to deploy!
