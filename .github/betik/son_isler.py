"""README'deki <!-- son-isler --> bloğunu en son güncellenen açık depolarla doldurur."""
import json, os, pathlib, re, urllib.request

KULLANICI = "FlyerFukas"
README = pathlib.Path(__file__).resolve().parents[2] / "README.md"

istek = urllib.request.Request(
    f"https://api.github.com/users/{KULLANICI}/repos?type=owner&sort=pushed&per_page=30",
    headers={"Accept": "application/vnd.github+json", **({"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"} if os.environ.get("GITHUB_TOKEN") else {})},
)
depolar = [d for d in json.load(urllib.request.urlopen(istek)) if not d["private"] and not d["fork"] and d["name"] != KULLANICI]
satirlar = [
    f"- [{d['name']}]({d['html_url']}) · {d['pushed_at'][:10]}"
    for d in depolar[:5]
]
metin = README.read_text(encoding="utf-8")
yeni = re.sub(
    r"(<!-- son-isler basla -->).*?(<!-- son-isler bitir -->)",
    lambda m: m.group(1) + "\n" + "\n".join(satirlar) + "\n" + m.group(2),
    metin,
    flags=re.S,
)
if yeni != metin:
    README.write_text(yeni, encoding="utf-8")
    print("güncellendi")
else:
    print("değişiklik yok")
