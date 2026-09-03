#!/usr/bin/env python3
"""拉取 Bing Webmaster Tools 数据（arabtrail.com）

用法：
  python3 scripts/bing-fetch.py <API_KEY>

API Key 获取：Bing Webmaster Tools → 右上齿轮⚙ → API 访问 → 生成密钥
鉴权方式：apikey 作为 query 参数（实测有效；Authorization Bearer 会报 InvalidToken）

可用端点（实测）：
  GetUserSites          站点列表 + IsVerified
  GetUrlSubmissionQuota 提交配额（DailyQuota/MonthlyQuota）
  GetRankAndTrafficStats 排名流量（新站为空）
  GetPageStats          页面统计（新站为空）
注：Bing 官方 API 无直接「已索引页面数」端点，该数字只在 WMT 后台首页显示。
"""
import json, sys, urllib.request, urllib.parse

BASE = "https://ssl.bing.com/webmaster/api.svc/json/"

def call(method, key, params=None):
    params = dict(params or {})
    params["apikey"] = key
    url = BASE + method + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        print(f"  [HTTP {e.code}] {method}: {e.read().decode('utf-8','ignore')[:200]}")
        return None
    except Exception as e:
        print(f"  [错误] {method}: {e}")
        return None

SITE = "https://arabtrail.com/"

def show_sites(key):
    print("=== 站点状态 (GetUserSites) ===")
    r = call("GetUserSites", key)
    if not r:
        return
    for s in (r.get("d") or []):
        if isinstance(s, dict):
            print(json.dumps({
                "Url": s.get("Url"),
                "IsVerified": s.get("IsVerified"),
            }, ensure_ascii=False, indent=2))

def show_quota(key):
    print("\n=== URL 提交配额 (GetUrlSubmissionQuota) ===")
    r = call("GetUrlSubmissionQuota", key, {"siteUrl": SITE})
    if r:
        d = r.get("d") or {}
        print(f"  每日配额: {d.get('DailyQuota')}  ·  每月配额: {d.get('MonthlyQuota')}")

def show_traffic(key):
    print("\n=== 排名流量 (GetRankAndTrafficStats) ===")
    r = call("GetRankAndTrafficStats", key, {"siteUrl": SITE})
    d = (r or {}).get("d") or []
    print(f"  数据行数: {len(d)}" + ("（新站，暂无流量数据）" if not d else ""))

def show_pagestats(key):
    print("\n=== 页面统计 (GetPageStats) ===")
    r = call("GetPageStats", key, {"siteUrl": SITE})
    d = (r or {}).get("d") or []
    print(f"  数据行数: {len(d)}" + ("（新站，暂无页面级数据）" if not d else ""))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    key = sys.argv[1]
    show_sites(key)
    show_quota(key)
    show_traffic(key)
    show_pagestats(key)
