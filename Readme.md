# SC2006
# AiXexplore 📍

AiXexplore is a full-stack web application designed to help users generate personalized, AI-powered day-trip itineraries across Singapore. It offers a seamless user experience with secure authentication, activity discovery, intelligent planning, and itinerary management.

---

## 💪 Features

### 👤 User Account Management
- Secure user registration with password validation
- JWT-based login/logout session handling
- Forgot password email reset flow
- Change password functionality (requires current password)

### 📅 Activity Marketplace
- Curated activities from OnePA and Data.gov.sg
- Filtering by interest category and budget level
- Activity detail page with full descriptions

### ⚖️ AI-Powered Trip Planning
- Gemini API integration for smart itinerary generation
- Planner form includes: title, date, time, interest, budget
- Generated plans are saved and viewable under My Itineraries

### 📌 Itinerary Management
- View, edit, or delete saved itineraries
- Edit itinerary activities by ID
- View itineraries shared with the user

### 🔒 Security
- bcrypt for password hashing
- JWT access control for protected routes
- Email validation and password strength enforced

---

## 🎨 Tech Stack

### Frontend
- **React** (Vite + TypeScript)
- **Tailwind CSS**
- **Axios** for HTTP requests
- **React Router DOM** for routing
- **React Hot Toast** for notifications

### Backend
- **Flask** (Python)
- **Flask-JWT-Extended**
- **Flask-Mail** (reset password)
- **Flask-CORS**
- **bcrypt** and **email-validator**

### AI
- **Gemini API** for itinerary generation

### Database
- **SQLite** (for development/testing)
---

## 🚀 Getting Started

### Backend Setup

1. Navigate to `backend/`
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run Flask server:
```bash
python app.py
```

### Frontend Setup

1. Navigate to `frontend/`
2. Install packages:
```bash
npm install
```
3. Start development server:
```bash
npm run dev
```

### URLs
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:5000`

---

## 📂 Key Functional Pages

| Page | Route | Description |
|------|-------|-------------|
| Home | `/` | Landing page |
| Register | `/register` | Create new user |
| Login | `/login` | User sign-in |
| Planner | `/planner` | Generate itinerary |
| Itineraries | `/itineraries` | View user's plans |
| Activity Marketplace | `/activitymarketplace` | Browse activities |
| Shared Itineraries | `/shared_itineraries` | View shared plans |
| Change Password | `/change-password` | Change current password |
| Forgot Password | `/forgot-password` | Start password reset flow |

---

## 🙋‍ Contact
Feel free to contribute or report issues in this repository!
