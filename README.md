# B2S-2-PinUp-Image-Extractor
A small python script that extracts Backglass &amp; FullDMD images from .directb2s files, and saves them to PinUp Popper's media folder.

Right now it only works for VPX, but in the future, I may give it the option to work with FX2, FX3, and Future Pinball. Feel free to fork.

## Instructions 
1. Install "Pinup Popper Baller Installer"
2. Make sure your directory structure looks something like this.
```
vPinball
  FuturePinball
  Installer
  PinUPSystem
  VisualPinball
    Tables
      <YOUR TABLE FOLDER>
        YOUR TABLE.directb2s
      <YOUR 2nd TABLE FOLDER>
        YOUR 2nd TABLE.directb2s
```
3. Put ```b2s_2_PinUp_img_extractor.py``` in top level ```vPinball``` folder.
4. Once all your ```.directb2s``` files are in your corresponding table folders run ```b2s_2_PinUp_img_extractor.py```
```
python b2s_2_PinUp_img_extractor.py
```

Once completed this will be where the files are extracted to:

'Backglass' images should be saved in 'PinUPSystem/POPMedia/Visual Pinball X/Backglass/'

'DMD' images should be saved in 'PinUPSystem/POPMedia/Visual Pinball X/Menu/'

