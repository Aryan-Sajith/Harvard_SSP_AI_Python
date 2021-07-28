Firstly, when I tried the base program that Brian provided in the lecture I only ended up with about a 95% accurate program that averaged out around that mark.
Then I decided to try and experiment with different activation functions and I ended up finding one that turned out to be more optimized for cases that tend to
simply fall into the 0 range. After messing around with that activation function I ended up reaching about a 96% consistently, but still only reached about 97% rarely
as overfitting probably took its effect on the model and eventually the final test wouldn't even end up close to 97%. After this I realized that adding additional
convolutional layers could add greater consistency and greater modeling capabilities to my model... so I added another convolutional layer,  and after testing, I realized that
a layer with more filters than the first but a smaller kernel matrix was producing ideal results. 

After additional testing, I also came to the realization that Average pooling was netting  me more consistent results than the Max pooling method, so I decided to swap the max 
pooling layer for an average pooling one. My last few explorations came in the form of dropping the dropout rate to about 0.15 percent because I realized that significant dropout,
when the dataset is already substantially smaller than the one that Brian tested on in the lecture, would hinder the model's long-term success. After finding a sweet spot for the
dropout rate, I added a few extra layers to the actual DNN. First it had 256 units, then another layer with 192 units, and lastly 128 units. Firstly, I realized that having a layer
with double my base rate was good so I ended up using 256 units off of a base 128. Then I tested adding a layer inbetween with an average of the 1st/3rd layers. Although this
addition made the process produce slightly less accurate results, the overfitting seems to be a lot less than before since the performance on testing(non-epoch) set of data was 
within 1-1.5% of the actual data sets being tested on. I came to overall conclusion that this design for the AI model was the most efficient that I could find with research online of popular activation functions, alpha values, kernel sizes, etc.

Convolutional Neural Network Structure(Utilizing Leaky-ReLU Activation Function[ Alpha: 0.001]):

  - Convolutional layer with 32 filters and 4 x 4 kernel matrix.
  - Convolutional layer with 64 filters and 3 x 3 kernel matrix.
  - Average Pooling of size (3, 3).
  - Flattening.
  - Dense DNN Layer(256 Units).
  - Dense DNN Layer(192 Units).
  - Dense DNN Layer(128 Units).
  - Dropout DNN Layer(0.15 [~15%])
  - Output DNN Layer(Softmax Activation)
