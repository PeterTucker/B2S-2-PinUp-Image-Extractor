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

def check_existing_images(output_directory_backglass, output_directory_menu):
    existing_backglass_games = set()
    existing_menu_games = set()
    for file in os.listdir(output_directory_backglass):
        if file.endswith(".png"):
            game_name = file.replace(".png", "")
            existing_backglass_games.add(game_name)
    for file in os.listdir(output_directory_menu):
        if file.endswith(".png"):
            game_name = file.replace(".png", "")
            existing_menu_games.add(game_name)
    return existing_backglass_games, existing_menu_games

def extract_images(directb2s_files, output_directory_backglass, output_directory_menu, overwrite):
    existing_backglass_games, existing_menu_games = check_existing_images(output_directory_backglass, output_directory_menu)
    games_to_skip = set()
    extracted_backglass_images = []
    extracted_menu_images = []
    backglass_images_not_found = []
    dmd_images_not_found = []

    for idx, file_path in enumerate(directb2s_files, start=1):
        print(f"Checking '{idx}' of '{len(directb2s_files)}' .directb2s files: {os.path.basename(file_path)}")
        game_name = os.path.basename(file_path).replace(".directb2s", "")
        
        if game_name in existing_backglass_games and game_name in existing_menu_games:
            print(f"Both backglass and menu images already exist for '{game_name}'. Skipping.")
            games_to_skip.add(game_name)
            continue
        
        backglass_image_name = f"{game_name}.png"
        menu_image_name = f"{game_name}.png"
        
        backglass_image_path = os.path.join(output_directory_backglass, backglass_image_name)
        menu_image_path = os.path.join(output_directory_menu, menu_image_name)
        
        if not overwrite and os.path.exists(backglass_image_path) and os.path.exists(menu_image_path):
            print(f"Backglass and menu images already exist for '{game_name}'. Skipping.")
            games_to_skip.add(game_name)
            continue

        tree = ET.parse(file_path)
        root = tree.getroot()
        backglass_image_found = False
        dmd_image_found = False
        for image_type in root.findall(".//Images/*"):
            image_data = image_type.get("Value")
            image_data_decoded = base64.b64decode(image_data)
            if image_type.tag == 'BackglassImage':
                backglass_image_found = True
                if not os.path.exists(backglass_image_path):
                    extracted_backglass_images.append(backglass_image_path)
                    with open(backglass_image_path, "wb") as img_file:
                        img_file.write(image_data_decoded)
            elif image_type.tag == 'DMDImage':
                dmd_image_found = True
                if not os.path.exists(menu_image_path):
                    extracted_menu_images.append(menu_image_path)
                    with open(menu_image_path, "wb") as img_file:
                        img_file.write(image_data_decoded)

        if not backglass_image_found:
            print(f"Warning: 'BackglassImage' not found in .directb2s file for game '{game_name}'.")
            backglass_images_not_found.append(game_name)
        if not dmd_image_found:
            print(f"Warning: 'DMDImage' not found in .directb2s file for game '{game_name}'.")
            dmd_images_not_found.append(game_name)

    return games_to_skip, extracted_backglass_images, extracted_menu_images, backglass_images_not_found, dmd_images_not_found

def main():
    overwrite_option = input("If images already exist, should we overwrite them, or skip? (Overwrite/Skip , default: Skip) ").lower()
    overwrite = overwrite_option.startswith('o')
    
    print("Scanning 'VisualPinball/Tables'.")
    directb2s_files = extract_images_from_directb2s("VisualPinball/Tables")
    print(f"'{len(directb2s_files)}' .directb2s files were found:\n")
    for file in directb2s_files:
        print(f"{os.path.dirname(file)} <DIR>")
        print(f"\t{os.path.basename(file)} <FILE>")
    print()
    user_input = input(f"I found '{len(directb2s_files)}' .directb2s files in 'VisualPinball/Tables'. Do you want to extract and export images to the 'PinUPSystem/POPMedia/Visual Pinball X/Backglass/' and 'PinUPSystem/POPMedia/Visual Pinball X/Menu/' folders? (Y/N) ")
    if user_input.lower() in ('y', 'yes'):
        output_directory_backglass = "PinUPSystem/POPMedia/Visual Pinball X/Backglass/"
        output_directory_menu = "PinUPSystem/POPMedia/Visual Pinball X/Menu/"
        games_skipped, extracted_backglass, extracted_menu, backglass_not_found, dmd_not_found = extract_images(directb2s_files, output_directory_backglass, output_directory_menu, overwrite)
        print("\nExtraction completed.\n")
        print("\nEXTRACTION SUMMARY")
        print("------------------------------------------------")
        if games_skipped:
            print("The following games were skipped because both Backglass and Menu images already exist:")
            for game in games_skipped:
                print(f"- {game}")
                
        if extracted_backglass:
            print("\nBackglass images were successfully extracted for the following games:")
            for game in extracted_backglass:
                print(f"- {os.path.basename(game)}")
                
        if extracted_menu:
            print("\nMenu images were successfully extracted for the following games:")
            for game in extracted_menu:
                print(f"- {os.path.basename(game)}")
                
        if backglass_not_found:
            print("\nBackglass images were not found in the following games:")
            for game in backglass_not_found:
                print(f"- {game}")
                
        if dmd_not_found:
            print("\nDMD images were not found in the following games:")
            for game in dmd_not_found:
                print(f"- {game}")
    else:
        print("Goodbye!")

if __name__ == "__main__":
    main()
