# pyqt-matplotlib-scatter-plots-example
Showcase of interaction of PyQt GUI and Matplotlib Scatter Plot (with LassoSelector)

The module helps optimize image size when generating image models.

You can use it by selecting and removing overly large and excessively small images from the graph.

I made this by reading this <a href="https://medium.com/analytics-vidhya/how-to-pick-the-optimal-image-size-for-training-convolution-neural-network-65702b880f05">article</a>.

Read the article to know how this works. After all this package is just an example of utilizing that article's example :)

## How to Install
1. git clone ~
2. pip install -r requirements.txt
3. move your folders which contains the image files to src, you can see each iamges in the graph
- if you don't have anything, default images directories are prepared in src folder (Alzheimer's Disease MRI, Parkinson's Disease MRI)

## Preview

![image](https://github.com/yjg30737/pyqt-matplotlib-scatter-plots-example/assets/55078043/dabb0f7e-1053-4a9a-9341-51adb2177f9b)

Images are distributed according to their sizes.

## How to Use

https://github.com/yjg30737/pyqt-matplotlib-scatter-plots-example/assets/55078043/a56d6f84-0fe5-4ca3-9c3d-e2844116c496

Ignore the dark part of the video :)

Select the dots (which are corresponding with image file inside the directory) with lasso, and delete them at the widget on the right side of the window.

<b>If you press the "delete" button, it actually deletes the images. So you have to back them up before you use this.</b>

You can view an underlying image when you click on a specific dot. This could help you make a more careful decision about whether to remove it or not.

## Help Me!

I don't know how to refresh the chart after deleting files, so if you want to help me, I will be really glad.
