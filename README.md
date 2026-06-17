<div align="center">
  <h1>❄️ UrbanCool AI</h1>
  <p><b>Enterprise-Grade Geospatial AI for Mitigating Urban Heat Islands</b></p>
  <p><i>Winner - Smart City Innovation</i></p>
</div>

---

## 🌍 The Global Crisis: Why We Built This

As climate change accelerates, extreme heat is now the **number one weather-related killer** worldwide. Cities suffer uniquely due to the **Urban Heat Island (UHI) effect**—a phenomenon where dense concrete, asphalt, and dark building materials absorb solar radiation and trap heat, causing urban centers to be up to 10°C hotter than surrounding rural areas.

This causes a vicious cycle:
- **Health Crisis:** Vulnerable populations suffer from heat strokes and respiratory issues.
- **Energy Drain:** Air conditioning usage skyrockets, stressing the electrical grid and increasing greenhouse gas emissions.
- **Economic Loss:** Lower worker productivity and strained municipal infrastructure.

City Planners and Municipal Governments *want* to cool their cities by planting trees or installing cool roofs, but they are paralyzed by complexity. They don't know exactly **where** to place these interventions to achieve the maximum temperature drop for their limited budgets.

## 💡 Our Solution: UrbanCool AI

**UrbanCool AI** is a comprehensive, physics-informed Machine Learning platform designed to give governments a "God's-eye view" of their city's thermodynamics. It completely automates the process of identifying heat hotspots, diagnosing their underlying drivers, and generating mathematically optimized cooling strategies.

Instead of relying on guesswork, UrbanCool AI empowers decision-makers to test, simulate, and budget millions of dollars of green infrastructure with pinpoint geographic accuracy.

---

## 🧠 Model Architecture & Physics Engine

UrbanCool AI is not just a standard regression model. It is a highly specialized pipeline combining Geospatial AI, Explainable ML, Physics Simulation, and Operations Research.

### 1. Geospatial Data Ingestion Pipeline
The system ingests multispectral satellite imagery (simulating Landsat 8/9 via Google Earth Engine APIs) and structural urban data (OpenStreetMap). It extracts:
*   **Target Variable:** Land Surface Temperature (LST).
*   **Predictive Features:** NDVI (Vegetation), NDBI (Building Density), Albedo (Reflectivity), and Distance to Water Bodies.

### 2. The Explainable AI Layer (XGBoost + SHAP)
We employ an **eXtreme Gradient Boosting (XGBoost)** regressor to model the complex, non-linear relationships between urban morphology and surface temperature. 
*   Because city planners cannot blindly trust a "black box," we integrate **SHAP (SHapley Additive exPlanations)**. 
*   When a hotspot is detected, the model outputs exactly *why* it is hot (e.g., "70% of the heat in Zone A is caused by a lack of tree canopy, while 30% is caused by low albedo rooftops").

### 3. Physics-Informed Simulation (Oke Surface Energy Balance)
We ensure our AI doesn't "hallucinate" impossible cooling results. When simulating the addition of trees or cool roofs, the ML predictions are strictly bounded by thermodynamic laws derived from the **Oke Surface Energy Balance Model**. This guarantees that a simulated intervention will only yield realistic temperature deltas (e.g., capping cooling drops at a maximum of 10°C).

### 4. Multi-Objective Portfolio Optimizer (NSGA / Knapsack)
The platform features an advanced mathematical optimizer. Given a strict municipal budget (e.g., $5,000,000) and thousands of potential intervention combinations across hundreds of hotspots, it uses a bounded Knapsack algorithm to find the absolute best portfolio. It balances:
*   **Maximizing** overall $\Delta$ LST (temperature drop).
*   **Minimizing** implementation cost.
*   **Minimizing** the embodied carbon of the interventions (favoring carbon-sequestering trees over high-carbon concrete pavements).

---

## 🚀 The 10 "Wow" Features

1. **🛰️ Urban Heat Digital Twin:** A live, interactive 3D-ready representation of the city's heat signature.
2. **🧠 Explainable Policy Engine:** The AI automatically generates localized, markdown-formatted governance rules (e.g., "Mandate cool roof coatings in Zone B") derived directly from SHAP values.
3. **⚖️ Multi-Objective Budget Optimizer:** Mathematically guarantees the maximum cooling ROI for every dollar spent.
4. **🌡️ Physics-Informed Interventions:** Thermodynamic bounds ensure realistic cooling simulations.
5. **🌱 Carbon + Cooling Lifecycle Tracking:** We calculate the carbon footprint vs. cooling benefit of your interventions.
6. **📅 7-Day Heat Forecast Engine:** Predictive modeling to warn cities of impending heat spikes.
7. **📊 Urban Heat Vulnerability Index (UHVI):** A composite score mapping extreme heat over vulnerable population densities to prioritize life-saving deployments.
8. **📍 Precision Intervention Placement:** Generates exact GeoJSON coordinate bounds for new pocket parks and cool roofs.
9. **👥 Simulated Citizen Feedback Layer:** REST APIs allowing citizens to report heat stress directly to the command center.
10. **📑 AI Generated Planner Reports:** Automated PDF dossier generation for mayoral briefings.

---

## 🏗️ System Architecture

UrbanCool AI is engineered using a decoupled, highly scalable microservices architecture.

*   **Frontend (Command Center):** 
    *   `React` & `TypeScript` (powered by `Vite`)
    *   `TailwindCSS` for beautiful, responsive SaaS-level styling
    *   `Leaflet` & `Recharts` for interactive geospatial mapping.
*   **Backend API Gateway:**
    *   `Node.js` & `Express` handling RESTful routing and JWT Authentication.
    *   `MongoDB` for persistent storage of user profiles, projects, and geometries.
    *   `Redis` & `BullMQ` for asynchronous, non-blocking task orchestration.
*   **Analytics Engine (Heavy Compute):**
    *   `Python` & `FastAPI` deployed as isolated background workers to execute heavy machine learning tasks without blocking the web server.

---

## 🌎 Real-World Impact

If deployed by a mid-sized metropolitan government, UrbanCool AI will:
1. **Save Lives:** By directing cooling interventions to high-density, low-income neighborhoods (using our UHVI metric) before extreme heat waves hit.
2. **Save Taxpayer Money:** Eliminating the "trial and error" phase of urban planning. The mathematical optimizer ensures that every dollar of a $10M climate resilience grant achieves maximum thermodynamic impact.
3. **Accelerate Policy:** The automated Policy Engine translates raw satellite data into actionable legislative text in seconds, drastically speeding up bureaucratic response times.

---

## 💻 Getting Started & Deployment

### Option 1: Live Web Demo (Vercel)
The frontend UI is deployed publicly via Vercel for instant demonstrations. It features an intelligent **Demo Mode**—if the heavy Python AI backend isn't running, the dashboard falls back to a high-fidelity simulated dataset so you can experience the full interactive UI.
[View Live Demo](#) *(Insert your Vercel Link Here)*

### Option 2: Full-Stack Local Execution (For Developers)
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
The backend is rigorously validated. Our CI/CD pipeline runs `pytest` suites to ensure physical constraints are respected and that the Machine Learning pipeline maintains predictability ($R^2$ scores > 0.8).
```bash
pytest tests/
```