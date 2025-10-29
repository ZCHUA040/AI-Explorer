# AiXexplore 📍

AiXexplore is a full-stack web application designed to help users generate personalised, AI-powered day-trip itineraries across Singapore. It offers a seamless user experience with secure authentication, activity discovery, intelligent planning, and itinerary management.

<p align="center">
  <img src="/landing page.png" width=300 />
</p>

<p align="center">
    <a href="https://github.com/softwarelab3/2006-SCSB-T5/tree/lab5-frontend">Frontend</a>
    |
    <a href="https://github.com/softwarelab3/2006-SCSB-T5/tree/lab5-backend">Backend</a>
    |
    <a href="https://youtu.be/8AF-AX5OjSw">Demo Video</a>
    |
    <a href="https://github.com/softwarelab3/2006-SCSB-T5/blob/main/Lab%205/Lab%205%20SRS%20Deliverables.pdf">SRS</a>
</p>

## 📚 Table of Contents

- [AiXexplore 📍](#aixexplore-)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Diagrams](#diagrams)
- [Getting Started](#-getting-started)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Key Functional Pages](#-key-functional-pages)
- [External APIs](#external-apis)
- [Supporting Documentation](#supporting-documentations)
- [Demo Video](#demo-video)
- [Contributors](#contributors)

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


# External APIs

1. **Gemini API**
   1. Gen-Ai (https://ai.google.dev/gemini-api/docs)

---

# Contributors

The following contributors have contributed to the whole Software Developement Life-cycle, including (not exhausive):

1. Ideation and refinement
2. Generation of functional and non-funtional requirements
3. Generation of Use Cases and Descriptions
4. UI/UX Mockup and Prototyping (Figma)
5. Design of Architecture Diagram, Class Diagram, Sequence Diagrams, and Dialog Map Diagram
6. Development of Application
7. Black-box and White-box Testing
8. Documentations

| Name           | Github Username                                | Role                   |
| -------------- | ---------------------------------------------  | ---------------------- |
| Agarwal Aryaman|                                                | Frontend               |
| Chua Zhi Li    | [ZCHUA040](https://github.com/ZCHUA040)        | Full-Stack / Backend   |
| Gu Boyuan      | [boyuan618](https://github.com/boyuan618)      | Full-Stack / Backend   |
| Guo Kexuan     | [kx0224](https://github.com/kx0224)            | Frontend               |
| Ng Yuhang Dilon| [dillydecoded](https://github.com/dillydecoded)| Frontend               |
| Seet Jia Viona | [vionaseet](https://github.com/vionaseet)      | Backend                |
