# 3Dmodelize
Création IA pour la Forward

Install python dependancies :
  - Tensorflow : Library for the AI implementation
  - Open3D : Library used for creating the furniture's 3D model (1 unit corresponds to 1 centimeter)
  - Pillow : Library used to look into the image's pixels

```bash
pip3 install --user tensorflow open3d Pillow more_itertools
```

Generating the dataset :

```bash
./generate_database.sh links
```

Debugging a non functionnal link :

```bash
./info.sh "https://..." # The link that poses problem
cat dimentions.txt      # file where the dimentions are stored
eog img.jpg             # file that has the image of the furniture
```

Generating a 3D model :

```bash
./modelize.py path/to/file/furniture_XX-XX-XX.jpg output_file.ply [ -v | -w ]
# use -v when you want a visualisation of the generated model and -w when you want to see the wireframe
```
