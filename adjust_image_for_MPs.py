#!/usr/bin/env python

# Sample Shell Rel 1
# Created by Tin Tran
# Comments directed to http://gimpchat.com or http://gimpscripts.com
#
# License: GPLv3
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY# without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# To view a copy of the GNU General Public License
# visit: http://www.gnu.org/licenses/gpl.html
#
#
# ------------
#| Change Log |
# ------------
# Rel 1: Initial release.
import math
import os
import string
from gimpfu import *
import gimpfu
from array import array

""" =================== CONST =================== """
WIDTH = 1200
HIEGHT = 1600

"""
===========================FILE SAVERS========================
"""

def save_file(image, layer, filename=None):
	if not filename:
		filename = pdb.gimp_image_get_uri(image)
	filename = filename.replace('file://', '')
	pdb.gimp_message(str(filename))
	pdb.gimp_file_save(
		image,
		layer,
		filename,
		'?'
	)


def save_file_as_png(image, layer, filename):
	old_image_base_name = os.path.basename(filename)
	old_image_path = os.path.dirname(filename)
	new_filename = os.path.splitext(old_image_base_name)[0] + ".PNG"
	_filename = os.path.join(old_image_path, new_filename)
	save_file(image, layer, filename=_filename)


def add_suffix_to_filename(filename, suffix):
	old_image_base_name = os.path.basename(filename)
	old_image_path = os.path.dirname(filename)
	new_filename = os.path.splitext(old_image_base_name)[0] + suffix + os.path.splitext(old_image_base_name)[1]
	new_file_path = os.path.join(old_image_path, new_filename)
	return new_file_path

"""
======================IMAGE SIZES=====================
"""

# changing the scale of image, in order to adjust requirements
# this procedure makes images width equal to 1200 if image's height won't be higher than 1600
# or makes image's height equal to 1600 if inages width won't be hire than 1600

def change_scale(image):
	w = image.width
	h = image.height

	big_w = w*HIEGHT/h

	big_h = h*WIDTH/w

	if big_h > HIEGHT:
		pdb.gimp_image_scale(image, big_w, HIEGHT)
	else:
		pdb.gimp_image_scale(image, WIDTH, big_h)

# Adjust image size
# Image's height have to be equal 1600
# and Image's width have to be equal 1200

def resize_image(image):

	y_offset = (HIEGHT - image.height)/2
	x_offset = (WIDTH - image.width)/2

	pdb.gimp_image_resize(image, WIDTH, HIEGHT, x_offset, y_offset)


def prepare_image_for_marketplaces(image):
	change_scale(image)
	resize_image(image)

"""
================LAYERS====================
"""
def add_white_layer(image):
	newLayer = pdb.gimp_layer_new(image, image.width, image.height, 0, "White Layer", 100, 0)
	pdb.gimp_context_set_background((255, 255, 255))
	pdb.gimp_drawable_fill(newLayer, gimpfu.BACKGROUND_FILL)
	image.add_layer(newLayer, 1) #TODO chnage to insert layer


"""
================GIMP main functions====================
"""

def change_scale_and_save_file_with_transparency(image, layer):
	pdb.gimp_image_undo_group_start(image)
	pdb.gimp_context_push()

	prepare_image_for_marketplaces(image)

	pdb.gimp_layer_resize_to_image_size(layer)
	merged_layer = pdb.gimp_image_merge_visible_layers(image, CLIP_TO_IMAGE)
	save_file_as_png(image, merged_layer, pdb.gimp_image_get_uri(image))

	pdb.gimp_context_pop()
	pdb.gimp_image_undo_group_end(image)
	pdb.gimp_displays_flush()

def adjust_image_for_mps(image, layer) :
	pdb.gimp_image_undo_group_start(image)
	pdb.gimp_context_push()

	change_scale(image)
	resize_image(image)
	layer = image.layers[0]

	pdb.gimp_selection_invert(image)
	pdb.gimp_layer_resize_to_image_size(layer)
	add_white_layer(image)
	layer = pdb.gimp_image_merge_visible_layers(image, CLIP_TO_IMAGE)
	save_file(image, layer)

	pdb.gimp_context_pop()
	pdb.gimp_image_undo_group_end(image)
	pdb.gimp_displays_flush()


def change_scale_and_save_file_with_transparency_in_separate_file(image, layer):

	new_image = pdb.gimp_image_duplicate(image)
	pdb.gimp_image_set_filename(new_image, add_suffix_to_filename(pdb.gimp_image_get_uri(image), '_TR'))

	new_image_layer = pdb.gimp_image_get_active_layer(new_image)
	change_scale_and_save_file_with_transparency(new_image, new_image_layer)
	pdb.gimp_image_delete(new_image)

	pdb.gimp_image_undo_group_start(image)
	pdb.gimp_context_push()

	prepare_image_for_marketplaces(image)
	add_white_layer(image)
	merged_layer = pdb.gimp_image_merge_visible_layers(image, CLIP_TO_IMAGE)
	save_file(image, merged_layer)

	pdb.gimp_context_pop()
	pdb.gimp_image_undo_group_end(image)
	pdb.gimp_displays_flush()

register(
	"python_fu_adjust_image_for_mps",                           
	"Make image convinient for marketplaces",
	"Make image convinient for marketplaces",
	"Ildarworld",
	"Ildarworld",
	"2020",
	"<Image>/Seller Helper/Adjust image for marketplaces", #Menu path
	"RGB*, GRAY*", 
	[
	],
	[],
	adjust_image_for_mps)

register(
	"python_fu_change_scale_and_save_file_with_transparecny",                           
	"Adjust image for MP and save file with transperency",
	"Adjust image for MP and save file with transperency",
	"Ildarworld",
	"Ildarworld",
	"2020",
	"<Image>/Seller Helper/Save the file with transparency in the background", #Menu path
	"RGB*, GRAY*", 
	[
	],
	[],
	change_scale_and_save_file_with_transparency)

register(
	"python_fu_change_scale_and_save_file_with_transparency_in_separate_file",                           
	"Adjust image for MP and save file transparetly (separate file)",
	"Adjust image for MP and save file transparetly (separate file)",
	"Ildarworld",
	"Ildarworld",
	"2020",
	"<Image>/Seller Helper/Adjust image for MP and save as with transparency and as well white background", #Menu path
	"RGB*, GRAY*", 
	[
	],
	[],
	change_scale_and_save_file_with_transparency_in_separate_file)



main()
