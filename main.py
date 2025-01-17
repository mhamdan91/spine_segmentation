import training
import tensorflow as tf
import warnings
import argparse
from termcolor import colored
import os
sep = os.sep
tf.logging.set_verbosity(tf.logging.ERROR)  # disable to see tensorflow warnings

'''
This module takes in arguments from user to configure
the training/prediction process
'''

def predictor(batch_size = 2, train_mode=0, epochs_= 2, visualize=0, ckpt_path= None, images_path=None, masks_path=None ):
    """

    :param batch_size: consumed batch size by the network at each training step
    :param train_mode: determines training mode. If set to 0 then model is in prediction mode, if set to 1 then model will train from an existing
    checkpoint, and if set to 2 the model will train from scratch.
    :param epochs: number of forward and backward passes to train the model for.
    :param visualize: determines which dataset to visualize. 0 for training dataset and 1 for validation.
    :param checkpoint_path: path to existing checkpoint in case train_mode equals 0 or 1.
    :param images_path: path to images to be used for training or prediction
    :param masks_path:  path to ground truth masks to be used for training or prediction
    :return: None

    """
    # Do sanity checks before running the code
    if batch_size > 15 or batch_size<1: batch_size = 2
    if train_mode > 2 or train_mode<0: train_mode = 0
    if visualize > 1 or visualize <0: visualize = 0
    if not os.path.exists(ckpt_path):
        warnings.warn(colored("Model checkpoints/weights does not exist - continuing without checkpoints", "magenta"))

    assert os.path.exists(images_path) != False, "Provided directory does not exist!"
    assert os.path.exists(masks_path) != False, "Provided directory does not exist!"
    ls_masks = os.listdir(masks_path)
    ls_images = os.listdir(images_path)
    assert len(ls_images) == len(ls_masks), "Please verify that each image corresponds to a mask"
    assert len(ls_images) != 0, "Provided directory is empty!"
    training.train(batch_size, train_mode, epochs_,visualize, ckpt_path, images_path, masks_path)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--batch_size', default=2, type=int, help='Batch size between 1 & 15 -- default: 2 ')
    parser.add_argument('-t', '--train_mode', default=0, type=int, help='0: Predict, 1: Train from a previous checkpoint, 2: Train from scratch -- default: 0')
    parser.add_argument('-v', '--visualize', default=0, type=int, help='0: Visualize training samples, 1: visualize validation samples -- default: 0')
    parser.add_argument('-e', '--training_epochs', default=2, type=int, help='-- default: 2')
    parser.add_argument('-k', '--ckpt_path', default='checkpoints'+sep+'pre_trained.h5', type=str, help='(Optional, provide path to checkpoints in case of '
                            'train_mode = 0 or 1) -- default: checkpoints'+sep+'pre_trained.h5')
    parser.add_argument('-i', '--images_path', default='data_files'+sep+'images', type=str, help='(Optional, provide path to input images in case of '
                        'training on a different dataset - must be .png) -- default: data_files'+sep+'images')
    parser.add_argument('-m', '--masks_path', default='data_files'+sep+'masks', type=str, help='(Optional, provide path to input masks in case of '
                        'training on a different dataset - must be .npy) -- default: data_files'+sep+'masks')
    args = parser.parse_args()
    predictor(args.batch_size, args.train_mode, args.training_epochs,args.visualize, args.ckpt_path, args.images_path, args.masks_path)

if __name__ == '__main__':
    main()
