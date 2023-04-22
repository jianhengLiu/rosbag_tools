# rosbag_merge
Merge rosbag according to msg's time stamp

Credit to https://blog.csdn.net/Bryantaoli/article/details/105155757

I modified the script to use msg's header stamp replace the record time so that msg could be replace in their own publish stamp.


**merge bags & sync with header time**
```
python merge_bag.py rim_output_g1019_2_sync_merge.bag rim_output_g1019_1.bag rim_output_g1019_2.bag -v -t '/neural_slam/mesh /neural_slam/mesh_color /neural_slam/pose /neural_slam/path /camera/color/image_raw /tf'
```
**sync with header time**
```
python merge_bag.py rim_output_g1019_2_sync.bag rim_output_g1019_2.bag -v -t '/neural_slam/mesh /neural_slam/mesh_color /neural_slam/pose /neural_slam/path /camera/color/image_raw /tf'
```
