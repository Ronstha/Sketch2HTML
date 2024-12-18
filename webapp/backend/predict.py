
import numpy as np
import random
import cv2
import math
import tensorflow.keras.backend as K
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers 
from PIL import Image
MAX_SEQ_LEN=120
input_shape=(850,600,1)
tokens=[
    '<PAD>',
    '{',
    '}',
    'row',
    'header',
    'footer',
    'container',
    'text',
    'text-r',
    'text-c',
    'flex-sb',
    'flex',
    'flex-c',
    'flex-r',
    'image',
    'carousel',
    'paragraph',
    'div-3',
    'div-6',
    'div-12',
    'div-9',
    'input',
    'nav',
    'logodiv',
    'navlink',
    'table',
    'button',
    'button-c',
    'button-r',
    'card',
    '<END>',
    '<START>'
]
t2v={}
v2t={}
for i in range(len(tokens)):
    v2t[i]=tokens[i]
    t2v[tokens[i]]=i
def dsltotoken(dsl):
    tks=['<START>']
    for tk in [i.strip() for i in dsl.strip().split('\n')]:
      if tk=="": continue
      if(tk.endswith("{")):
        tks.append(tk[:-1])
        tks.append(tk[-1])
      else:
        tks.append(tk)
    tks.append('<END>')
    return [t2v[tokens] for tokens in tks]

def tokentodsl(tokens):
    tokens=[v2t[vec] for vec in tokens]
    if tokens[0]=="<START>":
        tokens.pop(0)
    if tokens[-1]=="<END>":
        tokens.pop()
    txt=""
    stack=[]

    for i in tokens:
      if(i=="{"):
        txt+="{"
        stack.append("{")
        continue
      elif(i=="}"):
        stack.pop()

      txt+='\n'+'\t'*len(stack)+i
    txt=txt.strip()
    return txt
def masked_accuracy(label, pred):
  """
  Calculates the masked accuracy between the true labels and predicted labels.
  Args:
      label: A tensor of shape (batch_size, seq_length) containing the true labels.
      pred: A tensor of shape (batch_size, seq_length, target_vocab_size) containing the predicted labels.
  Returns:
      A scalar tensor representing the masked accuracy value.
  """
  pred = tf.argmax(pred, axis=2)
  label = tf.cast(label, pred.dtype)
  match = label == pred

  mask = label != 0

  match = match & mask

  match = tf.cast(match, dtype=tf.float32)
  mask = tf.cast(mask, dtype=tf.float32)
  return tf.reduce_sum(match)/tf.reduce_sum(mask)
def masked_loss(label, pred):
  """
  Calculates the masked sparse categorical cross-entropy loss between the true labels and predicted labels.
  Args:
      label: A tensor of shape (batch_size, seq_length) containing the true labels.
      pred: A tensor of shape (batch_size, seq_length, target_vocab_size) containing the predicted labels.
  Returns:
      A scalar tensor representing the masked loss value.
  """
  mask = label != 0
  loss_object = tf.keras.losses.SparseCategoricalCrossentropy(
    from_logits=True, reduction='none')
  loss = loss_object(label, pred)

  mask = tf.cast(mask, dtype=loss.dtype)
  loss *= mask

  loss = tf.reduce_sum(loss)/tf.reduce_sum(mask)
  return loss


    

