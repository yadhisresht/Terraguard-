import gradio as gr, pandas as pd, json
from terraguard.quake_module import fetch_quakes, scan_aoi
from terraguard.tsunami_module import tsunami_flag, eta_to_coast_km
from terraguard.glacier_module import risk_from_trends
from terraguard.utils import pretty_eta

AOI_PATH = "data/aoi.csv"

def ui_quakes(min_mag, hours):
    q = fetch_quakes(hours=hours, min_mag=min_mag)
    out = scan_aoi(q, AOI_PATH)
    return out

def ui_tsunami(sample_quake_json, coast_name):
    aoi = pd.read_csv(AOI_PATH)
    coast = aoi[aoi['name']==coast_name].iloc[0]
    q = json.loads(sample_quake_json)
    flag = tsunami_flag(q, {"lat": coast.lat, "lon": coast.lon})
    dist, eta = eta_to_coast_km(q, coast.lat, coast.lon)
    level = "INFO"
    if flag: level = "WATCH" if q['mag']<8.0 else "WARNING"
    return {
        "tsunami_possible": bool(flag),
        "level": level,
        "dist_km": round(float(dist),1),
        "eta": pretty_eta(eta)
    }

def ui_glacier(csv_path):
    df = pd.read_csv(csv_path)
    score, lvl = risk_from_trends(df)
    return {"glof_risk": round(score,2), "level": lvl}

with gr.Blocks(title="TerraGuard MH") as demo:
    gr.Markdown("# 🌍 TerraGuard MH – Multi‑Hazard Early Warning")
    with gr.Tab("Earthquakes"):
        min_mag = gr.Slider(3.0, 8.0, value=4.5, step=0.1, label="Min Magnitude")
        hours = gr.Slider(6, 72, value=24, step=6, label="Lookback (hours)")
        btn_q = gr.Button("Scan AOIs")
        out_q = gr.Dataframe(label="AOI Alerts (P/S ETA & intensity proxy)")
        btn_q.click(ui_quakes, [min_mag, hours], out_q)

    with gr.Tab("Tsunami"):
        sample = gr.Textbox(label="Quake JSON", value='{"time":"2025-08-23T08:00:00Z","lat":5.8,"lon":92.1,"depth_km":20,"mag":7.6}')
        coast_name = gr.Dropdown(label="Coastal AOI", choices=list(pd.read_csv(AOI_PATH)['name'].values), value="Chennai")
        btn_t = gr.Button("Estimate Tsunami ETA")
        out_t = gr.JSON(label="Tsunami Heuristic")
        btn_t.click(ui_tsunami, [sample, coast_name], out_t)

    with gr.Tab("Glacier/GLOF"):
        up = gr.File(label="Upload glacier inputs CSV", file_count="single")
        out_g = gr.JSON(label="GLOF Risk")
        up.upload(lambda f: ui_glacier(f.name), inputs=up, outputs=out_g)

    gr.Markdown("> ⚠️ This demo is for hackathon use: earthquake **prediction** is not attempted; fast **detection/nowcasting** only.")

if __name__ == "__main__":
    demo.launch()
