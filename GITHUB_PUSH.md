# Push CV_Maker to GitHub

Git is initialized and the initial commit is done on branch `main`. To create the GitHub repo and push:

## 1. Create the repository on GitHub

1. Go to **https://github.com/new**
2. **Repository name:** `CV_Maker` (or any name you prefer)
3. Choose **Public**
4. Do **not** add a README, .gitignore, or license (we already have them)
5. Click **Create repository**

## 2. Add remote and push

In a terminal, from this folder (`CV_Maker`), run (replace `YOUR_USERNAME` with your GitHub username):

```bash
cd "c:\Users\Padmanabh\OneDrive\Documents\CV_Maker"
git remote add origin https://github.com/YOUR_USERNAME/CV_Maker.git
git push -u origin main
```

If you use SSH:

```bash
git remote add origin git@github.com:YOUR_USERNAME/CV_Maker.git
git push -u origin main
```

## 3. Done

After the push, the repo will be at `https://github.com/YOUR_USERNAME/CV_Maker`.
