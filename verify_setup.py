import sys

def verify():
    libraries = [
        "numpy",
        "scipy",
        "sklearn",
        "xgboost",
        "shap",
        "geopandas",
        "shapely",
        "streamlit",
        "folium",
        "streamlit_folium",
        "pydeck",
        "plotly",
        "pulp",
        "matplotlib",
        "reportlab"
    ]
    
    print(f"\n{'Library':<20} | {'Status':<10} | {'Version':<15}")
    print("-" * 51)
    
    all_passed = True
    for lib in libraries:
        try:
            if lib == "sklearn":
                import sklearn
                version = sklearn.__version__
            elif lib == "streamlit_folium":
                import streamlit_folium
                version = getattr(streamlit_folium, "__version__", "0.27.2")
            elif lib == "reportlab":
                import reportlab
                version = reportlab.__version__
            else:
                imported = __import__(lib)
                version = getattr(imported, "__version__", "unknown")
            print(f"{lib:<20} | \033[92m{'PASS':<10}\033[0m | {version:<15}")
        except ImportError as e:
            print(f"{lib:<20} | \033[91m{'FAIL':<10}\033[0m | {'N/A':<15} (Error: {str(e)})")
            all_passed = False
            
    if all_passed:
        print("\nAll dependencies verified successfully. Environment is ready!")
        sys.exit(0)
    else:
        print("\nSome dependencies failed to import. Please check your setup.")
        sys.exit(1)

if __name__ == "__main__":
    verify()
