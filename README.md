# 留白

一个无需依赖的静态个人博客。首页、文章页和样式都在 `dist/`，可以直接部署为静态网站。

## 写新文章

1. 在 `content/posts/` 新建一个 `.md` 文件。文件名会成为文章网址。
2. 按现有文章填写标题、日期、分类、摘要和阅读时间，并在下方写正文。
3. 在本目录运行 `python3 build.py`，重新生成首页和文章页。

目前支持段落、二级标题、引用和无序列表。站名和首页介绍在 `templates/index.html`；文章页的站名在 `build.py`。样式在 `dist/styles.css`。

## 发布到 GitHub Pages

这个目录已包含 GitHub Actions 发布流程。把全部文件推送到 GitHub 用户名对应的 `<用户名>.github.io` 仓库的 `main` 分支，并在仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**。每次推送后，工作流会生成并发布网站。

要得到 `https://DontBeSleepy.github.io/`，GitHub 账号名必须是 `DontBeSleepy`，仓库名必须是 `DontBeSleepy.github.io`。GitHub 用户名与域名大小写不敏感。
