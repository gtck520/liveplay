
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
