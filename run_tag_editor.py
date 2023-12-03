import os
import time
from mp3_tagger import MP3File


class MusicProcessor:
    def __init__(self, music_folder):
        self.music_folder = music_folder
        self.keywords_to_remove = [
            ' myfreemp3.vip', 'X2Download.app - ', 'X2Download.app ', ' (320 kbps)', 'SaveTube.io -'
        ]
        self.check_arr = ['(1)', '(2)', '(3)']
        self.parser_delimiters = [' - ', ' – ']

    def read_keyboard_input(self):
        keywords_nr = int(input('How many keywords do you want to remove?: '))
        self.keywords_to_remove = [input(f'Keyword {i + 1}:') for i in range(keywords_nr)]
        print(self.keywords_to_remove)

    def remove_duplicates(self):
        count_duplicates = 0
        total_nr_files = 0
        for file in os.listdir(self.music_folder):
            path_to_file = os.path.join(self.music_folder, file)
            if os.path.isfile(path_to_file):
                total_nr_files += 1
                if any(check in file for check in self.check_arr):
                    try:
                        os.remove(path_to_file)
                        count_duplicates += 1
                        print(f'Removed file: {file}')
                    except OSError:
                        print("Error while deleting file ", path_to_file)
        self._print_summary(count_duplicates, total_nr_files)

    def process_files(self):
        total_files_edited = 0
        for file in os.listdir(self.music_folder):
            path_to_file = os.path.join(self.music_folder, file)
            if os.path.isfile(path_to_file):
                output_file_name = file
                for key in self.keywords_to_remove:
                    output_file_name = output_file_name.replace(key, "")
                new_renamed_file_path = os.path.join(self.music_folder, output_file_name)
                os.rename(path_to_file, new_renamed_file_path)
                total_files_edited += 1
        print(f'Total files processed: {total_files_edited}')

    def show_all_files(self):
        for file in os.listdir(self.music_folder):
            path_to_file = os.path.join(self.music_folder, file)
            if os.path.isfile(path_to_file):
                print(file)

    def clear_fields(self, mp3_file):
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

    def edit_ID3_tag(self):
        print('running tag edit...')
        for file in os.listdir(self.music_folder):
            path_to_file = os.path.join(self.music_folder, file)
            if os.path.isfile(path_to_file) and '.mp3' in file:
                mp3 = MP3File(path_to_file)
                self.clear_fields(mp3)

                found_delimiter = None
                for delimiter in self.parser_delimiters:
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

    def _print_summary(self, count_duplicates, total_nr_files):
        print('--------------------------------------------')
        print(f'Duplicates removed: {count_duplicates}')
        print(f'Total number of songs: {total_nr_files}')
        print(f'Total songs after removal of duplicates: {total_nr_files - count_duplicates}')


def main():
    music_processor = MusicProcessor(r'D:\Music\test_folder')
    # music_processor.read_keyboard_input()
    # music_processor.remove_duplicates()
    music_processor.process_files()
    # music_processor.show_all_files()
    music_processor.edit_ID3_tag()


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f'Completed successfully in: {"{:.2f}".format(end - start)} s')
