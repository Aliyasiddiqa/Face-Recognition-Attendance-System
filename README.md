# Face Recognition Attendance System — A2 (GUI + MySQL)

**What this is**
A beginner-friendly attendance system with:
- Tkinter GUI
- Face capture (from webcam) and dataset creation
- LBPH face recognizer (OpenCV)
- Attendance storage in MySQL (with CSV fallback if DB not configured)
- Export to Excel/CSV

**Folders & files**
- `main.py` — GUI (register face, train model, start attendance)
- `train.py` — Train LBPH model from `dataset/`
- `detector.py` — Capture and recognition helpers
- `db.py` — MySQL helper (falls back to CSV)
- `config.json.example` — Example DB configuration
- `requirements.txt` — Python libs to install
- `dataset/` — Place images here: `dataset/User.ID.jpeg` (ID is integer)
- `trainer.yml` — Generated after training
- `attendance.csv` — Auto-created if DB not available

**Quick setup**
1. Install Python 3.8+ and pip.
2. Create & activate virtualenv (optional but recommended).
3. Install requirements:
   ```
   pip install -r requirements.txt
   ```
   Important: use `opencv-contrib-python` (this project requires `cv2.face`).
4. (Optional) Setup MySQL and create a database. Add credentials to `config.json` (copy from `config.json.example`).
5. Run the GUI:
   ```
   python main.py
   ```

**How to use**
- Register: Enter numeric ID and name, press *Register* to take 20 face samples via webcam. Images saved to `dataset/`.
- Train: Press *Train Model* to create `trainer.yml`.
- Start Attendance: Press *Start Attendance* to recognize faces and mark attendance in DB or `attendance.csv`.

**Notes**
- If `cv2.face` is missing, ensure you installed `opencv-contrib-python`.
- For best results, take multiple clear face images under good lighting.
- You can customize number of samples and model settings in `detector.py`.

