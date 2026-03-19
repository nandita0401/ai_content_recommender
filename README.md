# 🎬 AI Content Recommender

![Next.js](https://img.shields.io/badge/Frontend-Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)
![TypeScript](https://img.shields.io/badge/Language-TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Python](https://img.shields.io/badge/AI%20Backend-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Styling-Tailwind%20CSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

> A full-stack AI-powered content recommendation app that suggests movies, shows, and music based on your personal preferences and current mood — combining a modern Next.js frontend with a Python AI backend.

---

## 📖 Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Project Structure](#project-structure)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

## About the Project

Finding something to watch or listen to that truly matches how you feel in the moment is harder than it should be. **AI Content Recommender** solves this by combining **user preference profiling** with **mood-based filtering** to surface the most relevant movies, shows, and music at the right time.

The project features a clean, responsive **Next.js + TypeScript** frontend and a **Python-powered AI backend** that handles the recommendation logic — demonstrating a full-stack architecture with a clear separation between UI and intelligence layers.

---

## Features

- 🎭 **Mood-Based Recommendations** — Input your current emotional state and get content matched to how you feel
- 👤 **Preference-Aware Suggestions** — Personalizes results based on your genre and content type preferences
- 🎬 **Multi-Category Support** — Recommends across movies, TV shows, and music in one unified experience
- ⚡ **Fast, Responsive UI** — Built with Next.js and Tailwind CSS for a smooth, modern experience
- 🐍 **Python AI Backend** — Decoupled recommendation engine for clean separation of concerns
- 🔄 **Real-time Results** — Frontend communicates with the backend API to fetch recommendations dynamically

---

## How It Works
```
User Opens App
      │
      ▼
Set Preferences (genres, content type: movies / shows / music)
      │
      ▼
Select Current Mood
      │
      ▼
Frontend sends request to Python Backend API
      │
      ▼
AI Recommendation Engine
  ├── Filters by user preferences
  ├── Weights results by mood mapping
  └── Returns ranked content list
      │
      ▼
Results displayed in responsive UI
```

**Recommendation Logic:**
1. User sets their **content preferences** (genres, categories)
2. User selects their **current mood** (e.g. happy, relaxed, anxious, energetic)
3. The Python backend maps mood → content attributes (e.g. tempo, tone, genre weights)
4. The engine cross-references preferences with mood weights to return a ranked recommendation list
5. Results are rendered in the Next.js frontend in real time

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend Framework | Next.js (App Router) |
| Language (Frontend) | TypeScript |
| Styling | Tailwind CSS |
| AI / Recommendation Engine | Python |
| Frontend-Backend Communication | REST API |
| Config | PostCSS, ESLint, tsconfig |

---

## Getting Started

### Prerequisites

- Node.js v18+
- Python 3.8+
- npm or yarn

### Installation

1. **Clone the repository**
```bash
   git clone https://github.com/nandita0401/ai_content_recommender.git
   cd ai_content_recommender
```

2. **Install frontend dependencies**
```bash
   npm install
```

3. **Set up the Python backend**
```bash
   cd backend
   pip install -r requirements.txt
   python app.py
```

4. **Run the frontend development server**
```bash
   cd ..
   npm run dev
```

5. **Open the app**
```
   http://localhost:3000
```

> ⚠️ Make sure the Python backend server is running before starting the frontend, as the recommendation engine is served separately.

---

## Project Structure
```
ai_content_recommender/
├── app/                  # Next.js App Router pages and components
├── backend/              # Python AI recommendation engine
│   ├── app.py            # Backend API server
│   └── recommender.py    # Core recommendation logic
├── public/               # Static assets
├── tailwind.config.js    # Tailwind CSS configuration
├── tsconfig.json         # TypeScript configuration
├── next.config.ts        # Next.js configuration
├── package.json
└── README.md
```

---

## Future Improvements

- [ ] Integrate **TMDB API** for real-time movie and show data
- [ ] Integrate **Spotify API** for live music recommendations
- [ ] Add **user authentication** and saved preference profiles
- [ ] Improve AI engine with **NLP-based sentiment analysis** for richer mood detection
- [ ] Add **collaborative filtering** — recommend based on what similar users enjoyed
- [ ] Deploy backend to **AWS / Railway** and frontend to **Vercel**
- [ ] Add **"Why this was recommended"** explainability feature

---

## Author

**Nandita Bharambe**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-nanditabharambe-0A66C2?style=flat&logo=linkedin)](https://www.linkedin.com/in/nanditabharambe/)
[![GitHub](https://img.shields.io/badge/GitHub-nandita0401-181717?style=flat&logo=github)](https://github.com/nandita0401)

---

> 💡 *This project explores how AI can make content discovery more personal and emotionally intelligent — going beyond "you watched X, try Y" to actually understanding how a user feels and what they need in that moment.*
