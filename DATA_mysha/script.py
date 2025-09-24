import os
import csv
import yt_dlp

# Base directory for all songs
base_dir = "pakistani_urdu_songs_1975_1989"
os.makedirs(base_dir, exist_ok=True)

# Master archive file (stores video IDs of all downloaded songs)
archive_file = os.path.join(base_dir, "downloaded_songs.txt")

# yt-dlp options template
def get_ydl_opts(year_dir):
    return {
        'format': 'bestaudio/best[ext=m4a]/best',
        'noplaylist': True,
        'outtmpl': os.path.join(year_dir, '%(id)s_%(title)s.%(ext)s'),  # filename = ID + title
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'ignoreerrors': True,                # skip broken links
        'skip_unavailable_fragments': True,  # skip SABR / missing pieces
        'download_archive': archive_file,  # 🔑 prevents re-downloading duplicates
    }

# Function to download songs for a specific year and log metadata
def download_songs_for_year(year, max_results=20):
    query = f"Pakistani Urdu songs {year}"
    year_dir = os.path.join(base_dir, str(year))
    os.makedirs(year_dir, exist_ok=True)

    # Metadata CSV for this year
    metadata_file = os.path.join(year_dir, f"metadata_{year}.csv")
    if not os.path.exists(metadata_file):
        with open(metadata_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["title", "uploader", "upload_date", "duration",
                             "view_count", "like_count", "id", "webpage_url", "file_path"])

    ydl_opts = get_ydl_opts(year_dir)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"🔎 Searching and downloading top {max_results} songs for year {year}...")
        search_results = ydl.extract_info(f"ytsearch{max_results}:{query}", download=True)

        # Save metadata
        with open(metadata_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for entry in search_results["entries"]:
                if entry is None:
                    continue
                file_path = os.path.join(year_dir, f"{entry['id']}_{entry['title']}.mp3")
                writer.writerow([
                    entry.get("title"),
                    entry.get("uploader"),
                    entry.get("upload_date"),
                    entry.get("duration"),
                    entry.get("view_count"),
                    entry.get("like_count"),
                    entry.get("id"),
                    entry.get("webpage_url"),
                    file_path
                ])
    print(f" Finished year {year}")

# Loop through years 1975–1989
for year in range(1975, 1990):
    download_songs_for_year(year, max_results=20)
