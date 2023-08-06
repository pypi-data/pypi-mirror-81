# Introduction

Kayra is a python package that provides implementation of several data augmentation techniques mainly focusing on acoustic applications. Currently it supports two algorithms for acoustic data augmentation, Spec Augment and Mixup. 


## Installation

Clone the repository and install Kayra:

```
python setup.py sdist
pip install dist/kayra-0.1.tar.gz
```


## Usage

Import the module you wish to use and call the relevant method:

```python
from kayra.mixup import mixup
from kayra.spec_augment import spec_augment

spec_augment(spectrogram, num_masks=1, mask_type='mean', W=warp_parameter, T=time_blocks, F=frequency_bins)

# AND / OR

resulting_waveform, df = mixup(base_wave, overlap_wave, alpha=alpha, beta=beta)
```

### SpecAugment

```python
spec_augment(spec, num_masks=1, F=30, T=80, W=80, mask_type='mean', freq_mask=True, time_mask=True, time_warp=True)
```

The Spec Augment method applies three different transformations to a spectrogram: frequency masking, 
time masking, and time warping.

Time warp consists of a deformation of the spectrogram in the time direction, by warping a random point along the horizontal line passing through the center of the image either to the left or right. The distance to be warped is randomly selected from a range between 0-W.

Frequency masking works by randomly selecting a number of consecutive frequency channels to mask from a range between 0-F

Time masking consists of randomly selecting a number consecutive time bins to mask from a range between 0-T

This implementation allows 4 types of masking:

    - mean, sets the value of the mask to be the mean value of the spectrogram 

    - zero, sets the value of the mask to 0

    - min, sets the value of the mask to be the lowest value found in the spectrogram
    
    - max, sets the value of the mask to be the highest value found in the spectrogram

Finally, num_masks controls the number of masks that will be created in each axis

Figure 1 depict a Magnitude Spectrogram with no augmentation whilst Figure 2 showcases its SpecAugmented instance with all transformations.

![Original Mag Spectrogram](img/original.png)

Figure 1: *Magnitude Spectrogram with no augmentations*

![Spec Augmented Mag Spectrgram](img/augmented.png)

Figure 2: *Magnitude Spectrogram with time warp, frequency masking and time masking*

The method is best described here: https://arxiv.org/abs/1904.08779

**Parameters**

| Name | Type | Default | Description
| ---- | ---- | ---- | ----
| spec | np.ndarray | | The spectrogram
| num_masks | int | 1 | Number of masks that will be created in each axis
| F | int | 30 | Maximum number of frequency channels to be masked in each masking operation
| T | int | 80 | Maximum number of utterances of time to be masked in each masking operation
| W | int | 80 | Maximum number of utterances of time that will be warped
| mask_type | string | 'mean' | Type of masking. Valid values are 'mean', 'zero', 'min' or 'max'
| freq_mask | bool | True | Enable/disable frequency masking
| time_mask | bool | True | Enable/disable time masking
| time_warp | bool | True | Enable/disable time warping

**Returns**

np.ndarray -- The modified Spectrogram


### Mixup

```python
mixup(base_waveform, overlap_waveform, alpha=0.2, beta=None, base_wave_init=0, overlap_wave_start=0, overlap_wave_stop=None, keep_base_proportion=False)
```

The Mixup method generates a new waveform by computing the linear superposition 
of two input waveforms, including their labels, i.e.

```math
 x = \alpha  x_i + \beta  x_j \; , \quad y = \alpha  y_j + \beta  y_j 
```
where $`x`$ is the new waveform, and $`x_i`$, $`x_j`$ are the two waveforms beeing mixed, 
$`y`$ is the new label, and $`y_i`$, $`y_j`$ are the labels of the two waveforms beeing mixed, 

Note that the default algorithm uses $`(1 − \alpha)`$ instead of a $`\beta`$. 
We give a little more freedom by allowing the user to define $`\alpha`$ and $`\beta`$ separately.
If the user chooses not to define, we fall back to (1 − α).

This implementation accepts waveforms with different lengths. For this purpose, the input vectors 
are named `base_waveform` and `overlap_waveform`, where it is assumed that ```len(base_waveform) >= len(overlap_waveform)```. 
If ```len(base_waveform) > len(overlap_waveform)```, mixup will start at index `base_wave_init` for the base waveform and `overlap_wave_start` for the overlap_waveform.
If the lengths are equal, the input waveforms will be mixed in their entirety.

In any case, the resulting waveform will have length equal to the length of the `base_waveform` with target label $`y`$ 
of both input vectors.

This method returns the resulting waveform and a dictionary containing two rows, one for each target label of the original waveforms, 
in the following format.

Dictionary:

'label': a target label

'start_frame': the starting index of the linear combination

'end_frame': the ending index of the linear combination

