from quality import is_image_sharp, create_sharp_folder, process_images

#? Inputs
#*---------------------------------------------------------------------------------

quality = 100.0
folder_path = "/home/zuzia/Desktop/studia/year2/creativity/photo_book/photos"
folder_save_path = "/home/zuzia/Desktop/studia/year2/creativity/photo_book"


#? Saving only high quality images
#*---------------------------------------------------------------------------------

folder_save_path = create_sharp_folder(folder_save_path)
process_images(folder_path, quality, folder_save_path)

#? Saving only non screenshots
#*---------------------------------------------------------------------------------