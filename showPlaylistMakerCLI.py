import os.path
from showPlaylistMaker import *


def mainMenu():
    # The main menu
    print("")
    print("-------------------")
    print("1) Add show")
    print("2) Edit show")
    print("3) Remove show")
    print("4) Get shows")
    print("5) Change order")
    print("6) Create playlist")
    print("7) Settings")
    print("-------------------")
    print("")

    try:
        selection = int(input("Enter Your Selection: "))
    except ValueError:
        print("Please input a valid number")
        mainMenu()

    if selection == 1:
        addShowCLI()

    elif selection == 2:
        editShowCLI()

    elif selection == 3:
        removeShowCLI()

    elif selection == 4:
        getShowsCLI()

    elif selection == 5:
        changeOrderCLI()

    elif selection == 6:
        createPlaylistCLI()

    elif selection == 7:
        settingsCLI()

    else:
        print("Please select a valid number")
        mainMenu()


def addShowCLI():
    transcodeSettings = getSettings()
    showName = input("Enter the name of the show you want to add: ")
    while True:
        folderLocation = input("Enter the location of the folder: ")
        if os.path.exists(folderLocation):
            break
        else:
            print(
                "Folder location does not exists, please input a valid folder location"
            )
            continue
    while True:
        try:
            episodesPerRun = int(
                input("Enter the number of episodes you want per cycle: ")
            )
        except ValueError:
            print("Please input a integer")
            continue
        break
    while True:
        audioTranscode = input("Do you want to transcode the audio [y/n]: ")
        if audioTranscode == "y":
            audioTranscode = transcodeSettings[1]
            break
        elif audioTranscode == "n":
            audioTranscode = "copy"
            break
        else:
            print("Please input y or n")
    while True:
        videoTranscode = input("Do you want to transcode the video [y/n]: ")
        if videoTranscode == "y":
            videoTranscode = transcodeSettings[0]
            break
        elif videoTranscode == "n":
            videoTranscode = "copy"
            break
        else:
            print("Please input y or n")
    result = addShow(
        showName, folderLocation, episodesPerRun, audioTranscode, videoTranscode
    )
    if result[0]:
        print("")
        print("The show was added succesfully, but to confirm here is the information")
        print(f"Name: {showName}")
        print(f"Episodes per cycle: {episodesPerRun}")
        print(f"Audio transcode: {audioTranscode}")
        print(f"Video transcode: {videoTranscode}")
        print(f"Seasons: {result[1]}")
        print(f"Episodes: {result[2]}")
        print("")
        while True:
            informationIsCorrect = input("Is this information correct [y/n]: ")
            if informationIsCorrect == "y":
                print(f"{showName} has been added!")
                mainMenu()
            elif informationIsCorrect == "n":
                removeShow(showName)
                print("Show has not been added")
                mainMenu()
            else:
                print("Please input y or n")


