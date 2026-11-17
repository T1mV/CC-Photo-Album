from quality import is_image_sharp, create_sharp_folder, process_images
from screenshots import is_screenshot, screenshots_folder, check_screenshots_in_folder

#? Inputs
#*---------------------------------------------------------------------------------

quality = 100.0
folder_path = "/home/zuzia/Desktop/studia/year2/creativity/photo_book/photos"
folder_for_good_quality = "/home/zuzia/Desktop/studia/year2/creativity/photo_book"


#? Saving only high quality images
#*---------------------------------------------------------------------------------

folder_save_path = create_sharp_folder(folder_for_good_quality)
process_images(folder_path, quality, folder_save_path)

#? Saving only non screenshots
#*---------------------------------------------------------------------------------
folder_for_non_screenshots = screenshots_folder(folder_save_path)
check_screenshots_in_folder(folder_save_path, folder_for_non_screenshots)

#? Saving only one duplicate image
#*---------------------------------------------------------------------------------