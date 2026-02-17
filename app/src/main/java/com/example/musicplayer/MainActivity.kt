package com.example.musicplayer

import android.os.Build
import android.os.Bundle
import android.util.Patterns
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.cardview.widget.CardView
import androidx.media3.common.MediaItem
import androidx.media3.common.Player
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.ui.PlayerView
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import coil.load
import com.google.android.material.floatingactionbutton.FloatingActionButton
import com.google.gson.Gson
import com.google.gson.JsonObject
import okhttp3.*
import java.io.IOException

// Data Model
data class Track(val title: String, val author: String, val url: String, val thumbnailUrl: String? = null)

// Adapter
class PlaylistAdapter(
    private val tracks: MutableList<Track>,
    private val onTrackClick: (Int) -> Unit,
    private val onTrackRemove: (Int) -> Unit
) : RecyclerView.Adapter<PlaylistAdapter.ViewHolder>() {

    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val title: TextView = view.findViewById(R.id.itemTitle)
        val author: TextView = view.findViewById(R.id.itemArtist)
        val thumb: ImageView = view.findViewById(R.id.itemThumbnail)
        val btnDelete: ImageButton = view.findViewById(R.id.btnDelete)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_playlist, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val track = tracks[position]
        holder.title.text = track.title
        holder.author.text = track.author
        holder.thumb.load(track.thumbnailUrl ?: android.R.drawable.ic_menu_gallery) {
            crossfade(true)
            placeholder(android.R.drawable.ic_menu_gallery)
        }
        
        holder.itemView.setOnClickListener { onTrackClick(position) }
        holder.btnDelete.setOnClickListener { onTrackRemove(position) }
    }

    override fun getItemCount() = tracks.size
}

class MainActivity : AppCompatActivity() {

    private var player: ExoPlayer? = null
    private lateinit var playerView: PlayerView
    private lateinit var playPauseButton: FloatingActionButton
    private lateinit var btnNext: ImageButton
    private lateinit var btnPrev: ImageButton
    private lateinit var urlInput: EditText
    private lateinit var btnSearch: ImageButton
    private lateinit var playlistView: RecyclerView
    private lateinit var backgroundImage: ImageView
    private lateinit var progressBar: SeekBar

    private val playlist = mutableListOf<Track>()
    private lateinit var adapter: PlaylistAdapter
    private var currentTrackIndex = -1
    private val client = OkHttpClient()
    private val gson = Gson()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Init Views
        playerView = findViewById(R.id.playerView)
        playPauseButton = findViewById(R.id.playPauseButton)
        btnNext = findViewById(R.id.btnNext)
        btnPrev = findViewById(R.id.btnPrev)
        urlInput = findViewById(R.id.urlInput)
        btnSearch = findViewById(R.id.btnSearch)
        playlistView = findViewById(R.id.playlistRecyclerView)
        backgroundImage = findViewById(R.id.backgroundImage)
        progressBar = findViewById(R.id.progressBar)

        // Setup RecyclerView
        adapter = PlaylistAdapter(playlist, { index -> playTrack(index) }, { index -> removeTrack(index) })
        playlistView.layoutManager = LinearLayoutManager(this)
        playlistView.adapter = adapter

        // Setup Listeners
        btnSearch.setOnClickListener { processInput(urlInput.text.toString()) }
        playPauseButton.setOnClickListener { togglePlayPause() }
        btnNext.setOnClickListener { playNext() }
        btnPrev.setOnClickListener { playPrev() }

