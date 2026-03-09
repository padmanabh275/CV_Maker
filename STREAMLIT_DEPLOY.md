# Deploying to Streamlit Community Cloud

## Fix for "Failed building wheel for Pillow"

Streamlit Cloud may use **Python 3.14**, for which Pillow does not have pre-built wheels yet, so the build fails (zlib / `__version__` errors).

### What to do

1. **Delete the current app** in the Streamlit Cloud dashboard (if it exists).
2. **Deploy again** from your GitHub repo.
3. In the deploy dialog, open **"Advanced settings"**.
4. Set **Python version** to **3.11** (or 3.12).
5. Save and deploy.

With Python 3.11, Pillow installs from a wheel and the app should start.

### Optional: system libs

The repo includes a **`packages.txt`** that installs `zlib1g-dev` and `libjpeg-dev` on the Cloud runner. That helps if any dependency ever needs to build from source.
