package com.example.musicplayer

import android.os.Build
import android.os.Bundle
import android.util.Patterns
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.media3.common.MediaItem
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.ui.PlayerView

class MainActivity : AppCompatActivity() {

    private var player: ExoPlayer? = null
    private lateinit var playerView: PlayerView
    private lateinit var urlInput: EditText
    private lateinit var playButton: Button
    private lateinit var stopButton: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Inisialisasi View
        playerView = findViewById(R.id.playerView)
        urlInput = findViewById(R.id.urlInput)
        playButton = findViewById(R.id.playButton)
        stopButton = findViewById(R.id.stopButton)

        // Setup Tombol
        playButton.setOnClickListener {
            val url = urlInput.text.toString()
            if (url.isNotEmpty()) {
                playMedia(url)
            } else {
                Toast.makeText(this, "Masukkan URL terlebih dahulu", Toast.LENGTH_SHORT).show()
            }
        }

        stopButton.setOnClickListener {
            stopMedia()
        }
    }

    private fun initializePlayer() {
        if (player == null) {
            player = ExoPlayer.Builder(this).build()
            playerView.player = player
        }
    }

    private fun playMedia(url: String) {
        if (!Patterns.WEB_URL.matcher(url).matches()) {
            Toast.makeText(this, "URL tidak valid. Gunakan link http/https", Toast.LENGTH_SHORT).show()
            return
        }

        initializePlayer()
        
        // Membuat MediaItem dari URL
        val mediaItem = MediaItem.fromUri(url)
        
        player?.apply {
            stop()
            clearMediaItems()
            setMediaItem(mediaItem)
            prepare()
            play()
        }
    }

    private fun stopMedia() {
        player?.stop()
        player?.clearMediaItems()
        player?.seekTo(0)
    }

    override fun onStart() {
        super.onStart()
        if (Build.VERSION.SDK_INT > 23) {
            initializePlayer()
        }
    }

    override fun onResume() {
        super.onResume()
        if (Build.VERSION.SDK_INT <= 23 || player == null) {
            initializePlayer()
        }
    }

    override fun onPause() {
        super.onPause()
        if (Build.VERSION.SDK_INT <= 23) {
            releasePlayer()
        }
    }

    override fun onStop() {
        super.onStop()
        if (Build.VERSION.SDK_INT > 23) {
            releasePlayer()
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        releasePlayer()
    }

    private fun releasePlayer() {
        player?.let {
            it.release()
            player = null
        }
    }
}
