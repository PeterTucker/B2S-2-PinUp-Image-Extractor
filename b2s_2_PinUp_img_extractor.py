import os
import base64
import xml.etree.ElementTree as ET

def extract_images_from_directb2s(directory):
    directb2s_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".directb2s"):
                directb2s_files.append(os.path.join(root, file))
    return directb2s_files

def extract_images(directb2s_files, output_directory_backglass, output_directory_menu):
    existing_files_backglass = []
    existing_files_menu = []
    for idx, file_path in enumerate(directb2s_files, start=1):
        print(f"Extracting '{idx}' of '{len(directb2s_files)}' .directb2s files: {os.path.basename(file_path)}")
        tree = ET.parse(file_path)
        root = tree.getroot()
        backglass_image_found = False
        dmd_image_found = False
        for image_type in root.findall(".//Images/*"):
            image_data = image_type.get("Value")
            image_data_decoded = base64.b64decode(image_data)
            image_name = os.path.basename(file_path).replace(".directb2s", f".png")
            if image_type.tag == 'BackglassImage':
                backglass_image_found = True
                image_path = os.path.join(output_directory_backglass, image_name)
                if os.path.exists(image_path):
                    existing_files_backglass.append(image_path)
                else:
                    with open(image_path, "wb") as img_file:
                        img_file.write(image_data_decoded)
            elif image_type.tag == 'DMDImage':
                dmd_image_found = True
                image_path = os.path.join(output_directory_menu, image_name)
                if os.path.exists(image_path):
                    existing_files_menu.append(image_path)
                else:
                    with open(image_path, "wb") as img_file:
                        img_file.write(image_data_decoded)
        if not backglass_image_found:
            print("Warning: 'BackglassImage' not found in this file.")
        if not dmd_image_found:
            print("Warning: 'DMDImage' not found in this file.")

    return existing_files_backglass, existing_files_menu

def main():
    print("Scanning 'VisualPinball/Tables'.")
    directb2s_files = extract_images_from_directb2s("VisualPinball/Tables")
    print(f"'{len(directb2s_files)}' .directb2s files were found:\n")
    for file in directb2s_files:
        print(f"{os.path.dirname(file)} <DIR>")
        print(f"\t{os.path.basename(file)} <FILE>")
    print()
    user_input = input(f"I found '{len(directb2s_files)}' .directb2s files in 'VisualPinball/Tables', would you like me extract and export them to  the 'PinUPSystem/POPMedia/Visual Pinball X/Backglass/' folder? (Y/N) ")
    if user_input.lower() in ('y', 'yes'):
        output_directory_backglass = "PinUPSystem/POPMedia/Visual Pinball X/Backglass/"
        output_directory_menu = "PinUPSystem/POPMedia/Visual Pinball X/Menu/"
        existing_files_backglass, existing_files_menu = extract_images(directb2s_files, output_directory_backglass, output_directory_menu)
        print("\nAll 'BackglassImage' images have been extracted to 'PinUPSystem/POPMedia/Visual Pinball X/Backglass/'.")
        print("All 'DMDImage' images have been extracted to 'PinUPSystem/POPMedia/Visual Pinball X/Menu/'.\n")
        if existing_files_backglass or existing_files_menu:
            print("There were however existing files found in these locations:\n")
            for existing_file in existing_files_backglass:
                print(f"\t'{existing_file}'")
            for existing_file in existing_files_menu:
                print(f"\t'{existing_file}'")
            print("\nPlease remove these files if you would like to extract new image files in their place.")
    else:
        print("Goodbye!")

if __name__ == "__main__":
    main()
