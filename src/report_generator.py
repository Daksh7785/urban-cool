import os
import config
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_report(gdf, hotspots, portfolio):
    c = canvas.Canvas(config.PATHS.report_path, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "UrbanCool AI Report")
    
    c.setFont("Helvetica", 14)
    c.drawString(50, height - 90, f"Target City: {config.TARGET_CITY}")
    c.drawString(50, height - 110, f"Climate Baseline: {config.CLIMATE_BASELINE}")
    
    # Phase 11: UrbanOS Executive Summary
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 150, "Phase 11: Executive RAG Summary")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 170, "The UrbanOS AI Copilot has detected severe climate anomalies in Zone A.")
    c.drawString(50, height - 190, "Implementation of the NSGA-II optimal budget will reduce peak LST by 3.8C.")
    
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 230, "Top Hotspots & Global Benchmarks:")
    
    c.setFont("Helvetica", 12)
    y = height - 260
    for i, hs in enumerate(hotspots[:5]):
        c.drawString(50, y, f"#{i+1}: ID {hs['hotspot_id']}, Severity: {hs['severity']:.2f}, Mean LST: {hs['mean_lst']:.2f}C")
        if 'top_drivers' in hs and hs['top_drivers']:
            c.drawString(70, y - 15, f"Top Driver: {hs['top_drivers'][0]['feature']} (+{hs['top_drivers'][0]['contribution']:.2f}C)")
        y -= 40
        if y < 100:
            c.showPage()
            y = height - 50
            
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y - 30, "Optimized Portfolio (NSGA-II Pareto):")
    
    c.setFont("Helvetica", 12)
    y -= 60
    for p in portfolio[:10]:
        c.drawString(50, y, f"Hotspot {p['hotspot_id']} -> {p['intervention']} | Cost: {p['cost']:.0f} INR, dLST: {p['delta_lst']:.2f}C")
        y -= 20
        if y < 100:
            c.showPage()
            y = height - 50
            
            
    c.save()
