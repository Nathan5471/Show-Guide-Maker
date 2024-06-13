import sqlite3
import os
import re
import random
import shutil
import subprocess
import moviepy.editor as mp

# DB table information
# showInformation(name, episodesPerRun, folderLocation, position, audio, video)
# show(episodes)
# previousMain(fileNumber)
# previousShow(show, episode, id)


def addShow(name, folderLocation, episodesPerRun, audio, video):
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS showInformation(name, episodesPerRun, folderLocation, audio, video)"
    )
    values = (name, episodesPerRun, folderLocation, audio, video)
    cursor.execute(
        f"INSERT INTO showInformation(name, episodesPerRun, folderLocation, audio, video) VALUES {values}",
    )
    cursor.execute(f"CREATE TABLE '{name}'(episodes)")
    seasons = list(
        filter(lambda item: "Season" in item, os.listdir(f"{folderLocation}"))
    )
    if "Season 00" in seasons:
        while True:
            season0Check = input(
                "Season 00 found, would you like to remove it? [y/n]: "
            )
            if season0Check == "y":
                seasons.remove("Season 00")
                break
            elif season0Check == "n":
                break
            else:
                print("please enter y or n")
    episodesTotal = 0
    for season in seasons:
        episodes = list(
            filter(
                lambda item: "Episode" in item, os.listdir(f"{folderLocation}/{season}")
            )
        )

        episodesTotal += len(episodes)
        for episode in episodes:
            cursor.execute(f"INSERT INTO '{name}'(episodes) VALUES ('{episode}')")
    connection.commit()
    connection.close()
    return (True, len(seasons), episodesTotal)


def removeShow(showName):
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM showInformation WHERE name = '{showName}'")
    cursor.execute(f"DROP TABLE '{showName}'")
    connection.commit()
    connection.close()
    return True


def getShows():
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS showInformation(name, episodesPerRun, folderLocation, audio, video)"
    )
    cursor.execute("SELECT name FROM showInformation")
    shows = cursor.fetchall()
    for show in shows:
        showString = str(show).replace("('", "")
        showString = showString.replace("',)", "")
        shows[shows.index(show)] = showString
    connection.commit()
    connection.close()
    return shows


def getShowInformation(showName):
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM showInformation WHERE name = "{showName}"')
    showInformation = cursor.fetchone()
    connection.commit()
    connection.close()
    return showInformation


def getEpisodeCount(showName):
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM '{showName}'")
    episodes = cursor.fetchall()
    seasons = []
    episodeCount = 0
    for episode in episodes:
        episode = str(episode)
        season = re.search(r"S(\d+)", episode)
        season = season.group(1)
        if not season in seasons:
            seasons.append(season)
        episodeCount += 1
    connection.commit()
    connection.close()
    return (episodeCount, len(seasons))


def changeShowName(currentName, newName):
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute(f"ALTER TABLE '{currentName}' RENAME TO '{newName}'")
    cursor.execute(
        f"UPDATE showInformation SET name = '{newName}' WHERE name = '{currentName}'"
    )
    connection.commit()
    connection.close()
    return True


def changeShowFolder(showName, newFolderLocation):
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute(
        f"UPDATE showInformation Set folderLocation = '{newFolderLocation}' WHERE name = '{showName}'"
    )
    seasons = list(
        filter(lambda item: "Season" in item, os.listdir(f"{newFolderLocation}"))
    )
    episodesTotal = 0
    cursor.execute(f"DELETE FROM '{showName}'")
    for season in seasons:
        episodes = list(
            filter(
                lambda item: "Episode" in item,
                os.listdir(f"{newFolderLocation}/{season}"),
            )
        )
        episodesTotal += len(episodes)
        for episode in episodes:
            cursor.execute(f"INSERT INTO '{showName}'(episodes) VALUES ('{episode}')")
    connection.commit()
    connection.close()
    return (True, len(seasons), episodesTotal)


def changeEpisodePerRun(showName, episodesPerRun):
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute(
        f"UPDATE showInformation SET episodesPerRun = {episodesPerRun} WHERE name = '{showName}'"
    )
    connection.commit()
    connection.close()
    return True


def changeTranscode(showName, audio, video):
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute(
        f"UPDATE showInformation SET audio = '{audio}', video = '{video}' WHERE name = '{showName}'"
    )
    connection.commit()
    connection.close()
    return True


def addMovie(movieName, folderLocation, audioTranscode, videoTranscode):
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS movieInformation(name, folderLocation, audio, video)"
    )
    cursor.execute(
        f"INSERT INTO movieInformation(name, folderLocation, audio, video) VALUES ('{movieName}', '{folderLocation}', '{audioTranscode}', '{videoTranscode}')",
    )
    connection.commit()
    connection.close()
    return True


