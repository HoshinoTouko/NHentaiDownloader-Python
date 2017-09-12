import urllib.request
import os
import sys

from NHentaiComic.Comic import Comic




def main():
    if len(sys.argv) == 1:
        comicID = '206670'
        comicID = input("Comic.py id: ")
        comicID = [comicID]
    else:
        comicID = sys.argv[1:]
    print("You will get these comics: %s" % str(comicID))
    downComics = []
    # Download comics
    for id in comicID:
        comic = Comic(id)
        downComics.append(comic)
        print('Comic ID: %s' % comic.comicID)
        print('Title: %s' % comic.title)
        print('Gallery ID: %s' % comic.galleryID)
        print('Max page number: %s' % comic.getMaxPage())
        print('Img type: %s' % comic.getImgType())
        print('Downloading......')
        comic.downImgs()
    # down_img('https://i.nhentai.net/galleries/1113041/4.jpg', 'test.jpg')

    # Check comics
    print('.\n.\n.\n.\n.\n.')
    print('Check if the comic has been totally downloaded.')
    for downComic in downComics:
        downComic.checkIntegrity()
    print('Check end.')


if __name__ == '__main__':
    main()
