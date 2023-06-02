# Import necessary libraries
import cv2
from pathlib import Path

# Set the path of the directory containing the images
results_dir = Path("./results")

# Define a dictionary to map the detected staff line indices to letters
staff_dict = {
    0: 'A',
    1: 'F',
    2: 'D',
    3: 'B',
    4: 'G'
}

# Initialize and empty list to store the detected lines
results = []

# Loop over each image file in the directory
for img_path in results_dir.glob("*.png"):
    
    # Initialize an empty list to store the detected note
    note = []
    
    # Load the image
    img = cv2.imread(str(img_path))
    # cv2.imwrite('1.png', img)

    # Convert to grayscale
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Threshold to obtain a binary image
    _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    
    # Detect horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 1))
    horizontal_lines = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    
    # Detect vertical lines 
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 20))
    vertical_lines = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, vertical_kernel, iterations=2)

    # Find contoours of horizontal lines
    h_conts = cv2.findContours(horizontal_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    h_conts = h_conts[0] if len(h_conts) == 2 else h_conts[1]
    
    # Find contours of vertical lines
    v_conts = cv2.findContours(vertical_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    v_conts = v_conts[0] if len(v_conts) == 2 else v_conts[1]
    
    # Store the positions of the staff lines
    staff_line_positions = []
    
    white = (255, 255, 255)
    
    # Remove horizontal lines from the image and store their positions
    for c in h_conts:
        (x1, y1, w, h) = cv2.boundingRect(c)
        cv2.rectangle(gray_image, (x1, y1), (x1+w, y1+h), color=white, thickness=2)
        staff_line_positions.append([x1, y1, x1+w,  y1+h])
    
    # cv2.imwrite('2.png', gray_image)
    
    # Remove vertical lines from the image
    for c in v_conts:
        (x1, y1, w, h) = cv2.boundingRect(c)
        cv2.rectangle(gray_image, (x1, y1), (x1+w, y1+h), color=white, thickness=2)
        
    # cv2.imwrite('3.png', gray_image)
    
    # Sort staff lines according to y axis
    staff_line_positions = sorted(staff_line_positions, key=lambda x: x[1])
    
    # Invert the image and calculate the centroid of the blob
    inverted_img = cv2.bitwise_not(gray_image)
    M = cv2.moments(inverted_img)
    centroid = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
    cv2.circle(img, centroid, 4, (255, 0, 0), -1)
    # cv2.imwrite('4.png', inverted_img)

    # Get the nearest staff line 
    second_col = [row[1] for row in staff_line_positions]
    min_idx, _ = min(enumerate(second_col), key=lambda x: abs(centroid[1] - x[1]))
    min_idx = min(min_idx, 4)
    # cv2.imwrite('5.png', img)
    
    # img_path.rename(Path(img_path.parent, f"{img_path.stem}_{staff_dict[min_idx]}{img_path.suffix}"))
    # new_path = Path(output_dir, f"{img_path.stem}_{staff_dict[min_idx]}{img_path.suffix}")
    # cv2.imwrite(str(new_path), img)
    
    if 'eighth' in img_path.stem:
        note.append('eighth')
    if 'quarter' in img_path.stem:
        note.append('quarter')
    if 'half' in img_path.stem:
        note.append('half')
    if 'whole' in img_path.stem:
        note.append('whole')
    
    note.append(staff_dict[min_idx])   
    results.append(note)
    
# Save detected notes and staff line in a text file
with open('./results/detected_notes.txt', 'w') as f:
    for line in results:
        f.write(f"{line}\n")
