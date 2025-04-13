# Barcode Images Name Format

`t{barcode number}_{flags}` where

- Images with the same barcode number correspond to the same barcode
- Flags describe the image
  - `s` = (screenshot) the image is taken from [the USPS IMb decoder/encoder page](https://postalpro.usps.com/ppro-tools/encoder-decoder)
  - `c` = (camera) the image was taken with the Raspberry Pi camera
  - `i` = (isolated) barcode is the only thing in the image
  - `m` = (multiple) there's multiple objects in the image
  - `p` = (perpendicular) the image is rotated so the barcode's long side is vertical
  - `r` = (rotated) the image is rotated to an arbitrary degree
