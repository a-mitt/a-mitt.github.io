"""他のAIに翻訳チェックを頼むためのファイル（translation-check.md）を作る。

使い方: python tools/translation_check.py   （PyYAML が必要: pip install pyyaml）
"""
import glob
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
LANGS = ["ja", "en", "ko", "zh", "zh-tw"]
NAMES = {"ja": "日本語（原文）", "en": "English", "ko": "한국어", "zh": "简体中文", "zh-tw": "繁體中文（台湾）"}

PROMPT = """\
# 翻訳チェックのお願い

以下は個人の創作サイト（同人ゲームやイラストの紹介ページ）の文章です。
日本語が原文で、英語・韓国語・簡体字中国語・繁体字中国語（台湾向け）に訳してあります。
各言語の訳をチェックして、問題があるものだけ指摘してください。

## 前提
- 作品は漫画『モブサイコ100』の二次創作（ファン作品）です。
- 固有名詞：霊幻新隆 = Reigen Arataka / 레이겐 아라타카 / 灵幻新隆（繁：靈幻新隆）。
  ゲーム内の名前「こや」= Koya、「隆」= Takashi、「ライブラリ」= Library、「本日の主役たすき」= Guest of Honor Sash。
- 日本語版の自己紹介にある「れーれんあららら」は霊幻新隆を指すファンの呼び方です（他言語では霊幻新隆の名前にしています）。
- 文体は、気さくでくだけた個人サイトの口調。堅すぎる表現は避けたいです。
- 繁體中文は台湾の読者向けです。中国本土の言い回しや簡体字が混ざっていたら指摘してください。
- 「裏世界」「a-mitt」は作者名なので訳しません。

## 見てほしい点
1. 誤訳・意味のずれ
2. ネイティブが読んで不自然な表現
3. 文字の誤り（繁体字に簡体字が混ざっている、など）
4. その地域のファンが普段使わない言い方（例：台湾向けで中国本土の用語）

## 回答の形式
問題のあるものだけ、次の表で答えてください。問題が無ければ「問題なし」とだけ書いてください。

| ID | 言語 | 今の訳 | 直した訳 | 理由（日本語で） |
|---|---|---|---|---|
"""


def text(v):
    return v.strip() if isinstance(v, str) else v


def rows_from(obj, path):
    """{ja: ..., en: ...} の形を探して (ID, 訳の辞書) を返す。"""
    if isinstance(obj, dict):
        if "ja" in obj and any(l in obj for l in LANGS[1:]):
            yield path, obj
            return
        for k, v in obj.items():
            yield from rows_from(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from rows_from(v, f"{path}[{i}]")


def main():
    out = [PROMPT]
    n = 0

    def add(rid, d):
        nonlocal n
        n += 1
        out.append(f"\n### {rid}\n")
        for l in LANGS:
            if d.get(l):
                out.append(f"- **{NAMES[l]}**: {text(d[l])}".replace("\n", " / "))

    # 決まり文句（ui.yml はキーが日本語）
    for ja, d in yaml.safe_load((ROOT / "_data/ui.yml").read_text()).items():
        add(f"ui:{ja}", {"ja": ja, **d})

    for f in ["_data/profile.yml", "_data/news.yml", *sorted(glob.glob(str(ROOT / "_data/changelog/*.yml")))]:
        data = yaml.safe_load(Path(ROOT, f).read_text())
        name = Path(f).stem
        for rid, d in rows_from(data, name):
            add(rid, d)

    # 作品ページ（front matter の訳と本文）
    for f in sorted(glob.glob(str(ROOT / "_works/*.md"))):
        src = Path(f).read_text()
        _, fm, body = src.split("---", 2)
        fm = yaml.safe_load(fm)
        slug = Path(f).stem
        for key in ["title", "description"]:
            tr = (fm.get("i18n") or {}).get(key)
            if tr:
                add(f"{slug}.{key}", {"ja": fm[key], **tr})
        blocks = dict(re.findall(r'<div data-l="([\w-]+)" markdown="1">\s*(.*?)\s*</div>', body, re.S))
        if blocks:
            n += 1
            out.append(f"\n### {slug}.本文\n")
            for l in LANGS:
                if l in blocks:
                    out.append(f"#### {NAMES[l]}\n\n{blocks[l]}\n")

    (ROOT / "translation-check.md").write_text("\n".join(out) + "\n")
    print(f"translation-check.md を作成しました（{n} 項目）")


if __name__ == "__main__":
    main()
