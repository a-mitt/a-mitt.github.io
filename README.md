# a-mitt.github.io

裏世界（a-mitt）の作品置き場。<https://a-mitt.github.io/>
GitHub Pages の Jekyll でそのまま公開される（ビルド設定不要）。

## 更新のしかた

| やりたいこと | 触るファイル |
|---|---|
| 自己紹介・SNSリンク | `_data/profile.yml` |
| お知らせ・更新履歴・予告 | `_data/news.yml`（`work:` に作品のファイル名を入れると作品ページにも出る。`type: 予告` は「予告」欄へ） |
| 作品を追加 | `_works/` に `.md` を1つ足す。ダウンロード作品は `_templates/download-game.md` をコピー |

ローカル確認（任意）: `gem install jekyll jekyll-seo-tag webrick && jekyll serve`
