# 69yun 自动签到脚本

本项目旨在实现一个自动化的 69yun 签到脚本，并将签到结果通过 Bark 推送发送给用户。

## 准备工作

在开始之前，请确保您拥有以下账号：

*   GitHub 账号
*   69yun 账号
*   Bark 推送 (用于接收推送通知)

## 使用方法

1.  **Fork 仓库：** 点击 GitHub 页面右上角的 "Fork" 按钮，将本项目 Fork 到您的 GitHub 账号下。

2.  **启用 Actions：** 在您的 Fork 仓库的 "Settings" -> "Actions" -> "General" 中，确保 Actions 处于启用状态。如果显示 "Actions are disabled on this repository"，请选择 "Allow all actions and reusable workflows" 或 "Allow select actions"，然后点击 "Save"。

3.  **设置 GitHub Secrets (环境变量)：**

    在您的 Fork 仓库的 "Settings" -> "Secrets" -> "Actions" 中，添加以下 Secrets：

    *   **`DOMAIN`：** 您的 69yun 域名 (例如：`https://69yun69.com`)。
    *   **`BARK_KEY`：** 您的 Bark Key (用于接收推送通知)。
        *   获取方式：在 App Store 下载 Bark 应用，打开后即可看到您的 Bark Key。
    *   **`BARK_SERVER`：** 您的 Bark 服务器地址 (可选，默认为 `https://api.day.app`)。
        *   如果您使用的是自建的 Bark 服务器，请设置此变量。
    *   **`USER1`：** 第一个 69yun 账号的用户名 (邮箱地址)。
    *   **`PASS1`：** 第一个 69yun 账号的密码。
    *   **`USER2`：** 第二个 69yun 账号的用户名 (邮箱地址)。
    *   **`PASS2`：** 第二个 69yun 账号的密码。
    *   **以此类推，添加更多账号的 `USER(序号)` 和 `PASS(序号)` Secrets。**

4.  **配置 GitHub Actions 工作流：**

    *   本项目使用 GitHub Actions 实现自动化签到。
    *   您无需修改工作流文件 (`.github/workflows/69yuncheckin.yaml`)，除非您需要更改签到频率。
    *   默认情况下，脚本每天 UTC 16:00 执行 (北京时间 00:00)。您可以修改 `cron` 表达式来调整执行时间。

5.  **运行脚本：**

    *   您可以手动触发 GitHub Actions 工作流，或者等待定时任务自动触发。
        *   **手动触发：** 在您的 Fork 仓库的 "Actions" 页面，选择您的工作流，然后点击 "Run workflow"。

## 脚本运行逻辑

1.  脚本会读取您在 GitHub Secrets 中设置的配置信息。
2.  脚本会循环执行每个账号的签到任务。
3.  脚本会将每个账号的签到结果发送到 Bark (如果配置了 `BARK_KEY`)。

## 注意事项

*   请务必保护好您的 GitHub Secrets，不要泄露您的账号密码和 Bark Key。
*   请确保您的 69yun 账号密码正确。
*   如果遇到任何问题，请查看 GitHub Actions 的运行日志，或者提交 Issue。

## 贡献

欢迎提交 Issue 和 Pull Request！

## License

[MIT](LICENSE)

## 感谢

感谢所有为本项目做出贡献的人！
