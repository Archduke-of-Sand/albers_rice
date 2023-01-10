import os
from albers_sort import Image

# Set the path to the folder you want to search
folder_path = '~dt/larbs/albers/unsorted'

# Get a list of all the files in the folder
files = os.listdir(folder_path)

# Get screen resolution
resolution = get_screen_resolution()
screen_width = resolution[1]
screen_height = resolution[0]

# Iterate over the files
for file in files:
    # Get the full path of the file
    file_path = os.path.join(folder_path, file)

    # Check if the file is a regular file (not a directory)
    if os.path.isfile(file_path) and (file.endswith(".jpg") or file.endswith(".png")):
        if file.endswith(".jpg") or file.endswith(".png"):
            # Create an Image object
            image = Image(file_path)

            # Resize the image to fill the screen
            image.resize_to_screen(screen_width, screen_height)

            # Fill in the borders
            image.fill_borders(ratio)

            # Save the resized and filled image
            image.save(file_path)

            # Get the dominant color
            dominant_color = image.get_dominant_color()

            # create the full path to the sunset, noon, and sunrise directories
            sunset_dir = os.path.join(os.getcwd(), 'sunset')
            noon_dir = os.path.join(os.getcwd(), 'noon')
            sunrise_dir = os.path.join(os.getcwd(), 'sunrise')
            night_dir = os.path.join(os.getcwd(), 'night')
            unused_dir = os.path.join(os.getcwd(), 'unused')

            # create the sunset, noon, and sunrise directories if they do not exist
            if not os.path.exists(sunset_dir):
                os.makedirs(sunset_dir)
            if not os.path.exists(noon_dir):
                os.makedirs(noon_dir)
            if not os.path.exists(sunrise_dir):
                os.makedirs(sunrise_dir)
            if not os.path.exists(night_dir):
                os.makedirs(night_dir)
            if not os.path.exists(unused_dir):
                os.makedirs(unused_dir)

            # determine the dominant color of the file
            if dominant_color==night:
                os.rename(os.path.expanduser(os.getcwd()) + '/' + file,
                          os.path.join(night_dir, file))

            elif dominant_color[0] > 200 and dominant_color[1] < 50 and dominant_color[2] < 50:
                # move the file to the sunset directory
                os.rename(os.path.expanduser(os.getcwd()) + '/' + file,
                          os.path.join(sunset_dir, file))
            elif dominant_color[0] > 200 and dominant_color[1] > 200 and dominant_color[2] < 50:
                # move the file to the noon directory
                os.rename(os.path.expanduser(os.getcwd()) + '/' + file,
                          os.path.join(noon_dir, file))
            elif dominant_color[0] < 50 and dominant_color[1] > 200 and dominant_color[2] < 50:
                # move the file to the sunrise directory
                os.rename(os.path.expanduser(os.getcwd()) + '/' + file,
                          os.path.join(sunrise_dir, file))
            else:
                # move the file to the unused directory
                os.rename(os.path.expanduser(os.getcwd()) + '/' + file,
                          os.path.join(unused_dir, file))


