import logging
import sys
from datetime import datetime, timedelta
from getInfoSongs import *
from sparqlLibrary import *

LOG_FILE = datetime.now().strftime("%Y%m%d") + "logfile.log"

def setLogging():
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    sh = logging.StreamHandler(sys.stdout)
    fh = logging.FileHandler(LOG_FILE)

    logger.setLevel(logging.INFO)
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)

    logger.addHandler(sh)
    logger.addHandler(fh)

    return logger

def main(arg1,arg2,arg3,arg4):

    #STUDY 1
    song1 = arg1
    artist1 = arg2

    #STUDY 2
    song2 = arg3
    artist2 = arg4

    logger = setLogging()

    #PARSE SONGS
    try:
        #Object 1
        song1 = isSingle(song1,artist1)
        if song1.empty == True:
            song1 = arg1
            song1 = isSong(song1,artist1)
    
        #Object 2
        song2 = isSingle(song2,artist2)
        if song2.empty == True:
            song2 = arg3
            song2 = isSong(song2,artist2)

    except Exception as miss:
        logger.info(miss)
       
    #GET PROPERTIES         
    try:
        if song1.empty == True:
            raise Exception('Missing first song')
        else:
            if song2.empty == True:
                raise Exception('Missing second song')
            else:
                #SONG1
                songData = getInfSong(song1['item.value'][0],song1['itemLabel.value'][0])
                genreData = getGenre2(songData,logger)
                artistData = getArtist2(songData,logger)
                membersData = getMembers2(artistData,logger)

                #SONG2
                songData2 = getInfSong(song2['item.value'][0],song2['itemLabel.value'][0])
                genreData2 = getGenre2(songData2,logger)
                artistData2 = getArtist2(songData2,logger)
                membersData2 = getMembers2(artistData2,logger)


                #GENERE SONGINFO
                songData.to_csv('songData1.csv',index=False)
                songData2.to_csv('songData2.csv',index=False)

                #GENERE ARTIST
                artistData.to_csv('artistData.csv',index=False)
                artistData2.to_csv('artistData2.csv',index=False)

                song1Data = [songData,genreData,artistData,membersData]
                song1Data = pd.concat(song1Data,sort=False)

                song1Data = parseDates(song1Data)
                song1Data = formatDates(song1Data)

                song2Data = [songData2,genreData2,artistData2,membersData2]
                song2Data = pd.concat(song2Data,sort=False)

                song2Data = parseDates(song2Data)
                song2Data = formatDates(song2Data)

                relationsDF = mergeData(song1Data,song2Data)

                relationsDF = relationsDF.drop_duplicates()
                relationsDF.to_csv('relations.csv',index=False)

    except Exception as miss:
        logger.info(miss)
    return relationsDF

if __name__ == "__main__":
   song1 = 'Start Me Up'
   artist1 = 'The Rolling Stones'
   song2 = 'Let It Be' 
   artist2 = 'The Beatles'
   relationsDF = main(song1,artist1,song2,artist2)
