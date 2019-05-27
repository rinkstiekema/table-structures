import os,time,cv2, sys, math
import tensorflow as tf
import argparse
import numpy as np

from utils import utils, helpers
from builders import model_builder

# parser = argparse.ArgumentParser()
# parser.add_argument('--datadir', type=str, default=None, required=True, help='The image you want to predict on. ')
# parser.add_argument('--resultdir', type=str, default=None, required=True, help='The dir you want to save the predictions in')
# parser.add_argument('--checkpoint_path', type=str, default=None, required=True, help='The path to the latest checkpoint weights for your model.')
# parser.add_argument('--crop_height', type=int, default=512, help='Height of cropped input image to network')
# parser.add_argument('--crop_width', type=int, default=512, help='Width of cropped input image to network')
# parser.add_argument('--model', type=str, default=None, required=True, help='The model you are using')
# parser.add_argument('--dataset', type=str, default="CamVid", required=False, help='The dataset you are using')
# args = parser.parse_args()

# class_names_list = ['ruler', 'cell']
# label_values = [[255,0,0], [255,255,255]]
# num_classes = len(label_values)

# print("\n***** Begin prediction *****")
# print("Dataset -->", args.dataset)
# print("Model -->", args.model)
# print("Crop Height -->", args.crop_height)
# print("Crop Width -->", args.crop_width)
# print("Num Classes -->", num_classes)

def predict(checkpoint_path, datadir, resultdir, model):
	class_names_list = ['ruler', 'cell']
	label_values = [[255,0,0], [255,255,255]]
	num_classes = len(label_values)

	# Initializing network
	config = tf.ConfigProto()
	config.gpu_options.allow_growth = True
	sess=tf.Session(config=config)

	net_input = tf.placeholder(tf.float32,shape=[None,None,None,3])
	net_output = tf.placeholder(tf.float32,shape=[None,None,None,num_classes]) 

	network, _ = model_builder.build_model('encoder-decoder-skip', net_input=net_input,
											num_classes=num_classes,
											crop_width=1024,
											crop_height=1024,
											is_training=False)

	sess.run(tf.global_variables_initializer())

	print('Loading model checkpoint weights')
	saver=tf.train.Saver(max_to_keep=1000)
	saver.restore(sess, checkpoint_path)


	for image in os.listdir(datadir):
		print("Testing image " + image)
		file_name = os.path.join(datadir, image)
		loaded_image = cv2.imread(file_name)

		st = time.time()
		output_image = sess.run(network,feed_dict={net_input:input_image})

		run_time = time.time()-st

		output_image = np.array(output_image[0,:,:,:])
		output_image = helpers.reverse_one_hot(output_image)

		out_vis_image = helpers.colour_code_segmentation(output_image, label_values)
		file_name = os.path.join(resultdir, image)
		cv2.imwrite(file_name,cv2.cvtColor(np.uint8(out_vis_image), cv2.COLOR_RGB2BGR))

		print("Took %i"%run_time)
		# print("Finished!")
		# print("Wrote image " + "%s_pred.png"%(os.path.join(args.datadir,image)))		