def getMovies():
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS movieInformation(name, folderLocation, audio, video)"
    )
    cursor.execute("SELECT name FROM movieInformation")
    movies = cursor.fetchall()
    for movie in movies:
        movieString = str(movie).replace("('", "")
        movieString = movieString.replace("',)", "")
        movies[movies.index(movie)] = movieString
    connection.commit()
    connection.close()
    return movies


def editMovieName(currentName, newName):
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute(
        f"UPDATE movieInformation SET name = '{newName}' WHERE name = '{currentName}'"
    )
    connection.commit()
    connection.close()
    return True


def editMovieFolder(movieName, newFolderLocation):
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute(
        f"UPDATE movieInformation SET folderLocation = '{newFolderLocation}' WHERE name = '{movieName}'"
    )
    connection.commit()
    connection.close()
    return True


def editMovieTranscode(movieName, audioTranscode, videoTranscode):
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute(
        f"UPDATE movieInformation SET audio = '{audioTranscode}', video = '{videoTranscode}' WHERE name = '{movieName}'"
    )
    connection.commit()
    connection.close()
    return True


def removeMovie(movieName):
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM movieInformation WHERE name = '{movieName}'")
    connection.commit()
    connection.close()
    return True


def getMovieInformation(movieName):
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM movieInformation WHERE name = "{movieName}"')
    movieInformation = cursor.fetchone()
    connection.commit()
    connection.close()
    return movieInformation


def editShowOrder(showOrder):
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS showOrder(showOrder)")
    cursor.execute("DELETE FROM showOrder")
    showOrder = str(showOrder)
    cursor.execute(f"INSERT INTO showOrder(showOrder) VALUES (?)", (showOrder,))
    connection.commit()
    connection.close()
    return True


def checkShowOrder():
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM showOrder")
    showOrder = cursor.fetchall()
    if not showOrder:
        return False
    else:
        return True


def getRandomMovie():
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM movieInformation")
    movies = cursor.fetchall()
    return random.choice(movies)[0]


def createShowOrder(orderLength):
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM showOrder")
    order = cursor.fetchone()[0]
    order = order.replace("[", "")
    order = order.replace("]", "")
    order = order.replace("'", "")
    order = order.split(", ")
    cursor.execute("CREATE TABLE IF NOT EXISTS previousMain(fileNumber)")
    cursor.execute("CREATE TABLE IF NOT EXISTS previousShow(show, episode, id)")
    episodeCount = 1
    currentRun = 1
    showOrder = []
    while True:
        for show in order:
            if show == "Movie":
                episodeCount += 1
                movie = getRandomMovie()
                showOrder.append(("Movie", movie))
                if episodeCount > orderLength:
                    connection.commit()
                    connection.close()
                    return showOrder
                continue
            showInformation = getShowInformation(show)
            while True:
                cursor.execute(f"SELECT 1 FROM previousShow WHERE show = '{show[0]}'")
                enteryExist = cursor.fetchone()
                episodesPerRun = showInformation[1]
                if not enteryExist:
                    cursor.execute(f"SELECT * FROM '{show}' LIMIT 1")
                    episode = cursor.fetchone()
                    showOrder.append((show, episode[0]))
                    cursor.execute(
                        f"INSERT INTO previousShow(show, episode, id) VALUES ('{show}', '{episode[0]}', 1)"
                    )
                    currentRun += 1
                    episodeCount += 1
                else:
                    cursor.execute(f"SELECT * FROM previousShow WHERE show = '{show}'")
                    previousEpisode = cursor.fetchone()
                    cursor.execute(
                        f"SELECT * FROM '{show}' WHERE ROWID IN (SELECT max(ROWID) FROM '{show}')"
                    )
                    lastEpisode = cursor.fetchone()
                    if previousEpisode[1] != lastEpisode[0]:
                        cursor.execute(
                            f"SELECT * FROM '{show}' LIMIT 1 OFFSET {previousEpisode[2]}"
                        )
                        episode = cursor.fetchone()
                        cursor.execute(
                            f"UPDATE previousShow SET episode = '{episode[0]}', id = {previousEpisode[2] + 1} WHERE show = '{show[0]}'"
                        )
                    else:  # Fixes show hitting the last episode
                        cursor.execute(f"SELECT * FROM '{show}' LIMIT 1")
                        episode = cursor.fetchone()
                        cursor.execute(
                            f"UPDATE previousShow SET episode = '{episode[0]}', id = 1 WHERE show = '{show}'"
                        )

                    showOrder.append((show, episode[0]))
                    currentRun += 1
                    episodeCount += 1
                if episodeCount > orderLength:
                    connection.commit()
                    connection.close()
                    return showOrder
                if currentRun > episodesPerRun:
                    currentRun = 1
                    break
        if episodeCount > orderLength:
            connection.commit()
            connection.close()
            return showOrder
        else:
            continue


