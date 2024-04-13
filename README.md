
```
1. Install Python
2. Install `pipx`:
   ```
   pip install --user pipx
   ```
3. Ensure `pipx` is in the PATH:
   ```
   pipx ensurepath
   ```
4. Install `edge-tts`:
   ```
   pipx install edge-tts
   ```
5. Download `mpv` from this [link](https://sourceforge.net/projects/mpv-player-windows/files/64bit/mpv-x86_64-20240317-git-3afcaeb.7z/download)

Usage:
- To convert text to speech and save as media and subtitles files:
   ```
   edge-tts --text "Hello, world!" --write-media hello.mp3 --write-subtitles hello.vtt
   ```
- To directly play the speech:
   ```
   edge-playback --text "Hello, world!"
   ```

Available voices:
- `zh-CN-YunxiNeural`: Masculine voice commonly used in Douyin (TikTok)
- `zh-CN-XiaoyiNeural`: Sweet female voice
- `zh-CN-XiaoxiaoNeural`: Normal female voice
```

安装 PyOxidizer：在命令行中运行以下命令来安装 PyOxidizer：

pip install pyoxidizer
创建 PyOxidizer 配置文件：在项目文件夹中创建一个名为 pyoxidizer.toml 的文件，并根据需要进行配置。这个配置文件指定了打包的目标平台、程序入口点等信息。例如，一个简单的 pyoxidizer.toml 配置文件如下所示：

[app]
name = "my_app"
version = "1.0.0"
description = "My awesome Python app"

[python]
version = "3.8.5"
执行打包命令：在命令行中运行以下命令以执行打包：

pyoxidizer build