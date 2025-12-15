# 🌍 TerraGuard MH – Multi-Hazard Early Warning & Preparedness

TerraGuard MH (Multi-Hazard) is a lightweight, demo-ready platform that turns live/simulated hazard data into **actionable alerts** for operations teams. It focuses on rapid **detection/nowcasting**, simple **ETA** estimates, **proximity risk scoring**, and **offline-resilient alerting** for:

- **🌐 Earthquakes** – magnitude/depth, distance to Areas of Interest (AOIs), **P/S-wave ETA**, intensity proxy  
- **🌊 Tsunami** – quake-driven heuristic + **ETA** for coastal AOIs  
- **🏔️ Glacier / GLOF** – trend-based risk score from temp/rain/slope (CSV)  
- **☁️ Weather (optional)** – can plug in flood/heatwave/rain models later

> ⚠️ **Scientific note:** Deterministic **earthquake prediction** (exact time/place/magnitude) is **not feasible** today. TerraGuard MH implements **rapid detection & early warning-style nowcasting** and demo heuristics only. For production, integrate official feeds (IMD/NCS/INCOIS/PTWC/USGS/NRSC).
---

## ✨ Key Innovations
- **Unified Alert Bus** → Multiple hazards output a single, consistent alert format (INFO / ADVISORY / WATCH / WARNING)
- **Offline Resilience** → Logs to CSV and triggers a simulated **local siren** path when the network is down
- **Rapid Nowcasting** → P/S-ETA for quakes, tsunami ETA heuristic, GLOF trend score—fast & explainable
- **Contact-Aware Alerts** → Each AOI has NDRF + local EOC contact numbers for immediate SOP execution
---

## 🧩 Modules
- `terraguard/quake_module.py` – pulls recent quakes (USGS) or generates a synthetic event offline, computes **distance / P-ETA / S-ETA / intensity proxy** per AOI
- `terraguard/tsunami_module.py` – **tsunami advisory/watch/warning** heuristic from quake params + **ETA** to coastal AOIs
- `terraguard/glacier_module.py` – toy **GLOF risk** from temp/rain/slope trends (CSV)
- `terraguard/alert_router.py` – routes alerts to **console + CSV log**; simulates **offline siren**
- `app.py` – **Gradio dashboard** with tabs: Earthquakes, Tsunami, Glacier

---
