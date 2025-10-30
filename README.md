# ha-jellyfin

A comprehensive Home Assistant integration for Jellyfin media server that provides sensors and media player entities using API key authentication.

## Features

- **Server Status Monitoring**: Track if your Jellyfin server is online/offline
- **Active Sessions**: Monitor who's currently watching and what they're watching
- **Library Statistics**: Get counts of movies, TV shows, episodes, and music tracks
- **Media Player Entities**: Control playback for each Jellyfin user
- **Now Playing Support**: Full media information for now playing cards
- **API Key Authentication**: Secure connection using Jellyfin API keys

## Installation

### Manual Installation

1. Copy the `custom_components/ha-jellyfin` folder to your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant

## Configuration

1. In Home Assistant, go to **Settings** > **Devices & Services**
2. Click **Add Integration**
3. Search for "ha-jellyfin" and select it
4. Fill in the configuration form:
   - **Host**: Your Jellyfin server IP address or hostname
   - **Port**: Your Jellyfin server port (default: 8096)
   - **API Key**: Your Jellyfin API key (see below)
   - **Use SSL**: Enable if your server uses HTTPS

### Getting a Jellyfin API Key

1. Log into your Jellyfin web interface as an administrator
2. Go to **Dashboard** > **API Keys**
3. Click **New API Key**
4. Give it a name (e.g., "Home Assistant")
5. Copy the generated API key

## Entities

### Sensors

The integration provides the following sensors:

- **Server Status**: Shows if the server is online/offline
- **Active Sessions**: Number of currently active streaming sessions
- **Movies**: Count of movies in your library
- **TV Shows**: Count of TV series in your library
- **Episodes**: Count of TV episodes in your library
- **Music**: Count of music tracks in your library

### Media Players

The integration creates a media player entity for each Jellyfin user, allowing you to:

- **Control Playback**: Play, pause, stop, next/previous track
- **Volume Control**: Set volume level and mute/unmute
- **Seek**: Jump to specific positions in media

## Media Player Features

### Supported Controls
- Play/Pause
- Stop
- Next/Previous Track
- Volume Control
- Mute/Unmute
- Seek to Position

### Media Information
- Title, Artist, Album (for music)
- Series, Season, Episode (for TV shows)
- Duration and Current Position
- Media Artwork/Thumbnails
- Production Year, Ratings

### Now Playing Card Support

The media player entities provide comprehensive metadata for Home Assistant's now playing cards:

- **Media Type**: Movie, TV Show, Music, etc.
- **Artwork**: High-quality thumbnails and posters
- **Progress**: Current position and total duration
- **Metadata**: All relevant media information
- **Client Information**: Device and app being used

## Entity Attributes

### Server Status Sensor
- `server_name`: Name of your Jellyfin server
- `version`: Jellyfin server version
- `operating_system`: Server operating system

### Active Sessions Sensor
- `active_sessions`: List of active sessions with details:
  - `user`: Username of the person watching
  - `client`: Client application being used
  - `device`: Device name
  - `media_type`: Type of media (Movie, Episode, etc.)
  - `media_title`: Title of the media being watched

### Media Player Entities
- `session_id`: Current session identifier
- `client`: Client application name
- `device_name`: Name of the playback device
- `user_name`: Jellyfin username
- `media_type`: Type of currently playing media
- `production_year`: Year the media was produced
- `community_rating`: Community rating score
- `official_rating`: Official content rating
- `series_name`: TV series name (for episodes)
- `season_number`: Season number (for episodes)
- `episode_number`: Episode number (for episodes)


### Connection Issues
- Verify your Jellyfin server is accessible from Home Assistant
- Check that the API key is valid and hasn't been revoked
- Ensure the port number is correct
- If using SSL, make sure your certificate is valid

### Media Player Issues
- Some clients may not support all control features

## Support

If you encounter issues:
1. Check the Home Assistant logs for error messages
2. Verify your Jellyfin server is running and accessible
3. Test your API key with a tool like curl or Postman
4. Check Jellyfin server logs for any API-related errors

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
