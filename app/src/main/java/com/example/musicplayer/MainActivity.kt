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
import com.google.gson.JsonArray
import java.security.SecureRandom
import java.security.cert.X509Certificate
import javax.net.ssl.SSLContext
import javax.net.ssl.TrustManager
import javax.net.ssl.X509TrustManager
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
    private lateinit var loadingIndicator: ProgressBar

    private val playlist = mutableListOf<Track>()
    private lateinit var adapter: PlaylistAdapter
    private var currentTrackIndex = -1
    // Fallback Piped Instances (More reliable for Mixes)
    private val pipedInstances = listOf(
        "https://api.piped.projectsegfau.lt",
        "https://pipedapi.tokhmi.xyz",
        "https://pipedapi.kavin.rocks",
        "https://api.piped.privacy.com.de"
    )
    private var currentPipedIndex = 0

    // Fallback Invidious Instances (Updated List)
    private val invidiousInstances = listOf(
        "https://inv.nadeko.net",
        "https://invidious.projectsegfau.lt",
        "https://invidious.nerdvpn.de",
        "https://yewtu.be",
        "https://iv.ggtyler.dev",
        "https://vid.puffyan.us",
        "https://inv.tux.pizza"
    )
    private var currentInstanceIndex = 0

    // Custom Client with User-Agent and Unsafe SSL
    private val client = getUnsafeOkHttpClient()

    private val gson = Gson()

    // Helper to Create Unsafe OkHttpClient (Trusts All Certificates)
    private fun getUnsafeOkHttpClient(): OkHttpClient {
        try {
            // Create a trust manager that does not validate certificate chains
            val trustAllCerts = arrayOf<TrustManager>(object : X509TrustManager {
                override fun checkClientTrusted(chain: Array<out X509Certificate>?, authType: String?) {}
                override fun checkServerTrusted(chain: Array<out X509Certificate>?, authType: String?) {}
                override fun getAcceptedIssuers(): Array<X509Certificate> = arrayOf()
            })

            // Install the all-trusting trust manager
            val sslContext = SSLContext.getInstance("SSL")
            sslContext.init(null, trustAllCerts, SecureRandom())
            val sslSocketFactory = sslContext.socketFactory

            return OkHttpClient.Builder()
                .sslSocketFactory(sslSocketFactory, trustAllCerts[0] as X509TrustManager)
                .hostnameVerifier { _, _ -> true } // Trust all hostnames
                .addInterceptor { chain ->
                    val original = chain.request()
                    val request = original.newBuilder()
                        .header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                        .method(original.method, original.body)
                        .build()
                    chain.proceed(request)
                }
                .build()
        } catch (e: Exception) {
            throw RuntimeException(e)
        }
    }

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
        loadingIndicator = findViewById(R.id.loadingIndicator)

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
        
        if (input.contains("list=")) {
             fetchPlaylistInfo(input)
        } else if (input.contains("youtube.com") || input.contains("youtu.be")) {
             fetchYoutubeInfo(input)
        } else {
            addTrack(Track("Unknown Title", "Unknown Artist", input))
        }
        urlInput.text.clear()
    }

    private fun extractPlaylistId(url: String): String? {
        val pattern = "(?<=list=)[^#\\&\\?]*"
        val compiled = java.util.regex.Pattern.compile(pattern)
        val matcher = compiled.matcher(url)
        return if (matcher.find()) matcher.group() else null
    }

    private fun fetchPlaylistInfo(url: String) {
        val playlistId = extractPlaylistId(url)
        if (playlistId != null) {
            // Priority: Try Piped API first (better support for Mixes/RD playlists)
            fetchPlaylistFromPiped(playlistId, url)
        } else {
             Toast.makeText(this, "Invalid Playlist URL", Toast.LENGTH_SHORT).show()
        }
    }

    private fun fetchPlaylistFromPiped(playlistId: String, originalUrl: String) {
        val instance = pipedInstances[currentPipedIndex]
        val apiUrl = "$instance/playlists/$playlistId"
        
        val request = Request.Builder()
            .url(apiUrl)
            .header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            .build()
        
        runOnUiThread { 
            loadingIndicator.visibility = View.VISIBLE 
            if (currentPipedIndex == 0) {
                Toast.makeText(this, "Fetching via Piped...", Toast.LENGTH_SHORT).show()
            }
        }

        client.newCall(request).enqueue(object : Callback {
             private fun retryPipedOrFallback(errorMsg: String) {
                runOnUiThread {
                    if (currentPipedIndex < pipedInstances.size - 1) {
                        currentPipedIndex++
                        fetchPlaylistFromPiped(playlistId, originalUrl)
                    } else {
                        // All Piped instances failed, fallback to Invidious
                        currentPipedIndex = 0 // Reset
                        fetchPlaylistFromInvidious(playlistId, originalUrl)
                    }
                }
            }

            override fun onFailure(call: Call, e: IOException) {
                retryPipedOrFallback("Network: ${e.message}")
            }

            override fun onResponse(call: Call, response: Response) {
                if (!response.isSuccessful) {
                    retryPipedOrFallback("HTTP ${response.code}")
                    return
                }

                val responseBody = response.body?.string()
                if (responseBody == null) {
                    retryPipedOrFallback("Empty Response")
                    return
                }

                try {
                    val data = gson.fromJson(responseBody, JsonObject::class.java)
                    if (data.has("relatedStreams")) {
                        val videos = data.getAsJsonArray("relatedStreams")
                        val newTracks = mutableListOf<Track>()
                        
                        videos.forEach { videoElement ->
                            try {
                                val video = videoElement.asJsonObject
                                val title = video.get("title").asString
                                val author = video.get("uploaderName").asString // Piped uses uploaderName
                                // Piped provides relative URLs like /watch?v=...
                                val videoUrl = video.get("url").asString
                                val videoId = videoUrl.replace("/watch?v=", "")
                                val thumb = "https://img.youtube.com/vi/$videoId/hqdefault.jpg"
                                val watchUrl = "https://www.youtube.com/watch?v=$videoId"
                                
                                newTracks.add(Track(title, author, watchUrl, thumb))
                            } catch (e: Exception) {
                                // Ignore individual failures
                            }
                        }

                        runOnUiThread {
                            loadingIndicator.visibility = View.GONE
                            if (newTracks.isEmpty()) {
                                retryPipedOrFallback("Empty Piped Playlist")
                                return@runOnUiThread
                            }
                            
                            val startPos = playlist.size
                            playlist.addAll(newTracks)
                            adapter.notifyItemRangeInserted(startPos, newTracks.size)
                            
                            if (currentTrackIndex == -1) {
                                playTrack(0)
                            }
                            Toast.makeText(this@MainActivity, "Added ${newTracks.size} tracks from Piped", Toast.LENGTH_SHORT).show()
                        }
                    } else {
                        retryPipedOrFallback("Invalid Piped JSON")
                    }
                } catch (e: Exception) {
                    retryPipedOrFallback("Piped Parse Error")
                }
            }
        })
    }

    private fun fetchPlaylistFromInvidious(playlistId: String, originalUrl: String) {
        val instance = invidiousInstances[currentInstanceIndex]
        val apiUrl = "$instance/api/v1/playlists/$playlistId"
        
        val request = Request.Builder()
            .url(apiUrl)
            .header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            .build()
        
        runOnUiThread { 
            // Toast.makeText(this, "Falling back to Invidious...", Toast.LENGTH_SHORT).show()
        }

        client.newCall(request).enqueue(object : Callback {
            private fun retryOrShowError(errorMsg: String) {
                runOnUiThread { 
                    if (currentInstanceIndex < invidiousInstances.size - 1) {
                        currentInstanceIndex++
                        fetchPlaylistFromInvidious(playlistId, originalUrl)
                    } else {
                        loadingIndicator.visibility = View.GONE
                        currentInstanceIndex = 0 // Reset
                        val finalError = if (errorMsg.length > 50) errorMsg.substring(0, 50) + "..." else errorMsg
                        Toast.makeText(this@MainActivity, "Failed: $finalError", Toast.LENGTH_LONG).show() 
                    }
                }
            }

            override fun onFailure(call: Call, e: IOException) {
                retryOrShowError("Network: ${e.message}")
            }

            override fun onResponse(call: Call, response: Response) {
                if (!response.isSuccessful) {
                    retryOrShowError("HTTP ${response.code}")
                    return
                }

                val responseBody = response.body?.string()
                if (responseBody == null) {
                    retryOrShowError("Empty Response")
                    return
                }

                try {
                    val data = gson.fromJson(responseBody, JsonObject::class.java)
                    
                    if (data.has("videos")) {
                        val videos = data.getAsJsonArray("videos")
                        val newTracks = mutableListOf<Track>()
                        
                        videos.forEach { videoElement ->
                            try {
                                val video = videoElement.asJsonObject
                                val title = video.get("title").asString
                                val author = video.get("author").asString
                                val videoId = video.get("videoId").asString
                                val thumb = "https://img.youtube.com/vi/$videoId/hqdefault.jpg"
                                val watchUrl = "https://www.youtube.com/watch?v=$videoId"
                                
                                newTracks.add(Track(title, author, watchUrl, thumb))
                            } catch (e: Exception) {
                                // Ignore
                            }
                        }

                        runOnUiThread {
                            loadingIndicator.visibility = View.GONE
                            if (newTracks.isEmpty()) {
                                Toast.makeText(this@MainActivity, "Playlist is empty", Toast.LENGTH_SHORT).show()
                                return@runOnUiThread
                            }
                            
                            val startPos = playlist.size
                            playlist.addAll(newTracks)
                            adapter.notifyItemRangeInserted(startPos, newTracks.size)
                            
                            if (currentTrackIndex == -1) {
                                playTrack(0)
                            }
                            Toast.makeText(this@MainActivity, "Added ${newTracks.size} tracks from Invidious", Toast.LENGTH_SHORT).show()
                        }
                    } else if (data.has("error")) {
                        retryOrShowError("API Error: ${data.get("error").asString}")
                    } else {
                        retryOrShowError("Invalid JSON Structure")
                    }
                } catch (e: Exception) {
                    if (responseBody.trim().startsWith("<")) {
                        retryOrShowError("Server returned HTML (Blocked/Error)")
                    } else {
                        retryOrShowError("JSON Parse Error")
                    }
                }
            }
        })
    }

    private fun fetchYoutubeInfo(url: String) {
        val videoId = extractVideoId(url)
        if (videoId != null) {
            // Use the current instance or default to the first one
            val instance = invidiousInstances[currentInstanceIndex]
            val apiUrl = "$instance/api/v1/videos/$videoId"
            
            val request = Request.Builder()
                .url(apiUrl)
                .header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                .build()
            
            client.newCall(request).enqueue(object : Callback {
                override fun onFailure(call: Call, e: IOException) {
                    runOnUiThread { Toast.makeText(this@MainActivity, "Failed: ${e.message}", Toast.LENGTH_SHORT).show() }
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
                            runOnUiThread { Toast.makeText(this@MainActivity, "Error parsing video info", Toast.LENGTH_SHORT).show() }
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
        
        if (track.url.contains("youtube.com") || track.url.contains("youtu.be")) {
             fetchAndPlayYoutubeVideo(track.url)
        } else {
             playMedia(track.url)
        }
    }

    private fun fetchAndPlayYoutubeVideo(url: String) {
        val videoId = extractVideoId(url) ?: return
        val apiUrl = "https://inv.tux.pizza/api/v1/videos/$videoId"
        val request = Request.Builder().url(apiUrl).build()
        
        Toast.makeText(this, "Loading stream...", Toast.LENGTH_SHORT).show()

        client.newCall(request).enqueue(object : Callback {
             override fun onFailure(call: Call, e: IOException) {
                 runOnUiThread { Toast.makeText(this@MainActivity, "Failed to load stream", Toast.LENGTH_SHORT).show() }
             }
             
             override fun onResponse(call: Call, response: Response) {
                 response.body?.string()?.let { json ->
                     try {
                         val data = gson.fromJson(json, JsonObject::class.java)
                         val formatStreams = data.getAsJsonArray("formatStreams")
                         if (formatStreams.size() > 0) {
                             val streamUrl = formatStreams.get(0).asJsonObject.get("url").asString
                             runOnUiThread { playMedia(streamUrl) }
                         } else {
                             runOnUiThread { Toast.makeText(this@MainActivity, "No stream found", Toast.LENGTH_SHORT).show() }
                         }
                     } catch (e: Exception) {
                         runOnUiThread { Toast.makeText(this@MainActivity, "Error parsing stream info", Toast.LENGTH_SHORT).show() }
                     }
                 }
             }
        })
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