def editShowCLI():
    shows = getShows()
    print("")
    print("----------------------")
    for show in shows:
        print(f"{shows.index(show) + 1}) {show}")
    print("----------------------")
    print("")
    while True:
        try:
            showSelection = int(input("Enter the show to edit: "))
        except ValueError:
            print("Please input a valid number")
            continue
        if showSelection > len(shows):
            print("Please input a valid number")
            continue
        break
    print("")
    print("----------------------")
    print("1) Name")
    print("2) Folder location")
    print("3) Episodes per cycle")
    print("4) Rescan episodes")
    print("5) Transcode settings")
    print("----------------------")
    print("")
    while True:
        try:
            editSelection = int(input("Enter your selection to edit: "))
        except ValueError:
            print("Please input a valid number")
            continue
        break
    if editSelection == 1:
        newName = input("Enter the new name for this show: ")
        while True:
            confirmation = input(
                f"Are you sure you want to rename {shows[showSelection - 1]} to {newName} [y/n]: "
            )
            if confirmation == "y":
                break
            elif confirmation == "n":
                mainMenu()
            else:
                print("Please input a valid y or n")
        result = changeShowName(shows[showSelection - 1], newName)
        if result == True:
            print("The show has been edited sucessfully!")
            mainMenu()
    elif editSelection == 2:
        newFolderLocation = input("Enter the new folder location for this show: ")
        if os.path.exists(newFolderLocation):
            previousFolderLocation = getShowInformation(shows[showSelection - 1])
            result = changeShowFolder(shows[showSelection - 1], newFolderLocation)
            if result[0]:
                print(
                    f"The location of {shows[showSelection - 1]} has been changed to {newFolderLocation}"
                )
                print(
                    f"In the new location, there is {result[1]} seasons and {result[2]} episodes"
                )
                while True:
                    confirmation = input("Is this information corret [y/n]: ")
                    if confirmation == "y":
                        mainMenu()
                    elif confirmation == "n":
                        print(
                            f"Changing the folder location back to {previousFolderLocation[2]}"
                        )
                        changeShowFolder(
                            shows[showSelection - 1], previousFolderLocation[2]
                        )
                        mainMenu()
                    else:
                        print("Please input y or n")
    elif editSelection == 3:
        while True:
            try:
                newEpisodesPerRun = int(
                    input("Enter how many episodes your want per cycle: ")
                )
            except:
                print("Please input a valid number")
                continue
            break
        result = changeEpisodePerRun(shows[showSelection - 1], newEpisodesPerRun)
        if result:
            print(f"{shows[showSelection - 1]} now has {newEpisodesPerRun} per session")
            mainMenu()
    elif editSelection == 4:
        showInformation = getShowInformation(shows[showSelection - 1])
        results = changeShowFolder(shows[showSelection - 1], showInformation[2])
        if results[0]:
            print(
                f"{shows[showSelection - 1]} now has {results[1]} seasons and {results[2]} episodes"
            )
            mainMenu()
    elif editSelection == 5:
        transcodeSettings = getSettings()
        while True:
            audioTranscode = input("Do you want to transcode the audio [y/n]: ")
            if audioTranscode == "y":
                audioTranscode = transcodeSettings[1]
                break
            elif audioTranscode == "n":
                audioTranscode = "copy"
                break
            else:
                print("Please input y or n")
        while True:
            videoTranscode = input("Do you want to transcode the video [y/n]: ")
            if videoTranscode == "y":
                videoTranscode = transcodeSettings[0]
                break
            elif videoTranscode == "n":
                videoTranscode = "copy"
                break
            else:
                print("Please input y or n")
        if changeTranscode(shows[showSelection - 1], audioTranscode, videoTranscode):
            print(
                f"{shows[showSelection - 1]} now transcodes audio to {audioTranscode} and video to {videoTranscode}"
            )
            mainMenu()


def removeShowCLI():
    shows = getShows()
    print("")
    print("----------------------")
    for show in shows:
        print(f"{shows.index(show) + 1}) {show}")
    print("----------------------")
    print("")
    while True:
        try:
            showSelection = int(input("Enter the show to delete: "))
        except ValueError:
            print("Please input a valid number")
            continue
        if showSelection > len(shows):
            print("Please input a valid number")
            continue
        break
    while True:
        confirmation = input(
            f"Are you sure your want to delete {shows[showSelection - 1]} [y/n]: "
        )
        if confirmation == "y":
            break
        elif confirmation == "n":
            mainMenu()
        else:
            print("Please select y or n")
    result = removeShow(shows[showSelection - 1])
    if result:
        print(f"{shows[showSelection - 1]} has been succesfully deleted")
        mainMenu()


def getShowsCLI():
    shows = getShows()
    for show in shows:
        showInformation = getShowInformation(show)
        episodeCount = getEpisodeCount(show)
        print("")
        print(show)
        print(f"  Episodes per cycle: {showInformation[1]}")
        print(f"  Folder location: {showInformation[2]}")
        print(f"  Show position: {showInformation[3]}")
        print(f"  Audio transcode: {showInformation[4]}")
        print(f"  Video transcode: {showInformation[5]}")
        print(f"  Episodes: {episodeCount[0]}")
        print(f"  Seasons: {episodeCount[1]}")
        print("")
    input("Press enter for main menu")  # Allows time for viewing information
    mainMenu()


