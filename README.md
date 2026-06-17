<div align="center">
  <h1>❄️ UrbanCool AI</h1>
  <p><b>Enterprise-Grade Geospatial AI for Mitigating Urban Heat Islands</b></p>
  <p><i>Winner - Smart City Innovation</i></p>
</div>

---

## 🌍 The Problem: Urban Heat Islands (UHI)
As global temperatures rise, cities are heating up twice as fast as rural areas. Concrete, asphalt, and dense buildings absorb and trap the sun's heat, creating dangerously hot **Urban Heat Islands (UHIs)**. This extreme heat leads to increased energy consumption (AC usage), poor air quality, and severe health risks for vulnerable populations.

City planners know they need to cool their cities, but they struggle with three massive questions:
1. **Where** exactly are the most dangerous heat hotspots?
2. **Why** are those specific spots so hot? (Is it lack of trees, too much concrete, or dark roofs?)
3. **What** is the most cost-effective way to fix it with a limited budget?

## 💡 Our Solution: UrbanCool AI
UrbanCool AI is a full-stack, enterprise-grade AI platform that gives city planners a "God's-eye view" of their city's thermodynamics. It completely automates the process of finding heat islands, diagnosing their root causes, and generating optimized, physics-backed cooling strategies.

Instead of guessing where to plant trees or paint roofs, planners use our interactive Digital Twin Dashboard to mathematically guarantee the maximum cooling effect for every dollar spent.

---

## 🚀 Key Features & "Wow" Factors

1. **🛰️ Urban Heat Digital Twin:** We process massive satellite datasets (Land Surface Temperature, NDVI vegetation index, Albedo) to create a live, interactive map of the city's heat signature.
2. **🧠 Explainable AI (SHAP):** When we identify a hotspot, our XGBoost machine learning model doesn't just say "it's hot." It uses SHAP values to explain *exactly why*, breaking it down into specific drivers like "Low Tree Canopy" or "High Building Density."
3. **⚖️ Multi-Objective Budget Optimizer:** You have $5,000,000 to spend. Do you plant trees or install cool roofs? Our Knapsack Optimization algorithm tests millions of combinations to find the absolute best portfolio of interventions to maximize cooling while minimizing cost.
4. **🌡️ Physics-Informed Interventions:** We don't just guess temperature drops. Our backend uses standard thermodynamic models (like the Oke Surface Energy Balance) to simulate exactly how many degrees a neighborhood will cool if you plant 500 trees.
5. **📜 Automated Policy Engine:** The AI automatically writes markdown-formatted policy recommendations (e.g., "Mandate cool roof coatings in Zone B") based directly on the localized ML data.
6. **🌱 Carbon + Cooling Lifecycle:** We calculate not just the temperature drop, but the embodied carbon cost vs. carbon sequestration of the interventions you choose.

---

## 🏗️ Technical Architecture

UrbanCool AI is built using a modern, decoupled microservices architecture designed to scale seamlessly:

*   **Frontend (Command Center):** 
    *   `React` & `TypeScript` (powered by `Vite`)
    *   `TailwindCSS` for beautiful, responsive SaaS-level styling
    *   `Leaflet` & `Recharts` for interactive geospatial mapping and data visualization
*   **Backend (API & Job Queues):**
    *   `Node.js` & `Express` API Gateway
    *   `MongoDB` for persistent storage of user profiles and hotspot geometries
    *   `Redis` & `BullMQ` for asynchronous, non-blocking task orchestration
*   **Analytics Engine (AI & Physics):**
    *   `Python` & `FastAPI` to execute heavy machine learning tasks without blocking the web server
    *   `XGBoost` for predictive modeling
    *   `GeoPandas` & `Rasterio` for advanced spatial transformations

---

## 💻 How to Run It

### 1. Live Web Demo (Vercel)
The frontend UI is deployed publicly via Vercel for instant demonstrations. It features an intelligent **Demo Mode**—if the heavy Python AI backend isn't running, the dashboard falls back to a high-fidelity simulated dataset so judges can still experience the full interactive UI.
[View Live Demo](#) *(Insert your Vercel Link Here)*

### 2. Full-Stack Local Execution (For Developers)
To run the *entire* heavy-compute AI pipeline natively with live Database + Redis + Python + Node communication:

```bash
# 1. Clone the repository
git clone https://github.com/Daksh7785/urban-cool.git
cd urban-cool

# 2. Start all 5 microservices using Docker
docker-compose up --build -d

# 3. Access the platforms
- Frontend UI: http://localhost:5173
- Node.js API: http://localhost:5000
- Python FastAPI ML Workers: http://localhost:8000
```

## 🧪 Testing & Scientific Validation
The backend is rigorously validated. Our CI/CD pipeline runs `pytest` suites to ensure:
*   Physical constraints are respected (e.g., interventions cannot artificially cool a city by impossible margins like 50°C).
*   Machine Learning Predictability ($R^2$ scores > 0.8).

---
*Built to cool the world, one city block at a time.*