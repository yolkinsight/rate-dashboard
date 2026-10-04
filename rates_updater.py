import json
import urllib.request
from datetime import datetime

def get_hkma_rates():
    """自動從香港金管局官方 API 抓取最新 1 個月 HIBOR"""
    url = "https://api.hkma.gov.hk/public/market-data-and-statistics/monthly-statistical-bulletin/er-ir/hk-interbank-ir-daily?segment=hibor.fixing&offset=0"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            records = data.get('result', {}).get('records', [])
            return records[0] if records else None
    except Exception as e:
        print(f"HKMA API Error: {e}")
        return None

def main():
    latest = get_hkma_rates()
    if latest and 'ir_1m' in latest:
        hibor_1m = float(latest['ir_1m'])
        report_date = str(latest.get('end_of_day', datetime.now().strftime('%Y-%m-%d')))
    else:
        hibor_1m = 2.968
        report_date = datetime.now().strftime('%Y-%m-%d')

    # Python 切片語法：取月和日 MM/DD
    date_display = report_date[5:].replace('-', '/') if len(report_date) >= 10 else report_date

    # 計算滙豐 H+0.5%
    hsbc_h_rate = round(hibor_1m + 0.5, 3)

    data = {
        "last_updated": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "hibor_1m": f"{hibor_1m:.3f}%",
        "hsbc_rate": f"{hsbc_h_rate:.3f}%",
        "hsbc_date": f"資料 {date_display}",
    }

    with open('rates.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("成功更新 rates.json！")

if __name__ == '__main__':
    main()
