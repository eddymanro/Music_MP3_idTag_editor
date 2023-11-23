import os
import time
from mp3_tagger import MP3File

# Array containing keywords to be removed from the filename
keywords_to_remove = [' myfreemp3.vip ', 'X2Download.app - ', 'X2Download.app ', ' (320 kbps)']
words_removal_arr = []

# Path to the folder containing the music files
path_to_music = r'D:\Music\test_folder'


def read_keyboard_input():
    keywords_nr = int(input('How many keywords do you want to remove?: '))
    for i, _ in enumerate(range(keywords_nr), start=1):
        words_removal_arr.append(str(input(f'Keyword {i}:')))
    print(words_removal_arr)


def remove_duplicates():
    check_arr = ['(1)', '(2)', '(3)']
    count_duplicates = 0
    total_nr_files = 0
    for file in os.listdir(path_to_music):
        path_to_file = os.path.join(path_to_music, file)
        if os.path.isfile(path_to_file):
            total_nr_files += 1
            if any(k in file for k in check_arr):
                try:
                    os.remove(path_to_file)
                    count_duplicates += 1
                    print('Removed file:', file)
                except OSError:
                    print("Error while deleting file", path_to_file)
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
            edit_flag = any(key in output_file_name for key in keywords_to_remove)
            if edit_flag:
                total_files_edited += 1
                new_renamed_file_path = os.path.join(path_to_music, output_file_name.replace(key, ""))
                os.rename(path_to_file, new_renamed_file_path)
    print("Total files processed:", total_files_edited)


def show_all_files():
    for file in os.listdir(path_to_music):
        path_to_file = os.path.join(path_to_music, file)
        if os.path.isfile(path_to_file):
            print(file)


def clear_fields(mp3_file):
    for attr in dir(mp3_file):
        if not callable(getattr(mp3_file, attr)) and not attr.startswith("__"):
            setattr(mp3_file, attr, "")


def edit_ID3_tag():
    print('running tag edit...')
    parser_delimiter_1 = ' - '  # delimiters seen: ' - ' ' – '
    parser_delimiter_2 = ' – '
    for file in os.listdir(path_to_music):
        path_to_file = os.path.join(path_to_music, file)
        if os.path.isfile(path_to_file) and file.endswith('.mp3'):
            # Create MP3File instance
            mp3 = MP3File(path_to_file)
            # Clear all id3 tag fields
            clear_fields(mp3)
            # under work
            if parser_delimiter_1 in file:
                split_song_arr = file.split(parser_delimiter_1)
                mp3.artist, mp3.song = split_song_arr[0], split_song_arr[1][:-4]
            elif parser_delimiter_2 in file:
                split_song_arr = file.split(parser_delimiter_2)
                mp3.artist, mp3.song = split_song_arr[0], split_song_arr[1][:-4]
            else:
                mp3.artist, mp3.song = 'Unknown Artist', file[:-4]
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
