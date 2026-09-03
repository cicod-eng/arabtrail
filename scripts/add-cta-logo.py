#!/usr/bin/env python3
# 给含 signup-card 的文章，在卡片头部加平台官方 logo（点击即注册）
import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

binance = ["binance-p2p", "withdraw-usdt", "register-binance", "binance-fees",
           "buy-usdt-saudi-arabia", "binance-kyc"]
okx = ["okx-fees", "is-okx-safe", "okx-kyc", "register-okx", "okx-p2p", "buy-usdt-okx"]

PAT = re.compile(r'(<div class="signup-card">\s*)(<h3>.*?</h3>)', re.DOTALL)


def apply(slug, logos):
    p = ROOT / slug / "index.html"
    html = p.read_text(encoding="utf-8")
    imgs = ""
    for logo, alt in logos:
        imgs += f'          <img src="/assets/{logo}" alt="{alt}" class="signup-logo" width="44" height="44">\n'
    repl = (r'\1'
            '<div class="signup-head">\n'
            + imgs +
            '          ' + r'\2' + '\n'
            '        </div>')
    new, n = PAT.subn(repl, html, count=1)
    if n != 1:
        print(f"!! 未匹配 {slug}")
        return
    p.write_text(new, encoding="utf-8")
    print(f"✓ {slug}")


for s in binance:
    apply(s, [("binance-logo.webp", "Binance")])
for s in okx:
    apply(s, [("okx-logo.webp", "OKX")])
apply("binance-vs-okx", [("binance-logo.webp", "Binance"), ("okx-logo.webp", "OKX")])