class ConvolutionalTokenizer(layers.Layer):
    """
    Creates Convolutional Tokens of images for feeding to Transformer Encoder.
    """
    def __init__(self,kernel_size=3,stride=1,padding=1,pooling_kernel_size=3,pooling_stride=2,conv_layers=2,num_output_channels=[32, 64],**kwargs,):
        super(ConvolutionalTokenizer, self).__init__(**kwargs)
        
        # Creating a Sequential Keras Model for Tokenizing images
        self.conv_model = keras.Sequential()
        self.conv_model.add(layers.Conv2D(32,7,1,padding="valid",use_bias=False,activation="relu"))
        self.conv_model.add(layers.ZeroPadding2D(1))   
        self.conv_model.add(layers.MaxPool2D(3, 2, "same"))
        self.conv_model.add(layers.Conv2D(64,5,1,padding="valid",use_bias=False,activation="relu"))
        self.conv_model.add(layers.ZeroPadding2D(1))   
        self.conv_model.add(layers.MaxPool2D(3, 2, "same"))
        self.conv_model.add(layers.Dropout(0.1))
        self.conv_model.add(layers.Conv2D(64,3,1,padding="valid",use_bias=False,activation="relu"))
        self.conv_model.add(layers.ZeroPadding2D(1))   
        self.conv_model.add(layers.MaxPool2D(3, 2, "same"))
        self.conv_model.add(layers.Conv2D(128,3,1,padding="valid",use_bias=False,activation="relu"))
        self.conv_model.add(layers.ZeroPadding2D(1))   
        self.conv_model.add(layers.MaxPool2D(3, 2, "same"))
        self.conv_model.add(layers.Dropout(0.1))
        self.conv_model.add(layers.Conv2D(128,3,1,padding="valid",use_bias=False,activation="relu"))
        self.conv_model.add(layers.ZeroPadding2D(1))   
        self.conv_model.add(layers.MaxPool2D(3, 2, "same"))
  
  
     
    def call(self, images):
        # Reshaping the outputs by flattening them
        outputs = self.conv_model(images)
        Flattened = tf.reshape(
            outputs,
            (-1, tf.shape(outputs)[1] * tf.shape(outputs)[2], tf.shape(outputs)[3]),
        )
        return Flattened

    # Adding Learnable Positional Embeddings
    def pos_embeddings(self, image_size):
        inp = tf.ones((1, image_size[0], image_size[1],1))

        out = self.call(inp)

        seq_len = tf.shape(out)[1]
        projection_dim = tf.shape(out)[-1]

        
        embed_layer = layers.Embedding(
            input_dim=seq_len, output_dim=projection_dim
        )
        return embed_layer, seq_len

def load_image(im):
       
        thresh= cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 41, 21)
        kernel = np.ones((2,2), np.uint8)
        # thresh=cv2.erode(thresh,kernel)
        # thresh=cv2.dilate(thresh,kernel)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        coords=cv2.findNonZero(thresh)
        x, y, w, h = cv2.boundingRect(coords)
        img=thresh[:y+h,:]
        h,w=img.shape
        width=600
        height=math.ceil((h/w)*width)
        if height>850:
            height=850
            width=math.ceil((w/h)*height)
            
        resized=cv2.resize(img,(width,height),interpolation=cv2.INTER_AREA)
        resized[resized>15]=255
        resized[resized!=255]=0
        h,w=resized.shape
        oset=0
        if width<600:
            oset=(600-width)//2
        image=np.zeros((850,600))
        image[:h,oset:w+oset]=resized
        
        # resized=cv2.resize(im,(input_shape[1],input_shape[0]),interpolation=cv2.INTER_AREA)
        # _,thresh=cv2.threshold(resized,254,255,cv2.THRESH_BINARY_INV)
        image = image.astype(np.float32)
        image /= 255
        
        return image
model=tf.keras.models.load_model('model.h5',custom_objects={"ConvolutionalTokenizer":ConvolutionalTokenizer,'masked_loss':masked_loss,'masked_accuracy':masked_accuracy})
def predict(file):
    image=load_image(cv2.imread(file,cv2.IMREAD_GRAYSCALE))
    cv2.imwrite('test.png',image)
    st=np.zeros(MAX_SEQ_LEN)
    st[0]=t2v['<START>']
    i=0
    while st[i]!=t2v['<END>']:
        pd=np.argmax(model.predict((np.array([image]),np.array([st])),verbose=0)[0][i])
        i+=1
        st[i]=pd
    return tokentodsl(st[1:i])
    