def storeDriveLocation(driveLocation):
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS driveLocation(location)")
    cursor.execute(f"INSERT INTO driveLocation(location) VALUES ('{driveLocation}')")
    connection.commit()
    connection.close()
    return True


def getDriveLocations():
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS driveLocation(location)")
    cursor.execute("SELECT location FROM driveLocation")
    locations = cursor.fetchall()
    for location in locations:
        locationString = str(location).replace("('", "")
        locationString = locationString.replace("',)", "")
        locations[locations.index(location)] = locationString
    connection.commit()
    connection.close()
    return locations


def copyShow(showName, episodeLocation, episode, fileNumber, destination):
    shutil.copy(episodeLocation, f"{destination}/{fileNumber} - {showName} {episode}")


def transcodeShow(
    showName,
    episodeLocation,
    episode,
    fileNumber,
    destination,
    audio,
    video,
    videoBitrate,
    hardwareAcceleration,
):
    if hardwareAcceleration == "None":
        subprocess.run(
            f'ffmpeg -i "{episodeLocation}" -c:v {video} -b:v {videoBitrate} -c:a {audio} "{destination}/{fileNumber} - {showName} {episode}"'
        )
    elif hardwareAcceleration == "qsv":
        subprocess.run(
            f'ffmpeg -hwaccel qsv -hwaccel_output_format qsv -i "{episodeLocation}" -vf scale_qsv=format=nv12 -c:v {video}_qsv -b:v {videoBitrate} -c:a {audio} "{destination}/{fileNumber} - {showName} {episode}"'
        )


def transcodeMovie(
    movieLocation,
    movieName,
    destination,
    fileNumber,
    fileExtension,
    audio,
    video,
    videoBitrate,
    hardwareAcceleration,
):

    if hardwareAcceleration == "None":
        subprocess.run(
            f'ffmpeg -i "{movieLocation}" -c:v {video} -b:v {videoBitrate} -c:a {audio} "{destination}/{fileNumber} - {movieName}.{fileExtension}"'
        )
    elif hardwareAcceleration == "qsv":
        subprocess.run(
            f'ffmpeg -hwaccel qsv -i "{movieLocation}" -vf scale_qsv=format=nv12 -c:v {video}_qsv -b:v {videoBitrate} -c:a {audio} "{destination}/{fileNumber} - {movieName}.{fileExtension}"'
        )


def copyMovie(movieName, movieLocation, fileNumber, destination, fileExtension):
    shutil.copy(
        movieLocation, f"{destination}/{fileNumber} - {movieName}.{fileExtension}"
    )


def generateSettings():
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS settings(videoCodec, audioCodec, maxBitrate, hardwareAcceleration, moviesPerRun)"
    )
    cursor.execute("SELECT * FROM settings")
    settings = cursor.fetchall()
    if not settings:
        cursor.execute(
            "INSERT INTO settings(videoCodec, audioCodec, maxBitrate, hardwareAcceleration, moviesPerRun) VALUES ('h264', 'aac', '100M', 'None', 0)"
        )
    connection.commit()
    connection.close()


def editVideoCodec(videoCodec):
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute(f"UPDATE settings SET videoCodec = '{videoCodec}' WHERE ROWID = 1")
    connection.commit()
    connection.close()
    return True


def editAudioCodec(audioCodec):
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute(f"UPDATE settings SET audioCodec = '{audioCodec}' WHERE ROWID = 1")
    connection.commit()
    connection.close()
    return True


def editMaxBitrate(maxBitrate):
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute(f"UPDATE settings SET maxBitrate = '{maxBitrate}' WHERE ROWID = 1")
    connection.commit()
    connection.close()
    return True


def editHardwareAcceleration(hardwareAcceleration):
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute(
        f"UPDATE settings SET hardwareAcceleration = '{hardwareAcceleration}' WHERE ROWID = 1"
    )
    connection.commit()
    connection.close()
    return True


def editMoviesPerRun(moviesPerRun):
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute(f"UPDATE settings SET moviesPerRun = {moviesPerRun} WHERE ROWID = 1")
    connection.commit()
    connection.close()
    return True


def getSettings():
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM settings")
    settings = cursor.fetchall()
    connection.commit()
    connection.close()
    return settings[0]


def calculateBitrate(videoLocation):
    video = mp.VideoFileClip(videoLocation)
    videoLength = video.duration
    videoSize = os.path.getsize(videoLocation)
    bitrate = (videoSize * 8 / videoLength) / 1000
    return bitrate  # Returns in kbps