def changeOrderCLI():
    shows = getShows()
    position = 1
    showsPosition = []
    while True:
        if shows == []:
            break
        print("")
        print("----------------------")
        for show in shows:
            print(f"{shows.index(show) + 1}) {show}")
        print("----------------------")
        print("")
        while True:
            try:
                showSelection = int(
                    input(f"Enter the show to be in position {position}: ")
                )
            except ValueError:
                print("Please input a number")
                continue
            if showSelection > len(shows):
                print("Please input a valid number")
                continue
            break
        showsPosition.append(shows[showSelection - 1])
        position += 1
        shows.remove(shows[showSelection - 1])
        print(f"The current order is {showsPosition}")
    for show in showsPosition:
        print(f"{showsPosition.index(show) + 1}) {show}")
    while True:
        confirmation = input("Are you sure you want the above order [y/n]: ")
        if confirmation == "y" or confirmation == "n":
            break
        print("Please input y or n")
    if confirmation == "n":
        mainMenu()
    for show in showsPosition:
        result = changeShowPosition(show, (showsPosition.index(show) + 1))
        if result:
            continue
    print("Show order sucessfully changed!")
    mainMenu()


def createPlaylistCLI():
    check = checkShowPositionExist()  # Makes sure every show has a position
    if not check:
        print("Please make an order for your shows")
        mainMenu()
    while True:
        try:
            lengthOfPlaylist = int(
                input("Enter how many episodes you want in your playlist: ")
            )
        except TypeError:
            print("Please input a number")
            continue
        break
    playlist = createShowOrder(lengthOfPlaylist)
    while True:
        driveLocations = getDriveLocations()
        print("")
        print("----------------------")
        for location in driveLocations:
            print(f"{driveLocations.index(location) + 1}) {location}")
        print(f"{len(driveLocations) + 1}) Other location")
        print("----------------------")
        print("")
        try:
            folderLocationSelection = int(
                input("Enter the folder to copy the playlist to: ")
            )
        except ValueError:
            print("Please input a valid number")
            continue
        if folderLocationSelection == len(driveLocations) + 1:
            while True:
                folderLocation = input("Enter the folder location: ")
                if os.path.exists(folderLocation):
                    storeDriveLocation(folderLocation)
                    break
                else:
                    print(
                        "Folder location does not exists, please input a valid folder location"
                    )
                    continue
            break
        elif folderLocationSelection - 1 < len(driveLocations):
            folderLocation = driveLocations[folderLocationSelection - 1]
            if os.path.exists(folderLocation):
                break
            else:
                print(
                    "Folder location does not exists, please choose a different folder location"
                )
                continue
        else:
            print("Please input a valid number")
            continue
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM previousMain")
    fileNumber = cursor.fetchone()
    if not fileNumber:
        fileNumber = 1
        cursor.execute("INSERT INTO previousMain(fileNumber) VALUES (1)")
    else:
        fileNumber = fileNumber[0]
    for episode in playlist:
        showLocation = getShowInformation(episode[0])[2]
        season = re.search(r"S(\d+)", episode[1]).group(1)
        transcodeSettings = getShowInformation(episode[0])[4:6]
        preferredVideoCodec, maxBitrate = getSettings()[0], getSettings()[2]
        if os.path.exists(f"{showLocation}/Season {season}/{episode[1]}"):
            print(f"Copying {episode[1]} from {episode[0]}")
            bitrate = calculateBitrate(f"{showLocation}/Season {season}/{episode[1]}")
            number, suffix = float(maxBitrate[:-1]), maxBitrate[-1]
            if suffix == "M":
                number = number * 1000
            elif suffix == "K":
                number = number
            if bitrate > number:
                transcodeShow(
                    episode[0],
                    f"{showLocation}/Season {season}/{episode[1]}",
                    episode[1],
                    f"{'0'*(6-len(str(fileNumber)))}{fileNumber}",
                    folderLocation,
                    transcodeSettings[0],
                    preferredVideoCodec,
                    maxBitrate,
                )
            elif transcodeSettings == ("copy", "copy"):
                copyShow(
                    episode[0],
                    f"{showLocation}/Season {season}/{episode[1]}",
                    episode[1],
                    f"{'0'*(6-len(str(fileNumber)))}{fileNumber}",
                    folderLocation,
                )
            else:
                transcodeShow(
                    episode[0],
                    f"{showLocation}/Season {season}/{episode[1]}",
                    episode[1],
                    f"{'0'*(6-len(str(fileNumber)))}{fileNumber}",
                    folderLocation,
                    transcodeSettings[0],
                    transcodeSettings[1],
                    maxBitrate,
                )
            fileNumber += 1
    cursor.execute(f"UPDATE previousMain SET fileNumber = {fileNumber}")
    connection.commit()
    connection.close()
    print(f"Files sucessfully copied into {folderLocation}")
    mainMenu()


