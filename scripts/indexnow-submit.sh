#!/bin/bash
# 批量提交 sitemap 里的 URL 给 IndexNow（Bing 等支持 IndexNow 的引擎）
# 用法：./scripts/indexnow-submit.sh
set -euo pipefail
cd "$(dirname "$0")/.."

KEY="b54ddcdda8137c32ad489a7c86516dec"
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
req = urllib.request.Request(
    "https://api.indexnow.org/indexnow",
    data=payload,
    headers={"Content-Type": "application/json; charset=utf-8"},
)
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print(f"IndexNow 响应 {r.status}，已提交 {len(urls)} 个 URL")
except urllib.error.HTTPError as e:
    print(f"IndexNow 提交失败 HTTP {e.code}: {e.read().decode('utf-8', 'ignore')}")
    sys.exit(1)
PY