        initializePlayer()
    }

    private fun processInput(input: String) {
        if (input.isEmpty()) return
        
        if (input.contains("youtube.com") || input.contains("youtu.be")) {
             fetchYoutubeInfo(input)
        } else {
            addTrack(Track("Unknown Title", "Unknown Artist", input))
        }
        urlInput.text.clear()
    }

    private fun fetchYoutubeInfo(url: String) {
        val videoId = extractVideoId(url)
        if (videoId != null) {
            // Using a public Invidious instance API
            val apiUrl = "https://inv.tux.pizza/api/v1/videos/$videoId" 
            val request = Request.Builder().url(apiUrl).build()
            
            client.newCall(request).enqueue(object : Callback {
                override fun onFailure(call: Call, e: IOException) {
                    runOnUiThread { Toast.makeText(this@MainActivity, "Failed to fetch info", Toast.LENGTH_SHORT).show() }
                }

                override fun onResponse(call: Call, response: Response) {
                    response.body?.string()?.let { json ->
                        try {
                            val data = gson.fromJson(json, JsonObject::class.java)
                            val title = data.get("title").asString
                            val author = data.get("author").asString
                            val formatStreams = data.getAsJsonArray("formatStreams")
                            var streamUrl = ""
                            if (formatStreams.size() > 0) {
                                streamUrl = formatStreams.get(0).asJsonObject.get("url").asString
                            }
                            val thumb = "https://img.youtube.com/vi/$videoId/hqdefault.jpg"
                            
                            runOnUiThread {
                                addTrack(Track(title, author, streamUrl, thumb))
                            }
                        } catch (e: Exception) {
                             runOnUiThread { Toast.makeText(this@MainActivity, "Error parsing info", Toast.LENGTH_SHORT).show() }
                        }
                    }
                }
            })
        } else {
             Toast.makeText(this, "Invalid YouTube URL", Toast.LENGTH_SHORT).show()
        }
    }
    
    private fun extractVideoId(url: String): String? {
        val pattern = "(?<=watch\\?v=|/videos/|embed\\/|youtu.be\\/|\\/v\\/|\\/e\\/|watch\\?v%3D|watch\\?feature=player_embedded&v=|%2Fvideos%2F|embed%\u200C\u200B2F|youtu.be%2F|%2Fv%2F)[^#\\&\\?\\n]*"
        val compiled = java.util.regex.Pattern.compile(pattern)
        val matcher = compiled.matcher(url)
        return if (matcher.find()) matcher.group() else null
    }

    private fun addTrack(track: Track) {
        playlist.add(track)
        adapter.notifyItemInserted(playlist.size - 1)
        if (currentTrackIndex == -1) {
            playTrack(0)
        }
    }

    private fun removeTrack(index: Int) {
        playlist.removeAt(index)
        adapter.notifyItemRemoved(index)
        if (index == currentTrackIndex) {
            stopMedia()
            currentTrackIndex = -1
        } else if (index < currentTrackIndex) {
            currentTrackIndex--
        }
    }

    private fun playTrack(index: Int) {
        if (index < 0 || index >= playlist.size) return
        currentTrackIndex = index
        val track = playlist[index]
        
        backgroundImage.load(track.thumbnailUrl)
        playMedia(track.url)
    }

    private fun playNext() {
        if (playlist.isNotEmpty()) {
            val nextIndex = (currentTrackIndex + 1) % playlist.size
            playTrack(nextIndex)
        }
    }

    private fun playPrev() {
         if (playlist.isNotEmpty()) {
            val prevIndex = if (currentTrackIndex - 1 < 0) playlist.size - 1 else currentTrackIndex - 1
            playTrack(prevIndex)
        }
    }

    private fun togglePlayPause() {
        player?.let {
            if (it.isPlaying) {
                it.pause()
                playPauseButton.setImageResource(android.R.drawable.ic_media_play)
            } else {
                it.play()
                playPauseButton.setImageResource(android.R.drawable.ic_media_pause)
            }
        }
    }

    private fun initializePlayer() {
        if (player == null) {
            player = ExoPlayer.Builder(this).build()
            playerView.player = player
            player?.addListener(object : Player.Listener {
                override fun onPlaybackStateChanged(playbackState: Int) {
                    if (playbackState == Player.STATE_ENDED) {
                        playNext()
                    }
                }
                override fun onIsPlayingChanged(isPlaying: Boolean) {
                     playPauseButton.setImageResource(if (isPlaying) android.R.drawable.ic_media_pause else android.R.drawable.ic_media_play)
                }
            })
        }
    }

    private fun playMedia(url: String) {
        initializePlayer()
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

    private fun releasePlayer() {
        player?.release()
        player = null
    }

    override fun onStart() {
        super.onStart()
        if (Build.VERSION.SDK_INT > 23) initializePlayer()
    }

    override fun onResume() {
        super.onResume()
        if (Build.VERSION.SDK_INT <= 23 || player == null) initializePlayer()
    }

    override fun onPause() {
        super.onPause()
        if (Build.VERSION.SDK_INT <= 23) releasePlayer()
    }

    override fun onStop() {
        super.onStop()
        if (Build.VERSION.SDK_INT > 23) releasePlayer()
    }

    override fun onDestroy() {
        super.onDestroy()
        releasePlayer()
    }
}
