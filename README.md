# Steganography Detection Tool

A real-time steganography detection tool that uses SRM filters and a Convolutional Neural Network (CNN) to detect hidden data inside images.

## What This Project Does
This tool analyzes any image and detects whether secret data has been hidden inside it using LSB (Least Significant Bit) steganography. It outputs a confidence score showing how likely the image contains hidden data.

## How It Works
1. **SRM Filter** — strips the image content and extracts only the noise map
2. **CNN Model** — analyzes the noise map to detect steganographic patterns
3. **Confidence Score** — outputs a 0-100% probability of hidden data

## Project Structure
```
stegoproject/
├── srm_test.py                        
├── stego_image.py                     
├── comparison_1.py                    
├── cnn_model.py                       
├── training_of_cnn.py                 
├── images_creation.py                 
├── stego_images_of_image_creation.py  
├── checking_one.py                    
└── real_time_training_the_images.py   
```

## Technologies Used
- Python 3.11
- PyTorch
- OpenCV
- NumPy
- Stegano
- Matplotlib

## Dataset
- 300 clean images downloaded from Unsplash
- 300 stego images generated using LSB steganography
- Total: 600 balanced labelled samples
- Split: 80% training / 20% validation

## CNN Architecture
```
Input (256x256 grayscale)
    ↓
Conv Layer 1 (32 filters) + ReLU
    ↓
Average Pooling
    ↓
Conv Layer 2 (64 filters) + ReLU
    ↓
Average Pooling
    ↓
Fully Connected (128 neurons)
    ↓
Sigmoid Output (0-100% probability)
```

## How To Run

### Install dependencies
```
pip install torch torchvision opencv-python numpy stegano matplotlib
```

### Create stego dataset
```
python images_creation.py
python stego_images_of_image_creation.py
```

### Train the model
```
python real_time_training_the_images.py
```

## Results
- Dataset: 600 images (300 clean, 300 stego)
- Training samples: 480
- Validation samples: 120
- Model saved as: stego_cnn.pth

## Future Work
- Add Random Forest classifier for improved accuracy on small datasets
- Build real-time drag and drop detection interface
- Expand dataset to 1000+ images for better CNN performance
- Add support for detecting multiple steganography methods

## References
- SRM Filters: Fridrich and Kodovsky, 2012
- YeNet Architecture: Ye et al., 2017
- BOSSBase Dataset: Bas et al., 2011

- ## Background
Steganography is the practice of hiding secret data inside ordinary files. 
Unlike encryption which scrambles data, steganography conceals the existence 
of the data entirely. LSB (Least Significant Bit) steganography hides data 
in the last bit of each pixel — invisible to the human eye but detectable 
through statistical analysis using SRM filters and machine learning.
