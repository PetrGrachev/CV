#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gimpfu import *

def apply_gradient(image, drawable, mode):
    from math import sqrt
    
    pdb.gimp_context_push()
    pdb.gimp_image_undo_group_start(image)

    if pdb.gimp_drawable_is_rgb(drawable):
       pdb.gimp_image_convert_grayscale(image)

    height = pdb.gimp_image_height(image)
    width = pdb.gimp_image_width(image)

    for y in range(0, height - 1):
        for x in range(0, width - 1):

            current = pdb.gimp_drawable_get_pixel(drawable, x, y)[1][0]                
            down = pdb.gimp_drawable_get_pixel(drawable, x, y + 1)[1][0]                  
            right = pdb.gimp_drawable_get_pixel(drawable, x + 1, y)[1][0]               

            gx = int(abs(right - current))
            gy = int(abs(down - current))

            if (mode==False): #magnitude mode
                value = int(sqrt(gx*gx + gy*gy)) 
                if value > 255: 
                    value = 255

            else: #direction mode
                direction = math.atan2(gy, gx)
                direction_degrees = math.degrees(direction) #to degrees

                if direction_degrees < 0:
                    direction_degrees += 360

                value = int((direction_degrees / 360) * 255)
                #value = int(255 / (1 + math.exp(-direction_degrees)))

            pdb.gimp_drawable_set_pixel(drawable, x, y, 1, [value])
            
    for x in range(0, width): #Bottom edge
        current = pdb.gimp_drawable_get_pixel(drawable, x, height-2)[1][0]
        pdb.gimp_drawable_set_pixel(drawable, x, height-1, 1, [current])

    for y in range(0, height): #Right edge
        current = pdb.gimp_drawable_get_pixel(drawable, width-2, y)[1][0]
        pdb.gimp_drawable_set_pixel(drawable, width-1, y, 1, [current])

    pdb.gimp_drawable_shadows_highlights(drawable, 80, 0, 0, 100, 50, 0, 0) #makes image lighter
    
    pdb.gimp_displays_flush()

    pdb.gimp_image_undo_group_end(image)
    pdb.gimp_context_pop()

register(
          "python-fu-apply-gradient",                            
          "Applies a gradient effect in two modes",           
          "Applies a gradient effect in two modes",
          "Petr Grachev",                 # Information about the author
          "Petr Grachev",                 # Information about copyright    
          "2023",                                                  
          "apply_gradient",                                      
          "*",                                                     
          [
              (PF_IMAGE, "image", "Original image", None),       
              (PF_DRAWABLE, "drawable", "Source layer", None),   
              (PF_BOOL, "mode", "Mode(No-magnitude, Yes-direction)", False)   
          ],
          [],
          apply_gradient, menu="<Image>/My Extension/")

main()