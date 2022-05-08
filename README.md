# pyOCR
基于python的OCR软件，调用百度开放API接口实现OCR识别与翻译。界面使用tkinter编写。

## 使用方法
```
pythonw pyOCR.v0.1.5.py
```

## 其他补充说明
1. 依赖的软件包
    ```
    tkinter, PIL, time, ctypes, pyautogui, requests, base64, hashlib, json, os
    ```
    如果提示缺少相应的软件包，则使用`pip`或`conda`安装

2. 功能模式
    软件定义了两种OCR识别模式，一种叫做`截图`，一种叫做`识别剪贴板`。
    1. `截图`模式：
        软件会先截取整个屏幕，并在新窗口中展示截图。之后，用户使用鼠标在截图上先后点击两次，以框定识别区域。软件将在这两次点击位置所确定的矩形区域中进行OCR识别，并在文本框中显示。
    3. `识别剪贴板`模式：
        用户先使用windows系统自带的截图功能进行截图，截取的图片默认会保留在剪贴板中。之后，点击这一按钮即可识别截图。
3. `原文/翻译` 按钮：
    软件调用百度翻译开放API进行翻译，翻译模式为中英互译（如有其他语言的翻译需要，请在代码中进行修改）。
    请注意，当软件显示译文时，文本框内的文字不可编辑。可以先手动调整好文本框中的原文再翻译。

4. 跨平台问题？
    目前仅在Windows平台进行过测试，但由于tkinter是一个跨平台的GUI库，理论上可以在Linux/macOS上完美运行。如有疑问，欢迎反馈。

## 联系作者
QQ: 1738296705
邮箱同号。

