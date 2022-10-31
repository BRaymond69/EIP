from pygltflib import GLTF2
from pygltflib.validator import validate, summary

def main():
    glb_filename = "Templates/Bureau/Bureau_2.glb"
    glb = GLTF2().load(glb_filename)
    validate(glb)
    summary(glb)

if __name__ == "__main__":
    main()
