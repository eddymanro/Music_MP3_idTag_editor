import os
import time
from mp3_tagger import MP3File

# List containing keywords to be removed from the filename
keywords_to_remove = [' myfreemp3.vip', 'X2Download.app - ', 'X2Download.app ', ' (320 kbps)', 'SaveTube.io -']

# Path to the folder containing the music files
path_to_music = r'D:\Music\test_folder'


def read_keyboard_input():
    keywords_nr = int(input('How many keywords do you want to remove?: '))
    words_removal_arr = [input(f'Keyword {i + 1}:') for i in range(keywords_nr)]
    print(words_removal_arr)


def remove_duplicates():
    check_arr = ['(1)', '(2)', '(3)']
    count_duplicates = 0
    total_nr_files = 0
    for file in os.listdir(path_to_music):
        path_to_file = os.path.join(path_to_music, file)
        if os.path.isfile(path_to_file):
            total_nr_files += 1
            if any(check in file for check in check_arr):
                try:
                    os.remove(path_to_file)
                    count_duplicates += 1
                    print(f'Removed file: {file}')
                except OSError:
                    print("Error while deleting file ", path_to_file)
    print('--------------------------------------------')
    print(f'Duplicates removed: {count_duplicates}')
    print(f'Total number of songs: {total_nr_files}')
    print(f'Total songs after removal of duplicates: {total_nr_files - count_duplicates}')


def process_files():
    total_files_edited = 0
    for file in os.listdir(path_to_music):
        path_to_file = os.path.join(path_to_music, file)
        if os.path.isfile(path_to_file):
            output_file_name = file
            for key in keywords_to_remove:
                output_file_name = output_file_name.replace(key, "")
            new_renamed_file_path = os.path.join(path_to_music, output_file_name)
            os.rename(path_to_file, new_renamed_file_path)
            total_files_edited += 1
    print(f'Total files processed: {total_files_edited}')


def show_all_files():
    for file in os.listdir(path_to_music):
        path_to_file = os.path.join(path_to_music, file)
        if os.path.isfile(path_to_file):
            print(file)


def clear_fields(mp3_file):
    empty_field = ''
    mp3_file.album = empty_field
    mp3_file.band = empty_field
    mp3_file.comment = empty_field
    mp3_file.composer = empty_field
    mp3_file.publisher = empty_field
    mp3_file.url = empty_field
    # mp3_file.genre = empty_field
    mp3_file.year = empty_field
    mp3_file.save()


def edit_ID3_tag():
    print('running tag edit...')
    parser_delimiters = [' - ', ' – ']
    for file in os.listdir(path_to_music):
        path_to_file = os.path.join(path_to_music, file)
        if os.path.isfile(path_to_file) and '.mp3' in file:
            mp3 = MP3File(path_to_file)
            clear_fields(mp3)

            found_delimiter = None
            for delimiter in parser_delimiters:
                if delimiter in file:
                    found_delimiter = delimiter
                    break

            if found_delimiter:
                split_song_arr = file.split(found_delimiter)
                mp3.artist = split_song_arr[0]
                mp3.song = split_song_arr[1][:-4]
            else:
                mp3.artist = 'Unknown Artist'
                mp3.song = file[:-4]
            mp3.save()


def main():
    # read_keyboard_input()
    start = time.time()
    # remove_duplicates()
    process_files()
    # show_all_files()
    edit_ID3_tag()
    end = time.time()
    print(f'Completed successfully in: {"{:.2f}".format(end - start)} s')


if __name__ == "__main__":
    main()