'label_proportion_kept': The proportion of each label kept. Value can range from 0-1 and represent the $`\alpha`$ and $`\beta`$ values 


For example, consider that two small recordings of 3000 frames are been mixed with $`\alpha`$ and $`\beta`$ values of 0.2 and 0.8 respectively.
The resulting Dictionary would look like this:

```python
{
    'label': [0, 1], 
    'start_frame': [0, 0], 
    'end_frame': [3000, 3000], 
    'label_proportion_kept': [0.2, 0.8]
}   
```

Here, the label of `base_waveform` is always 0 and the label of `overlap_waveform` is always 1.

**Parameters**

| Name | Type | Default | Description
| ---- | ---- | ---- | ----
| base_waveform | np.ndarray | | The waveform that will be multiplied by $`\alpha`$
| overlap_waveform | np.ndarray | | The waveform that will be multiplied by $`\beta`$
| alpha | float | 0.2 | A weight between 0-1 
| beta | float | None | A weight between 0-1 or None. if None, will default to $`(1 − \alpha)`$
| base_wave_init | int | 0 | The starting index in the base waveform where the linear superposition will begin
| overlap_wave_start | int | 0 | The starting index in the overlap waveform where the linear superposition will begin, everything before will be ignored
| overlap_wave_stop | int | None | The last index in the overlap_waveform where the linear superposition will stop, everything after will be ignored
| keep_base_proportion | bool | False | When True, only the segment of the base_waveform that is superimposed will be weighted by $`\alpha`$. When False, The entire base_waform will be weighted by $`\alpha`$

**Returns**

np.ndarray -- The resulting waveform with length equal to that of the base_waveform

Dictionary -- Dictionary with both target labels, the proportion each one kept in the resulting waveform and the start and end frame where the overlap occurs

### Mix Random

```python
mix_random(base_waveform, overlap_waveform, alpha=0.2, beta=None, n_mixups=2)
```

High level function that will perform multiple mixups operations on the base_waveform

If the number of mixups operations chosen is too big, 
it will perform the maximum number of mixing operations possible

This method returns the resulting waveform and a list of dictionaries in the same format as the mixup method.


**Parameters**

| Name | Type | Default | Description
| ---- | ---- | ---- | ----
| base_waveform | np.ndarray | | The waveform that will be multiplied by $`\alpha`$
| overlap_waveform | np.ndarray | | The waveform that will be multiplied by $`\beta`$
| alpha | float | 0.2 | A weight between 0-1 
| beta | float | None | A weight between 0-1 or None. if None, will default to $`(1 − \alpha)`$
| n_mixups | int | 2 | The maximum number of times that the function will call the mixup method if possible

**Returns**

np.ndarray -- The resulting waveform with length equal to that of the base_waveform

List of dictionaries -- List of dictionaries wher eeach dictionary has both target labels, the proportion each one kept in the resulting waveform and the start and end frame where mixup occurs

## Examples

For every example, we will be assuming a dataset containing spectrograms in hdf5 format and using the ketos package. However the following implementation can be easily adapted to suit your needs

### SpecAugment -- Example 1

Here we will create a SpecAugmented instance for each sample in our training set

```python
import ketos.data_handling.database_interface as dbi
from kayra.spec_augment import spec_augment

# opening our database with append as we are going to write new augmented instances to it
db = dbi.open_file(database_file, 'a')

# retrieve the training data
train_data = dbi.open_table(db, "/train/data")

# for each sample in our training set, augment it using Spec Augment
for spec in train_data:  
    spec_augmented = spec_augment(spec.data, num_masks=1, mask_type='mean', W=80, T=80, F=30)

    # write the resulting augmented spectrogram back to the training set along with the corresponding label
    dbi.write_audio(train_data, spec_augmented, label=spec.label)
```
### SpecAugment -- Example 2

Here we will be adding 5000 samples to our dataset by randomly choosing a sample from our dataset and augmenting it via the SpecAugment method
```python
import random
import ketos.data_handling.database_interface as dbi
from kayra.spec_augment import spec_augment

# opening our database with append as we are going to write new augmented instances to it
db = dbi.open_file(database_file, 'a')

# retrieve the training data
train_data = dbi.open_table(db, "/train/data")

# Augment 5000 times
for i in range(5000):  
    # randomly select a sample from the training set
    index = random.randrange(len(train_data))
    spec_augmented = spec_augment(train_data[index].data, num_masks=1, mask_type='mean', W=80, T=80, F=30)

    # write the resulting augmented spectrogram back to the training set along with the corresponding label
    dbi.write_audio(train_data, spec_augmented, label=train_data[index].label)
```

### SpecAugment -- Example 3

This time, lets again add 5000 samples to our training set, however only from one particular class.


