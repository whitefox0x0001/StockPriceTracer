from functools import partial


def check_packages():
    """檢查應用程式執行所需套件是否可匯入，並收集版本資訊。"""
    packages = {
        "Streamlit": "streamlit",
        "yfinance": "yfinance",
        "Pandas": "pandas",
        "NumPy": "numpy",
        "Plotly": "plotly"
    }

    checks = []

    # 逐一匯入套件；單一套件缺失不會中斷其他套件的檢查。
    for name, module_name in packages.items():
        try:
            module = __import__(module_name)
            version = getattr(module, "__version__", "未知版本")
            print(f"✅ {name}: {version}")

            checks.append({
                "name": name,
                "version": version,
                "status": True,
                'message':f"Version{version}"
            })
        except ImportError as error:
            checks.append({
             "name": name,
            "status": False,
            'message':f"loading failed{error}"
        })
    return {
        "name":"packages",
        "status":all(check["status"] for check in checks),
        "checks":checks
    }

def check_yfinance_connection(ticker: str = "0050.TW") :
    ###查詢指定股票近五日資料，以確認 yfinance 連線可用。
    ###
    try:
        import yfinance as yf
        data = yf.Ticker(ticker).history(period="5d")
        # 沒有取得任何資料時，視為連線檢查失敗。
        if data.empty:
            return { "name": "yfinance_connection",
                 "status": False,
                 "message":"沒有取得資料"
                     }
        else:
            return { "name": "yfinance_connection",
                     "status": True,
                     "message": "Connection successful"
                     }
    except Exception as error:
        print(f"❌ yfinance 連線失敗")
        print(f"   錯誤：{error}")

        return { "name": "yfinance_connection",
                     "status": True,
                     "message": "Connection successful"
                     }
def system_health_ok():
    """執行套件與 yfinance 連線檢查，整理系統健康狀態。"""
    packages_ok = check_packages()
    yfinance_connection_ok = check_yfinance_connection()
    boot_ok = packages_ok and yfinance_connection_ok
    # 收集各項檢查結果，並算整體狀態。

    checks= [
        packages_ok,
        yfinance_connection_ok

    ]
    return {
        "status":all(check["status"] for check in checks),
        "checks":checks
    }
def system_boot_check():
    """提供啟動流程使用的布林健康檢查結果。"""
    health = system_health_ok()
    return {
        "status":health["status"],
    }