# Music Player Kotlin (Android)

A modern Android Music Player built with Kotlin, featuring YouTube playback, playlist management, and a clean UI.

## Features

- **YouTube Playback**: Play audio from YouTube videos directly.
- **Playlist Support**: 
  - Paste a YouTube Playlist URL (e.g., `https://youtube.com/playlist?list=...`) to import all tracks automatically.
  - Supports standard video URLs (e.g., `https://youtube.com/watch?v=...`).
- **Local Playback**: Manage a local queue of tracks.
- **Background Playback**: Continues playing audio even when the app is in the background.
- **Modern UI**: Clean interface with dynamic background and smooth transitions.

## How to Build

This project uses **GitHub Actions** for CI/CD. Every push to the `main` branch automatically triggers a build and generates an APK.

1. Go to the **Actions** tab in this repository.
2. Select the latest workflow run.
3. Download the `music-player-kotlin-debug` artifact (APK).

## Technologies Used

- **Kotlin**: Primary language.
- **ExoPlayer**: For robust media playback.
- **OkHttp**: For networking and API requests.
- **Gson**: For JSON parsing.
- **Coil**: For image loading.
- **Invidious API**: For fetching YouTube video metadata without an API key.
