import sqlite3
import os
import re
import shutil
import ffmpeg

# DB table information
# showInformation(name, episodesPerRun, folderLocation, position, audio, video)
# show(episodes)
# previousMain(fileNumber)
# previousShow(show, episode, id)


def addShow(name, folderLocation, episodesPerRun, audio, video):
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS showInformation(name, episodesPerRun, folderLocation, position, audio, video)"
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
        "CREATE TABLE IF NOT EXISTS showInformation(name, episodesPerRun, folderLocation, position)"
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
    cursor.execute(f"SELECT * FROM showInformation WHERE name = '{showName}'")
    showInformation = cursor.fetchall()
    connection.commit()
    connection.close()
    return showInformation[0]


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


def checkShowPositionExist():  # Check if every show has a position
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute("SELECT position FROM showInformation")
    positions = cursor.fetchall()
    for position in positions:
        if position[0] == None:
            return False
    return True


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


def changeShowPosition(showName, position):
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute(
        f"UPDATE showInformation SET position = {position} WHERE name = '{showName}'"
    )
    connection.commit()
    connection.close()
    return True


def createShowOrder(orderLength):
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM showInformation")
    showsInformation = cursor.fetchall()
    showsInformation = sorted(showsInformation, key=lambda x: x[3])
    cursor.execute("CREATE TABLE IF NOT EXISTS previousMain(fileNumber)")
    cursor.execute("CREATE TABLE IF NOT EXISTS previousShow(show, episode, id)")
    showOrder = []
    episodeCount = 1
    currentRun = 1
    while True:
        for show in showsInformation:
            while True:
                cursor.execute(f"SELECT 1 FROM previousShow WHERE show = '{show[0]}'")
                enteryExist = cursor.fetchone()
                episodesPerRun = showsInformation[showsInformation.index(show)][1]
                if not enteryExist:
                    cursor.execute(f"SELECT * FROM '{show[0]}' LIMIT 1")
                    episode = cursor.fetchone()
                    showOrder.append((show[0], episode[0]))
                    cursor.execute(
                        f"INSERT INTO previousShow(show, episode, id) VALUES ('{show[0]}', '{episode[0]}', 1)"
                    )
                    currentRun += 1
                    episodeCount += 1
                else:
                    cursor.execute(
                        f"SELECT * FROM previousShow WHERE show = '{show[0]}'"
                    )
                    previousEpisode = cursor.fetchone()
                    cursor.execute(
                        f"SELECT * FROM '{show[0]}' WHERE ROWID IN (SELECT max(ROWID) FROM '{show[0]}')"
                    )
                    lastEpisode = cursor.fetchone()
                    if previousEpisode[1] != lastEpisode[0]:
                        cursor.execute(
                            f"SELECT * FROM '{show[0]}' LIMIT 1 OFFSET {previousEpisode[2]}"
                        )
                        episode = cursor.fetchone()
                        cursor.execute(
                            f"UPDATE previousShow SET episode = '{episode[0]}', id = {previousEpisode[2] + 1} WHERE show = '{show[0]}'"
                        )
                    else:  # Fixes show hitting the last episode
                        cursor.execute(f"SELECT * FROM '{show[0]}' LIMIT 1")
                        episode = cursor.fetchone()
                        cursor.execute(
                            f"UPDATE previousShow SET episode = '{episode[0]}', id = 1 WHERE show = '{show[0]}'"
                        )

                    showOrder.append((show[0], episode[0]))
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
    showName, episodeLocation, episode, fileNumber, destination, audio, video
):
    ffmpeg.input(episodeLocation).output(
        f"{destination}/{fileNumber} - {showName} {episode}",
        acodec=audio,
        vcodec=video,
    ).run()
