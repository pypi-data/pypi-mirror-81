

# pytorch-vision-classifier	

The main target of this template is to help during building your classification model where:

1. It helps load the dataset whether the dataset in one directory or multiple directories
2. It shows the dataset details once the dataset directory has been specified
3. It helps know the available GPU devices and pick one to use easily
4. It helps get a pre-trained model for you with the last layer updated with or without a dropout layer and initialized by an algorithm you choose from the most common initialization algorithms
5. It helps know the GPU memory usage of your model
6. It helps understand the timing of different steps during model training
7. It helps find the best learning rate using the algorithm published by Leslie N. Smith in the paper Cyclical Learning Rates for Training Neural Networks. [The original code](https://github.com/davidtvs/pytorch-lr-finder)
8. It provides a dashboard to monitor your model during the training process
9. It helps track the metric that you choose to find the best model for your problem
10. It provides a compressed version of your model to be used for deployment purpose

In order to install, you need to download [pytorch](https://pytorch.org/get-started/locally/).
then open the command prompt and type:
```
pip install pytorch_vision_classifier
```