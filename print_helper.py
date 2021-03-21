

def get_confirmation():
	input("Press Enter to continue...")

def show_translate_stats():
	print('\nTRANSLATE STATS')

def show_download_stats(api_calls, mp3_download_lists):
	print('\nDOWNLOAD STATS')
	print('API calls: ' + str(api_calls))
	print('successfully downloaded: '+str(len(mp3_download_lists[0])))
	print('failed to download: '+str(len(mp3_download_lists[1])))
	print('previously failed to download: '+str(len(mp3_download_lists[2])))
	print('already had: '+str(len(mp3_download_lists[3])))

def create_download_output_text(mp3_download_lists):
	create_output_file('download_succeed', mp3_download_lists[0])
	create_output_file('download_failed', mp3_download_lists[1])
	create_output_file('download_previously', mp3_download_lists[2])
	create_output_file('download_already_have', mp3_download_lists[3])

def show_audio_lesson_stats(number_of_audio_lesson_passed):
	print('AUDIO LESSON STATS')
	print('entries passed: ', number_of_audio_lesson_passed)