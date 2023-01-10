#find resolution of current monitor
def get_screen_resolution():
    output = subprocess.check_output(['xrandr'])
    resolution = output.split()[7]
    resolution = resolution.split(b'x')
    return resolution

def replicate_border(image: object, ratio: object) -> object:
    # Get the dimensions of the image
    rows, cols, _ = image.shape

    # Initialize variables to keep track of the start and end points of the border
    start_row = 0
    end_row = 0
    start_col = 0
    end_col = 0

    # Find the start and end points of the border
    for row in range(rows):
        if not np.array_equal(image[row, 0], image[row, cols - 1]):
            start_row = row
            break

    for row in range(rows - 1, 0, -1):
        if not np.array_equal(image[row, 0], image[row, cols - 1]):
            end_row = row
            break

    for col in range(cols):
        if not np.array_equal(image[0, col], image[rows - 1, col]):
            start_col =
def check_folder_rez(folder):
    folder_size = len(os.listdir(folder))
    # Get screen resolution
    screen_resolution = get_screen_resolution()
    # Count files already checked
    file_count = 0
    deleted: bool = False

    for file in folder:
        if file_count < folder_size:
            # Check if the file is a JPG or PNG file
            if file.endswith('.jpg') or file.endswith('.png'):
                # Construct the full file path
                file_path = os.path.join(folder, file)
                # Get the resolution of the image
                file_resolution = Image.open(file_path).size
                # Check the file's resolution
                if file_resolution == screen_resolution:
                    file_count += 1
                    continue
                else:
                    # Remove the file if it has the wrong resolution
                    os.remove(file_path)
                    continue
            elif not file.endswith('.jpg') or not file.endswith('.png'):
                # Skip the file if it's not a JPG or PNG file
                file_count += 1
                continue
            else:
                return deleted==True
