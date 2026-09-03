#!/bin/bash
# 自动生成 sitemap.xml：扫描所有 index.html，输出干净 URL（无 .html）
# 用法：./scripts/generate-sitemap.sh
set -euo pipefail
cd "$(dirname "$0")/.."
BASE="https://arabtrail.com"

{
  echo '<?xml version="1.0" encoding="UTF-8"?>'
  echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
  # 首页
  echo "  <url><loc>${BASE}/</loc><lastmod>$(date -r index.html +%Y-%m-%d)</lastmod></url>"
  # 其余页面（目录内的 index.html）
  find . -name "index.html" -not -path "./.git/*" -not -path "./index.html" | sort | while read -r f; do
    dir="${f#./}"; dir="${dir%/index.html}"
    lm=$(date -r "$f" +%Y-%m-%d)
    echo "  <url><loc>${BASE}/${dir}/</loc><lastmod>${lm}</lastmod></url>"
  done
  echo '</urlset>'
} > sitemap.xml

echo "sitemap.xml 已更新：$(grep -c '<loc>' sitemap.xml) 个 URL"
