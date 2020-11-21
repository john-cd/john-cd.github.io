---
title: Deep Learning - Convolutional Neural Networks for Image Classification
category: datascience 
tags: ML deep learning neural networks
featured_image: '/img/assets/convolutional_network_layer.png'
comments: true
---

I am teaching myself deep learning (DL), starting with the excellent [CNN Stanford course](http://cs231n.stanford.edu/) and working with the [Keras](https://keras.io) platform.

I should start by stating that Deep Learning is a rebranding of neural networks (NN). If I compare the state of the art to the 90's, when I first studied NN, what is truly new is our ability to train very complex networks with very large numbers of neurons and many hidden layers, which in turn can learn increasingly abstract representations of the input data. Modern Neural Networks can contain on orders of 100 million parameters (neuron weights) and are made up of 10-20 layers. 

Keys to the renewed interest in neural nets are as follows: 
- Computer power (especially GPUs) has increased around a million-fold, making standard backpropagation feasible for networks several layers deeper than what the [vanishing gradient problem](https://en.wikipedia.org/wiki/Vanishing_gradient_problem) had previously allowed. 
- Newer techniques, like convolutional neural networks (CNN, ConvNet), simplified activation schemes (rectified linear unit or ReLU neurons) and better optimization algorithms (Adam, quasi-Newton methods...) made NN training less painful computionally.
- The recent availability of powerful, easy-to-use, open-source deep learning frameworks such as TensorFlow, MxNet or Keras, has simplified NN architecture by allowing the practioners to build layer-by-layer from existing building blocks. 

To date, I am pretty impressed how quickly and naturally one can address problems like image classification with deep learning. I also look forward to applying that to trickier problems like sequence-to-sequence prediction and Natural Language Processing. Deep Learning is not a machine learning panacea, however. To a degree, it is a brute force approach revived by the cloud computing area with its almost unlimited amount of available computational power.


## Image Classification and Convolutional Neural Networks

Let's focus, in this first post, on image classification. Image data is by nature three-dimensional (width, height, depth equal to the number of color channels). Traditional ("dense" a.k.a. fully connected) Neural Nets treat the input data as a 1D vector. A better neural network would take in account the 3D structure of the image.  

Dense Neural Nets also do not scale well to large images, since by definition each neuron draws input from all pixels. Image information is localized: the neighbors of a pixel are more relevant than distant pixels, therefore neurons that process only portions of the input image (and vastly reduce the amount of parameters needed) make sense. Enter convolutional neural networks.

A Convolutional neural network layer consists of a set of learnable filters (more often called "kernels" in image processing). As it is sliding around the input image, each filter outputs for each pixel the weighted sum of its neighbors by element-wise multiplying the filter's weights with the original pixel values of the image then summing up - this is [multidimensional discrete convolution](https://en.wikipedia.org/wiki/Multidimensional_discrete_convolution). The weights are, in our case, 3D arrays that are small spatially (along width and height), but extend through the full depth of the input volume (i.e. use all three color channels).

The figure below illustrate how, in a CNN layer, a small region of the input image (the "receptive field", dashed line cuboid) is transformed into one intermediate output for each filter. The process is repeated for all pixels or a fraction thereof. Sometimes the neurons in each depth slice (at a given index along F) are constrained to use the same weights and bias, in order to to control the number of parameters.

![Convolutional Network Layer](/img/assets/convolutional_network_layer.png)

## Convolutional Neural Network Architecture

Multiple neural network layers of multiple types, including CNNs, are combined into a stack to form a complete classifier.

- A simple ConvNet for image classification could have the architecture ``[INPUT - CONV - RELU - POOL - FC]``

* ``INPUT`` ``[W x H x 3]`` holds the raw pixel values of the image (with three color channels).
* The ``CONV`` layer computes the output of neurons that are connected to local regions in the input, each computing a dot product between their weights and a small region they are connected to in the input volume. This results in a 3D tensor (``W x H x F volume``).
* ``RELU`` applies an elementwise activation function, leaving the volume unchanged.
* The ``POOL`` layer (non-linearily) downsamples operation along the spatial dimensions (width, height) resulting into a ``[W' x H' x F]`` volume, ``W' < W, H' < H``. A factor 2 is typical.
* The ``FC`` (fully-connected) layer compute the class scores, resulting in a m-dimensional vector, ``m`` being the number of classes.

- A classic architecture would feature more convolution layers and/or interspread pool / convolution layers e.g. ``[INPUT - CONV - RELU - CONV - RELU - POOL - RELU - CONV - RELU - POOL - FC]``.


## Implementation

I summarize below the practical takeaways of my deep learning reading so far. Feel free to comment to suggest more DL tips and tricks.  

### Data Preprocessing

- It is very important to zero-center the data, and it is common to see normalization of every feature in your data (e.g. one pixel in images) to have unit variance or scaling to [-1, 1]. 
- If your data is very high-dimensional, consider using a dimensionality reduction technique, such as PCA or even [Random Projections](http://scikit-learn.org/stable/modules/random_projection.html).
- PCA / Whitening transformations are not typically used with Convolutional Networks. 


### Weight Initialization

- Initialize the NN weights by drawing them from a gaussian distribution such as ``w = np.random.randn(n) * sqrt(2.0/n)``.


### Overfitting

- I learned that "it seems that smaller neural networks can be preferred if the data is not complex enough to prevent overfitting. However, this is incorrect - there are many other preferred ways to prevent overfitting in Neural Networks that we will discuss later (such as L2 regularization, dropout, input noise). In practice, it is always better to use these methods to control overfitting instead of the number of neurons.

The subtle reason behind this is that smaller networks are harder to train with local methods such as Gradient Descent: It’s clear that their loss functions have relatively few local minima, but it turns out that many of these minima are easier to converge to, and that they are bad (i.e. with high loss). Conversely, bigger neural networks contain significantly more local minima, but these minima turn out to be much better in terms of their actual loss. 

Larger networks will always work better than smaller networks, but their higher model capacity must be appropriately addressed with stronger regularization (such as higher weight decay), or they might overfit." 

### Regularization

- Use L2 regularization and dropout.
- Use batch normalization.


### Training 

- As a sanity check, make sure that the initial loss is reasonable, and that you can achieve 100% training accuracy on a very small portion of the data.
- During training, monitor the loss, the training/validation accuracy, and the magnitude of updates in relation to parameter values (it should be ~1e-3), and when dealing with ConvNets, the first-layer weights.
- The two recommended optimization methods are SGD + Nesterov Momentum or Adam.
- Decay your learning rate over the period of the training. For example, halve the learning rate after a fixed number of epochs, or whenever the validation accuracy tops off.


### Cross-validation

- Split your training data randomly into train/val splits using the usual rule of thumb (70-90% of your data into the training set). 
- This setting depends on how many hyperparameters you have and how much of an influence you expect them to have. If there are many hyperparameters to estimate, you should err on the side of having larger validation set to estimate them effectively. 
- As usual, if you are concerned about the size of your validation data, it is best to split the training data into folds and perform cross-validation.
- Search for good hyperparameters with random search (not grid search). Stage your search from coarse (wide hyperparameter ranges, training only for 1-5 epochs), to fine (narrower rangers, training for many more epochs).
- Create model ensembles for extra performance.




