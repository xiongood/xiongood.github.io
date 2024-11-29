---
title: 手动触发Github Actions
author: 张一雄
summary: 手动触发Github Actions
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/github.jpg
categories:
 - 工具
tags:
 - Github Actions
---



GitHub Actions 是自动化的，通常基于仓库中的事件（如 push、pull request 等）或定时调度来触发。但是，如果你想要手动触发一个 GitHub Actions 工作流（workflow），你可以使用 "repository_dispatch" 事件。

以下是如何设置和手动触发 GitHub Actions 工作流的步骤：

## 不带参数

### 设置工作流以接受 repository_dispatch 事件

在你的 `.github/workflows/` 目录下的 YAML 文件中，添加 `on` 部分以监听 `repository_dispatch` 事件。例如：

```yaml
name: Manual Workflow  
  
on:  
  repository_dispatch:  
    types: [manual-trigger]  
  
jobs:  
  build:  
    name: Build  
    runs-on: ubuntu-latest  
    steps:  
      - name: Hello world  
        run: echo "Hello, world!"
```

注意 `types: [manual-trigger]` 部分，这定义了我们将要用于触发此工作流的自定义事件类型。

### 手动触发工作流

要手动触发此工作流，你需要使用 GiHub API 的 POST 请求到 `/repos/{owner}/{repo}/dispatches` 端点。你可以使用 `curl`、Postman 或其他 HTTP 客户端来发送此请求。

以下是一个使用 `curl` 的示例：

```bash
curl -X POST \  
  -H "Accept: application/vnd.github.everest-preview+json" \  
  -H "Authorization: Bearer <your_personal_access_token>" \  
  https://api.github.com/repos/{owner}/{repo}/dispatches \  
  -d '{"event_type": "manual-trigger"}'
```

![image-20240513092104915](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20240513092107.png)

![image-20240513092118584](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20240513092120.png)

注意：

- `<your_personal_access_token>` 是你的 GitHub 个人访问令牌（Personal Access Token），你需要确保它具有触发仓库 dispatch 的权限。
- `{owner}` 和 `{repo}` 应替换为你的仓库的所有者和名称。
- `-H "Accept: application/vnd.github.everest-preview+json"` 是可选的，用于指定 API 的预览版本（如果 `repository_dispatch` 还在预览中）。但在撰写本文时，它应该已经是 GA（一般可用）了。

1. **检查触发的工作流**

在发送 POST 请求后，你应该能够在 GitHub Actions 的 UI 中看到你的工作流已经开始运行了。你可以转到你的仓库的 "Actions" 选项卡来查看它。

## 带参数

### 配置

```yml
name: 测试工作流
  
on:  
  repository_dispatch:  
    types: [manual-trigger]
  
jobs:  
  build:  
    name: Build  
    runs-on: ubuntu-latest  
    steps:  
      - name: Hello world  
        run: |  
          echo "Key 1: ${{ github.event.client_payload.key1 }}"  
          echo "Key 2: ${{ github.event.client_payload.key2 }}"
```

### 请求参数

```
{
    "event_type": "manual-trigger",
    "client_payload": {
        "key1": "value1",
        "key2": "value2"
    }
}
```
