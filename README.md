# RoomGPT (CPU Version)

A minimal CPU-friendly version of RoomGPT using a local Stable Diffusion model.

## 🔧 Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the backend:
   ```bash
   cd backend
   python app.py
   ```

3. Open `frontend/index.html` in your browser.

## 📁 Structure

- `backend/` – Flask API with local AI model
- `frontend/` – Minimal UI
- `input/` – Uploaded images
- `generated/` – AI-generated outputs
