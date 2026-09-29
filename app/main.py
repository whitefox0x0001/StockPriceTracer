import streamlit
import yfinance as yf
import pandas as pd
import numpy as np
import plotly
from app.health.system_health import system_boot_check
from app.health.system_health import system_health_ok
def main():
    if not(system_boot_check()):
        print("boot failed")
    else:
        system_health_ok()
if __name__ == "__main__":
    main()

