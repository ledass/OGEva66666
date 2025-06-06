from pyrogram import Client, filters
from info import CHANNELS, DATABASE_URI
from database.ia_filterdb import save_file2, save_file3, save_file4, save_file5, check_file

media_filter = filters.document | filters.video | filters.audio

import logging
import re
from pymongo import MongoClient
from datetime import datetime

client = MongoClient(DATABASE_URI)
db = client["autopost"]
collection = db["latest"]
collection_m = db["latestm"]
collection_h = db["latesth"]
collection_e = db["lateste"]
collection_ta = db["latestta"]
collection_te = db["latestte"]
collection_k = db["latestk"]

MOVIE_NAME_PATTERN = r"^(?P<title>.*?)(?=\s+(?:S\d+E\d+|\(\d{4}\)|\d{4}\b|\d+p|WEBRip|BluRay|HDRip|WEB-DL|PreDVD|HEVC|AAC|x264|DD|ESub|\[|\(|-)|\s*$)"
YEAR_PATTERN = r"\b\d{4}\b"
LANGUAGES = r"(?i)\b(tamil|tam|hindi|hin|telugu|tel|malayalam|mal|kannada|kan|english|eng)\b"

async def get_all_movies(col):
    """
    Retrieve all movies in the database in insertion order,
    including their name and year.
    """
    movies = col.find().sort("_id", -1)
    return [{"name": movie["name"], "year": movie.get("year", "N/A")} for movie in movies]

@Client.on_message(filters.command("latest"))
async def handle_latest_command(client, message):
    """
    Handle the /latest command to show all movies in the database
    grouped by language and displayed with better UI.
    """
    # Define the collections for languages
    collections = {
        "Malayalam": collection_m,
        "Tamil": collection_ta,
        "Telugu": collection_te,
        "Hindi": collection_h,
        "English": collection_e,
        "Kannada": collection_k,
        "Uncategorized": collection  # Default collection
    }

    # Prepare the message with movies grouped by language
    response = "🎬 **Latest Movies by Language:**\n\n"
    for language, col in collections.items():
        movies = await get_all_movies(col)
        if movies:
            response += f"**{language}:**\n"
            for movie in movies:
                response += f"• {movie['name']} ({movie['year']})\n"
            response += "\n"

    # Send the message
    if response.strip() != "🎬 **Latest Movies by Language:**":
        await message.reply_text(response)
    else:
        await message.reply_text("No movies found in the database.")

async def maintain_movie_limit(col, MAX_MOVIES):
    movie_count = col.count_documents({})
    if movie_count > MAX_MOVIES:
        oldest_movie = col.find_one(sort=[("_id", 1)])
        if oldest_movie:
            col.delete_one({"_id": oldest_movie["_id"]})
            
async def match_file(caption):
    try:
        # Clean and prepare the file name
        file_name = re.sub(r"📂 Fɪʟᴇ ɴᴀᴍᴇ :", "", caption)
        cleaned = re.sub(r"[.\-]", " ", file_name)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        match = re.match(MOVIE_NAME_PATTERN, cleaned)
        
        if match:
            # Extract the movie name
            movie_name = match.group("title").strip()
            print(f"Extracted Movie Name: {movie_name}")
            
            # Extract the year (if present)
            year_match = re.search(YEAR_PATTERN, file_name)
            year = int(year_match.group(0)) if year_match else None
            print(f"Extracted Year: {year}")

            # Check for language in the caption
            language_match = re.search(LANGUAGES, file_name)
            if language_match:
                language = language_match.group(0).lower()
                # Determine the collection based on the language
                if language in ["malayalam", "mal"]:
                    target_collection = collection_m
                elif language in ["hindi", "hin"]:
                    target_collection = collection_h
                elif language in ["english", "eng"]:
                    target_collection = collection_e
                elif language in ["tamil", "tam"]:
                    target_collection = collection_ta
                elif language in ["telugu", "tel"]:
                    target_collection = collection_te
                elif language in ["kannada", "kan"]:
                    target_collection = collection_k
                else:
                    target_collection = collection
            else:
                # Default collection if no language is found
                target_collection = collection

            # Prepare the document to insert
            today = datetime.now().date()
            today_str = str(today).replace("-", "").replace(" ", "")
            document = {"name": movie_name, "year": year, "today": today_str}

            # Insert the movie into the selected collection if not already present
            if not target_collection.find_one({"name": movie_name}):
                target_collection.insert_one(document)
                await maintain_movie_limit(target_collection, 7)

    except Exception as e:
        logging.info(f"Error in saving latest movie: {e}")
    return 0

@Client.on_message(filters.chat(CHANNELS) & media_filter)
async def media(bot, message):
    """Media Handler"""
    for file_type in ("document", "video", "audio"):
        media = getattr(message, file_type, None)
        if media is not None:
            break
    else:
        return

    media.file_type = file_type
    media.caption = message.caption
    ok = await match_file(message.caption)
    
    if message.id % 3 == 0:
        tru = await check_file(media)
        if tru == "okda":
            await save_file2(media)
        else:
            print("skipped duplicate file from saving to db 😌")
    elif message.id % 4 == 1:
        tru = await check_file(media)
        if tru == "okda":
            await save_file3(media)
        else:
            print("skipped duplicate file from saving to db 😌")    
    else:
        tru = await check_file(media)
        if tru == "okda":
            await save_file4(media)
        else:
            print("skipped duplicate file from saving to db 😌")