def settingsCLI():
    print("")
    print("----------------------")
    print("1) Preferred Video Codec")
    print("2) Preferred Audio Codec")
    print("3) Max bitrate")
    print("4) Get current settings")
    print("5) Back to main menu")
    print("----------------------")
    print("")
    while True:
        try:
            selection = int(input("Enter your selection: "))
        except ValueError:
            print("Please input a valid number")
            continue
        break
    if selection == 1:
        codecs = ["h264", "hevc", "av1"]
        print("")
        print("----------------------")
        print("1) h264")
        print("2) hevc")
        print("3) av1")
        print("----------------------")
        print("")
        while True:
            try:
                videoCodecSelection = int(input("Enter your selection: "))
            except ValueError:
                print("Please input a valid number")
                continue
            if videoCodecSelection > 3 or videoCodecSelection < 1:
                print("Please input a valid number")
                continue
            break
        if editVideoCodec(codecs[videoCodecSelection - 1]):
            print(f"Video codec has been changed to {codecs[videoCodecSelection - 1]}")
            settingsCLI()
    elif selection == 2:
        codecs = ["aac", "mp3"]
        print("")
        print("----------------------")
        print("1) aac")
        print("2) mp3")
        print("----------------------")
        print("")
        while True:
            try:
                audioCodecSelection = int(input("Enter your selection: "))
            except ValueError:
                print("Please input a valid number")
                continue
            if audioCodecSelection > 2 or audioCodecSelection < 1:
                print("Please input a valid number")
                continue
            break
        if editAudioCodec(codecs[audioCodecSelection - 1]):
            print(f"Audio codec has been changed to {codecs[audioCodecSelection - 1]}")
            settingsCLI()
    elif selection == 3:
        print("Please input the bitrate in mbps")
        while True:
            try:
                maxBitrate = float(input("Enter the max bitrate: "))
            except ValueError:
                print("Please input a valid number")
                continue
            break
        if maxBitrate < 1:
            maxBitrate = f"{int(maxBitrate*1000)}K"
        else:
            maxBitrate = f"{int(maxBitrate)}M"
        if editMaxBitrate(maxBitrate):
            print(f"Max bitrate has been changed to {maxBitrate}")
            settingsCLI()
    elif selection == 4:
        settings = getSettings()
        print("")
        print("----------------------")
        print(f"Preferred Video Codec: {settings[0]}")
        print(f"Preferred Audio Codec: {settings[1]}")
        print(f"Max Bitrate: {settings[2]}")
        print("----------------------")
        print("")
        input("Press enter to go back to settings")
        settingsCLI()
    elif selection == 5:
        mainMenu()
    else:
        print("Please input a valid number")
        settingsCLI()


generateSettings()
mainMenu()
