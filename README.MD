# Hello there 👋🏼 
# This is The GIMP-helper github page

This is a small readme about the GIMP-helper plugin which helps to adjust images in order to place them in marketplaces.

The plugin was created only for personal usage and may look like something strange stuff. By the way, a saved a lot of time of mine and colleagues with the pressing one button instead of keeping in mind GIMP shortcuts and excluding some manual activities.

## Installation
To deploy this plugin you should to place the "adjust_image_for_MPs.py" file into GIMP's plugins folder.

To know where is GIMP plugins folder Open GIMP preferences and switch to "Folders" item and choose "Plugins" subitem. 
There will be paths where GIMP is looking when it loads plugins.

After placing the file in the folder just restart GIMP in case it was open.

If you are Linux or macOS user, then you can easily run deploy.sh file in a terminal window which has to be opened in the same directory where the file is located:

`source deploy.sh`

## Usage

After loading the plugin, your GIMP will have an additional menu at the top of GIMP which called "Seller Helper".
If you click it three options will appear:

1. ***"Adjust image for marketplaces"***
   
    This option will resize an image to 1200 and 1600 size of the image. If image's initial height and width are not proportional to 1200x1600 then the image will be increased and the image itself will be placed in the center. Also, all transparent areas will be replaced with a white background which is the requirement of some marketplaces for the first image (e.g. Yandex.Market and OZON).

2. ***"Save the file with transparency in the background***
   
    This option is like the first option except that instead of adding white background it will keep transparency as is and in case of required resize additional areas will be created as transparency. One more important thing is only PNG files support transparency, hence in any case file will be saved as PNG. If your file is PNG then it will override. If you have open another format file then a new file with the same name but PNG extension will be created.

3. ***"Adjust image for MP and save as with transparency and as well white background***

    This option will be helpful if you wanna save the file with transparency as well as ready for a place in marketplaces. Keeping file with transparency might be required in case if you gonna place the same file in different marketplaces who has different requirements for images. E.g. KazanExpress marketplace has requirements which say that image background has to be in another color than pure white (which is the requirement of most marketplaces).


