#!/usr/bin/env python

from gimpfu import *

def add_watermark(image, text, points, antialias, opacity,margin, fontname, color):
 
    #undo-start
    pdb.gimp_context_push();
    pdb.gimp_image_undo_group_start(image);
    
    x = 0
    y = 0
    border = 0

    text_layer = pdb.gimp_text_fontname(image, None, x, y, text, border, antialias, points, 1, fontname) #points = 1, pixels = 0 
    
    x = image.width - text_layer.width - margin         #right
    y = image.height - text_layer.height - margin       #bottom
    pdb.gimp_layer_set_offsets(text_layer, x, y)

    pdb.gimp_layer_set_opacity(text_layer, opacity)
    pdb.gimp_text_layer_set_color(text_layer, color)
    pdb.gimp_text_layer_set_text(text_layer, text)
    pdb.gimp_item_set_name(text_layer, "Watermark")
    
    pdb.gimp_image_merge_down(image, text_layer, 0)

    #undo-end
    pdb.gimp_image_undo_group_end(image);
    pdb.gimp_context_pop();


register(
    "python-fu-add-watermark",
    "Adds watermark text",          # Information about the extension
    "Adds a text layer with watermark in which color, size, opacity, font, text antialias and margins can be customized.",  # Short description of the actions performed by the script
    "Petr Grachev",                 # Information about the author
    "Petr Grachev",                 # Information about copyright
    "2023",
    "Add Watermark",
    "*",
    [
        (PF_IMAGE, "image", "Image", None),
        (PF_TEXT, "copyright", "Copyright Owner", "Copyrighter"),
        (PF_INT, "points", "Size (pts)", 50),
        (PF_BOOL, "antialias", "Antialias", True),
        (PF_INT, "opacity", "Text opacity", 50),
        (PF_INT, "margin", "Margin (px)", 5),
        (PF_FONT, "fontname", "Font Name", "Sans"),
        (PF_COLOR, "color", "Color", (255, 255, 255)),
        ],
    [],
    add_watermark, 
    menu=("<Image>/My Extension/"), 
    )

main()
