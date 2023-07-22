# The important thing

updated july 22 2023 with more textures showing each stage of collisiontest, GRAY>B&W>Testarea1/2


https://github.com/AccelQuasarDragon/kivycollisiontest/assets/138998466/a4ad2184-ab13-41d7-bfbf-fb8999fe5588


https://github.com/AccelQuasarDragon/kivycollisiontest/assets/138998466/c58d794b-317e-4120-9c78-d9603de44060

TO RUN:

with poetry:

poetry update (to download stuff)
poetry shell (to get into the shell)
python drag2.py to run the example, the other examples were checking other stuff

with pip:

I did `poetry export --without-hashes --format=requirements.txt > requirements.txt` so u should be able to pip install from requirements.txt

TODO:
    test it out on a non-mask image,grayConversion is on so it should work on any kivy widget... > WORKS
    bugs: it's just messed up, only works between the first and 2nd widget

# explanation:


to get the image from the testwidget you have helper functions:  

grayconversion > converts a numpy array to a gray image of dimension: (width, height) 

widgettomask > gets the image of the widget using .originalguy which is just the widget image saved using self.export_as_image(). This is because when I testing grayconversion would be applied multiple times, wiping out the mask. I only needed to get the image once, hence saving at some time later

after grayconversion u make bw which is the actual black/white image. black is 0, white is 255. this super matters because np logic u want ur object to be nonzero 

pixelcollider is hell, this is literally what checks for collision

min/max of x/y is just to help you place ur widgets in the large testarea, this is because the actual origin of the widget is 0,0 on the bottom left of each widget and ACTUAL 0,0 of the pos is the origin of the root widget, in this case FileSpace which is parent of the FileBox. This is also because the original example is some filechooser: https://stackoverflow.com/questions/58800955/kivy-dragbehavior-dragging-more-than-one-widget

next is testarea1 and testarea2. TL:DR; testarea1 has 1 widget, testarea2 has 2nd widget. both testareas have a black bg (which is a value of 0), and then I place the corresponding widget mask using this huge line in numpy `testarea1[widget1yoffset:widget1yoffset+widget1VAR.height,widget1xoffset:widget1xoffset+widget1VAR.width]`

after u have the 2 testareas done, u can now check for collision. This is as per:  https://stackoverflow.com/a/23655364 
u need some elementwise checking if some pixel is nonzero (white) in the same spot in testarea1 AND testarea2. This is why ur mask is white, because if ur color is say 100 from widget 1 and color 2 in the same area is 240 in widget 2 u can't check for collision with `finaltest = testarea1 & testarea2`

last bits are to show it on the large canvas, since finaltest is of dimension (maxY-minY, maxX-minX) it cannot be shown as a kivy texture. This is because available textures are basically rgb/rgba, we're missing 4 dimensions. to make a 1d array> 4d, I did `finaltest = np.stack((finaltest,)*4, axis=-1).astype(np.uint8) `. reference here: https://stackoverflow.com/a/40119878 

ALSO, it's Y before X because of orientation, numpy are arrays, up>down, L>R, but kivy draws from bottom left, so Down>Up, L>R. if you mix the dimensions u get a SUPER messed up image.

after that u create the texture with texture.create, blit buffer with bytes (.tobytes creates a bytes image, and blitbuffer takes numpy arrays of the correct format, in this case it's (height, width, 4) (4 for RGBA, u can see it by printing any numpy array's shape, array.shape, I also like looking at the actual array by printing it just to double check, it's how I RE-figured out the orientation issue))

next is then `self.ids["collisionspace"].texture = newtexture` which updates the texture, you can improve this by doing reloadobserver as per: https://kivy.org/doc/stable/api-kivy.graphics.texture.html#reloading-the-texture


# RE: shapechange.py and fulltrans.py

I spent ~1 hr checking it out, no joke it is possible to emulate the JS/chromium effect, but it will take a while. I would also advise just taking the dive and learning JS. I could do it but it would take like 3 months, no joke. 

relevant links:

https://stackoverflow.com/questions/31458331/running-multiple-kivy-apps-at-same-time-that-communicate-with-each-other

https://stackoverflow.com/questions/39359950/how-do-i-have-multiple-windows-in-kivy

PLAN:

ur main python file is going to have several kivy windows spawned with multiprocessing, each cropped out using window.shape and some numpy magic to make the shape png  and of the relevant opacity as per 
https://stackoverflow.com/questions/72496870/window-shape-change-not-working-properly-in-kivy

then to communicate with each other I would use shared dictionaries to pass whatever data is required, but keep each widget as modular as possible.

however, a more critical issue is that u asked for two things:

transparent in OBS

opaque on monitor

This i don't think is possible (software wise), even with using js/webtech. This is because things are only rendered in one opacity as far as i know. if ur transparent in OBS, ur gonna be transparent in the display and vice versa.

hardware wise, there is a technique: 

key + fill:

https://obsproject.com/forum/threads/window-capture-transparency-no-color-key.11781/post-66060

however obs does not support that, but vmix might
https://www.reddit.com/r/VIDEOENGINEERING/comments/10yem9v/comment/j7y23de/?utm_source=share&utm_medium=web2x&context=3

related stuff to read:

stream avatars does smth similar to what u want

https://docs.streamavatars.com/stream-avatars/how-to-overlay/obs

clone so u can look at some code: https://github.com/haliphax/hxavatars


TL:DR;

It is possible to replicate the chromium streamelements/chat overlay 
for OBS, but would be slight hell to do.

for Kivy, transparency is done in 2 ways, shaped window and 
transparency as per: https://stackoverflow.com/questions/59223007/
how-to-make-transparent-screen-on-desktopapp-in-kivy

HOWEVER, ur request might be undoable since as far as I know things 
only have 1 opacity.

If u still want some obs overlay, it's time to learn some js I guess...
