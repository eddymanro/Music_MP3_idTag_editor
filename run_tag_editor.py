import os
import time
from mp3_tagger import MP3File

# array containing keywords to be removed from the filename
keywords_to_remove = [' myfreemp3.vip', 'X2Download.app - ', 'X2Download.app ', ' (320 kbps)']
words_removal_arr = []

# path to the folder containing the music files
path_to_music = r'D:\Music\2023\03_March\2'


def read_keyboard_input():
    keywords_nr = int(input('How many keywords do you want to remove?: '))
    for i in range(keywords_nr):
        words_removal_arr.append(str(input('Keyword ' + str(i+1) + ':')))
    print(words_removal_arr)


def remove_duplicates():
    check_arr = ['(1)', '(2)', '(3)']
    count_duplicates = 0
    total_nr_files = 0
    for file in os.listdir(path_to_music):
        path_to_file = os.path.join(path_to_music, file)
        if os.path.isfile(path_to_file):
            total_nr_files += 1
            for k in check_arr:
                if k in file:
                    try:
                        os.remove(path_to_file)
                        count_duplicates += 1
                        print('Removed file: ' + file)
                    except OSError:
                        print("Error while deleting file ", path_to_file)
    print('--------------------------------------------')
    print('Duplicates removed: ' + str(count_duplicates))
    print('Total number of songs: ' + str(total_nr_files))
    print('Total songs after removal of duplicates: ' + str(total_nr_files - count_duplicates))


def process_files():
    total_files_edited = 0
    for file in os.listdir(path_to_music):
        path_to_file = os.path.join(path_to_music, file)
        if os.path.isfile(path_to_file):
            output_file_name = file
            edit_flag = False
            for key in keywords_to_remove:
                if key in output_file_name:
                    edit_flag = True
                    output_file_name = output_file_name.replace(key, "")
            if edit_flag is True:
                total_files_edited += 1
                new_renamed_file_path = os.path.join(path_to_music, output_file_name)
                os.rename(path_to_file, new_renamed_file_path)
            else:
                pass
    print("Total files processed: " + str(total_files_edited))


def show_all_files():
    for file in os.listdir(path_to_music):
        path_to_file = os.path.join(path_to_music, file)
        if os.path.isfile(path_to_file):
            print(file)


def clear_fields(mp3_file):
    emtpy_field = ''
    mp3_file.album = emtpy_field
    mp3_file.band = emtpy_field
    mp3_file.comment = emtpy_field
    mp3_file.composer = emtpy_field
    mp3_file.publisher = emtpy_field
    mp3_file.url = emtpy_field
    mp3_file.year = emtpy_field
    mp3_file.save()


def edit_ID3_tag():
    print('running tag edit...')
    parser_delimiter = ' - '
    for file in os.listdir(path_to_music):
        path_to_file = os.path.join(path_to_music, file)
        if os.path.isfile(path_to_file) and '.mp3' in file:

            # Create MP3File instance
            mp3 = MP3File(path_to_file)

            # Clear all id3 tag fields
            clear_fields(mp3)

            if parser_delimiter in file:
                split_song_arr = file.split(parser_delimiter)
                mp3.artist = split_song_arr[0]
                mp3.song = split_song_arr[1][:-4]
            else:
                mp3.artist = 'Unknown Artist'
                mp3.song = file[:-4]
            mp3.save()


def __main__():
    read_keyboard_input()
    start = time.time()
    # remove_duplicates()
    # process_files()
    # show_all_files()
    # edit_ID3_tag()
    end = time.time()
    print('Completed successfully in: ' + "{:.2f}".format(end - start) + ' s')


__main__()
