PANDUAN MASALAH SERVER & FITUR CUSTOM INSTANCE
================================================

STATUS SAAT INI (Februari 2026):
--------------------------------
YouTube sedang melakukan pemblokiran agresif terhadap hampir semua instance publik Piped dan Invidious.
- Error "Failed to load stream" atau "HTTP 403/500" disebabkan oleh server (backend) yang diblokir oleh YouTube, BUKAN kesalahan pada aplikasi Android ini.
- Instance populer seperti `api.piped.private.coffee` dan `pipedapi.kavin.rocks` saat ini sedang down/unstable.

SOLUSI YANG DITERAPKAN:
-----------------------
Saya telah memperbarui aplikasi dengan fitur "Custom Piped Instance".

CARA MENGGUNAKAN:
1. Buka aplikasi.
2. Klik tombol "Settings" (ikon gear) di sebelah tombol Log.
3. Masukkan URL instance Piped yang masih bekerja.
   Contoh instance yang mungkin bisa dicoba (cari yang baru/jarang dipakai):
   - https://pipedapi.kavin.rocks (Official, sering down tapi kadang up)
   - https://pipedapi.leptons.xyz
   - https://pipedapi.nosebs.ru
   - Atau cari "Piped instances list" di Google/GitHub untuk instance terbaru.
4. Klik "Save". Aplikasi akan menggunakan server ini sebagai prioritas utama.

JIKA TETAP ERROR:
-----------------
Jika Custom Instance juga gagal, berarti server tersebut juga diblokir. Cobalah URL lain.
Aplikasi ini dirancang untuk mencoba beberapa server secara otomatis, tetapi jika SEMUA server publik mati, satu-satunya cara adalah menunggu server pulih atau menggunakan instance pribadi (self-hosted).

CATATAN TEKNIS:
---------------
Kode aplikasi sudah menggunakan bypass SSL dan User-Agent palsu untuk memaksimalkan kompatibilitas, namun pemblokiran di sisi server (IP ban) tidak bisa dihindari dari sisi klien (aplikasi).
