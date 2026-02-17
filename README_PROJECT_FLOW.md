# Alur Proyek: YouTube Music Player (Versi Android Native Kotlin)

**PERINGATAN: JANGAN GUNAKAN ANDROID STUDIO LOKAL (Disk C Penuh)**
Proyek ini dirancang untuk dikembangkan tanpa perlu menginstal Android Studio atau SDK berat di komputer Anda. Kita menggunakan **GitHub Actions (Cloud Build)**.

Dokumen ini menjelaskan struktur, alur kerja, dan langkah-langkah pengembangan aplikasi pemutar musik berbasis Android Native (Kotlin).

---

## 1. Arsitektur Cloud Build

Karena Disk C penuh, kita menggunakan strategi **Zero-Footprint Development**:
1.  **Lokal (Komputer Anda)**: Hanya menyimpan file kode teks (`.kt`, `.xml`, `.gradle`). Ukurannya sangat kecil (MB).
2.  **Cloud (GitHub)**: Melakukan proses berat (download SDK, compile, build APK).
3.  **Hasil**: Anda tinggal download file APK jadi dari GitHub.

---

## 2. Struktur Folder & File

File kode tetap sama, namun Anda tidak perlu folder `.gradle` atau `build` lokal.

```text
android_versionKOTLIN/
├── build.gradle.kts          (Konfigurasi Project Level)
├── settings.gradle.kts       (Pengaturan Modul)
└── app/
    ├── build.gradle.kts      (Konfigurasi App Level)
    └── src/
        └── main/
            ├── AndroidManifest.xml
            ├── java/.../MainActivity.kt
            └── res/layout/activity_main.xml
```

---

## 3. Cara "Menjalankan" (Build APK Tanpa Android Studio)

Anda tidak bisa menekan tombol "Run" seperti biasa. Ikuti langkah ini:

### Langkah 1: Edit Kode (Gunakan VS Code / Notepad++)
Gunakan editor teks ringan apa saja (VS Code direkomendasikan) untuk mengedit file Kotlin atau XML di folder `android_versionKOTLIN`.

### Langkah 2: Upload ke GitHub
Pastikan folder `d:\COBA_MUSIC` ini terhubung ke repositori GitHub Anda.
1.  Buka terminal di folder ini.
2.  Jalankan perintah Git:
    ```bash
    git add .
    git commit -m "Update kode Android Kotlin"
    git push origin main
    ```

### Langkah 3: Tunggu Build Otomatis
1.  Buka halaman repositori GitHub Anda di browser.
2.  Klik tab **Actions**.
3.  Anda akan melihat proses bernama **"Build Android Native (Kotlin)"** sedang berjalan (berputar kuning).
4.  Tunggu hingga hijau (sukses). Biasanya memakan waktu 2-5 menit.

### Langkah 4: Download APK
1.  Klik pada workflow yang sudah sukses tersebut.
2.  Scroll ke bawah ke bagian **Artifacts**.
3.  Klik **music-player-kotlin-debug** untuk mendownload file `.zip`.
4.  Ekstrak file tersebut, Anda akan mendapatkan `app-debug.apk`.
5.  Kirim ke HP dan install.

---

## 4. Langkah-Langkah Implementasi Kode (Manual)

### Tahap 1: Persiapan Lingkungan (Gradle)
Memastikan alat pembangun (Gradle) tahu perpustakaan apa yang kita butuhkan.
-   **File**: `app/build.gradle.kts`
-   **Aksi**: Menambahkan `implementation("androidx.media3:media3-exoplayer:1.x.x")`. Ini akan mengunduh mesin pemutar otomatis.

### Tahap 2: Izin Akses (Manifest)
Aplikasi butuh internet untuk memutar lagu.
-   **File**: `AndroidManifest.xml`
-   **Aksi**: Menambahkan `<uses-permission android:name="android.permission.INTERNET" />`.

### Tahap 3: Merancang Tampilan (XML)
Membuat antarmuka pengguna.
-   **File**: `activity_main.xml`
-   **Komponen**:
    -   `EditText`: Untuk menempelkan link lagu.
    -   `Button`: Tombol "PLAY" dan "STOP".
    -   `PlayerView`: Komponen visual dari ExoPlayer.

### Tahap 4: Menulis Logika Pemutar (Kotlin)
Otak aplikasi.
-   **File**: `MainActivity.kt`
-   **Alur Logika**:
    1.  **Inisialisasi**: Siapkan `ExoPlayer` saat aplikasi dibuka.
    2.  **Input User**: Ambil teks URL saat tombol ditekan.
    3.  **Proses Media**: Buat `MediaItem` dari URL.
    4.  **Play**: Instruksikan `ExoPlayer` untuk memutar media.
    5.  **Cleanup**: Lepaskan memori player saat aplikasi ditutup (`onDestroy`).

---

**Dibuat otomatis oleh Asisten AI untuk Proyek Music Player (Mode Hemat Disk).**
