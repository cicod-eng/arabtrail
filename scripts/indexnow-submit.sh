#!/bin/bash
# 批量提交 sitemap 里的 URL 给 IndexNow（Bing 等支持 IndexNow 的引擎）
# 用法：./scripts/indexnow-submit.sh
set -euo pipefail
cd "$(dirname "$0")/.."

KEY="5c0eac9948e44c07aa3e7aead6d3a4b0"
HOST="arabtrail.com"

# 从 sitemap.xml 提取全部 <loc> URL
python3 - "$KEY" "$HOST" <<'PY'
import json, re, sys, urllib.request
key, host = sys.argv[1], sys.argv[2]
xml = open("sitemap.xml", encoding="utf-8").read()
urls = re.findall(r"<loc>(.*?)</loc>", xml)
payload = json.dumps({
    "host": host,
    "key": key,
    "keyLocation": f"https://{host}/{key}.txt",
    "urlList": urls,
}).encode("utf-8")
for endpoint in ("https://api.indexnow.org/indexnow", "https://www.bing.com/indexnow"):
    req = urllib.request.Request(
        endpoint, data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"{endpoint} 响应 {r.status}，已提交 {len(urls)} 个 URL")
    except urllib.error.HTTPError as e:
        print(f"{endpoint} 提交失败 HTTP {e.code}: {e.read().decode('utf-8', 'ignore')}")
PY
