# a-mitt.github.io

裏世界（a-mitt）の作品置き場。<https://a-mitt.github.io/>
GitHub Pages の Jekyll でそのまま公開される（ビルド設定不要）。

## 更新のしかた

| やりたいこと | 触るファイル |
|---|---|
| 自己紹介・各種リンク | `_data/profile.yml` |
| お知らせ・予告 | `_data/news.yml`（`work:` に作品のファイル名を入れると作品名リンクが付く。`type: 予告` は作品ページの「予告」欄にも出る） |
| 作品の更新履歴（バグ修正など） | `_data/changelog/作品のファイル名.yml`。先頭の日付が「最終更新日」になる |
| 作品を追加 | `_works/` に `.md` を1つ足す。ダウンロード作品は `_templates/download-game.md` をコピー |
| 画像 | `assets/img/`（作品の紹介画像は 16:9 推奨） |

## 多言語（日本語 / English / 한국어 / 简体中文 / 繁體中文）

- 右上のボタンで切り替え。`?lang=en` のように URL でも指定できる。
- 文字列は日本語だけでも OK（訳が無い言語では日本語が出る）。訳を付けるときは `{ ja: ..., en: ..., ko: ..., zh: ..., zh-tw: ... }`（zh は簡体字、zh-tw は繁体字） の形にする。
- 作品ページの本文は `<div data-l="en" markdown="1"> ... </div>` で言語ごとに囲む。
- タグや「公開中」などの決まり文句の訳は `_data/ui.yml`。

ローカル確認（任意）: `gem install jekyll jekyll-seo-tag webrick && jekyll serve`

## 翻訳のチェック

`python tools/translation_check.py` で `translation-check.md` ができる（PyYAML が必要）。中身をそのまま他のAIに渡すと、訳の誤りや不自然な箇所を表で返してくれる。