```python
import random
import ketos.data_handling.database_interface as dbi
from kayra.spec_augment import spec_augment

# opening our database with append as we are going to write new augmented instances to it
db = dbi.open_file(database_file, 'a')

# retrieve the training data
train_data = dbi.open_table(db, "/train/data")

# Assuming our dataset only contains two class, 0 and 1 lets add 5000 samples to the positive class
# Here we are using pytables built in method to filter for the positive class. Adapt it to suit your needs
train_positive = [row for row in train_data.read_where("label == 1")]

# train_positive now contains only the training samples from the positive class

# Augment 5000 times
for i in range(5000):  
    # randomly select a sample from the positive samples
    index = random.randrange(len(train_positive))
    spec_augmented = spec_augment(train_positive[index].data, num_masks=1, mask_type='mean', W=80, T=80, F=30)

    # write the resulting augmented spectrogram back to the training set along with the corresponding label
    dbi.write_audio(train_data, spec_augmented, label=train_positive[index].label)
```

### Mixup -- Example 1
Here we will simply mixup 2 waveforms and save the resulting one

```python
import soundfile as sf
from kayra.mixup import mixup

# Ensure both waveforms have the same sample rate
base_wave, base_sr = sf.read(file1)
overlap_wave, overlap_sr = sf.read(file2)
new_wave, annotations = mixup(base_wave, overlap_wave, alpha=0.2, beta=0.8)

# Here we are creating a new .wav file for the resulting waveform, however you may already add it to your pipeline or whatever dataset format you are using
sf.write('data/train/augmented_wav', new_wave, base_sr)
```

### Mixup -- Example 2 
Now, assuming we have a dataset with several wav recordings, lets augment it by 5000 samples, this time by creating 5000 new .wav files.

```python
import random
from kayra.mixup import mixup
import soundfile as sf

# Augment 5000 times
for i in range(5000):
    # Here assume that train_dataset is a pandas dataframe that contains the location of the audio samples
    # ramdomly select two samples from our pandas dataframe
    base_index = random.randrange(len(train_dataset))
    overlap_index = random.randrange(len(train_dataset))

    file1 = os.path.join('path/to/file/', train_dataset[base_index].location)
    file2 = os.path.join(os.getcwd()+'/data/train', train_dataset[overlap_index].location)

    base_wave, base_sr = sf.read(file1, sr=None)
    overlap_wave, overlap_sr = sf.read(file2, sr=None)


    # annotations will contain a dictionary with the annotations of the new sample. 
    # Adapt it to your need and add it to your annotations dataset
    new_wave, annotations = mixup(base_wave, overlap_wave, alpha=0.2, beta=0.8)


    new_file_name = 'augmented_' + str(i) + '.wav'
    # Instead of adding the new augmented data to a hdf5 dataset, lets create a .wav file to contain the augmented sample.
    sf.write('data/train/' + new_file_name, new_wave, base_sr)
```

### Mixup -- Example 3
Now lets add 5000 samples to our training set, however only from one particular class.

```python
import random
import pandas as pd
from kayra.mixup import mixup
import soundfile as sf

# Assuming we have a pandas dataframe with the annotations where 0 is the negative class and 1 is the postivie class.
# split it between the positive and negative class
df1, df0 = [x for _, x in dataset_df.groupby(dataset_df['label'] == 0)]


# Augment 5000 times
for i in range(5000):
    # ramdomly select two samples from our set
    # here we guarantee that the overlap_index will always reference a postive label
    # Therefore our new augmented sample will contain information from a positive sample
    base_index = random.randrange(len(df0))
    overlap_index = random.randrange(len(df1))

    file1 = os.path.join('path/to/file/', df0[base_index].location)
    file2 = os.path.join(os.getcwd()+'/data/train', df1[overlap_index].location)

    base_wave, base_sr = sf.read(file1)
    overlap_wave, overlap_sr = sf.read(file2)

    new_wave, annotations = mixup(base_wave, overlap_wave, alpha=0.2, beta=0.8)
    # annotation will conatain both labels since the new sample is composed of 20% from the nagative class and 80% from the positive class
    # as specified by the alpha and beta.

    # Since we only care about the positive class lets remove the row containing the negative class
    # Lets convert our dictionary to a Pandas DataFrame for easier data manipulation
    new_df = pd.DataFrame(annotations) 

    # deleting label 0
    new_df = new_df[new_df.label != 0]

    new_file_name = 'augmented_' + str(i) + '.wav'
    # write the new wave
    sf.write('data/train/' + new_file_name, new_wave, base_sr)

    # after adapting the df lets add the annotations back to our dataset containing the labels
    dataset_df = pd.concat([dataset_df, new_df])

```


### Contributing

We welcome all contributions! If you find a bug or have a suggestion, please open an issue.
