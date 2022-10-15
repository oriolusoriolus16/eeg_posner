import numpy as np
import mne
import pandas as pd
import matplotlib.pyplot as plt

START_TIME = [1180, 701, 566, 493, 477, 463, 448, 528, 398, 795]

#   0. X - start time of Posner task in EEG 

X = 0


#   1. Time intervals (task trials)

database = []

for k in range(1, 11):

    results_posner = pd.read_csv('results_posner_{}.csv'.format(k))
    results_posner.head(10)
    results_posner.sample(10)
    
    
    list_of_errors = results_posner['error']
    list_of_intervals = results_posner['r_time'] 
    new_list_of_intervals = []
    for i in range(len(list_of_intervals)):
        if list_of_errors[i] == 2 or list_of_errors[i] == 3:
            new_list_of_intervals.append((1200 + list_of_intervals[i]+1150)/1000)
                   
        else:
            new_list_of_intervals.append((1200 + list_of_intervals[i])/1000)
            
          
    print(new_list_of_intervals)
    
    sum_time = sum(new_list_of_intervals)
    print(f'Sum_time: {sum_time}')
    print(len(new_list_of_intervals))
    print(sum_time/60)
    
    #   2. Cutting of EEG recordings
    
    sample_data_folder = mne.datasets.sample.data_path()
    sample_data_raw_file = (sample_data_folder / 'MEG' / 'sample' /
                            '{}.edf'.format(k))
    
    raw = mne.io.read_raw_edf(sample_data_raw_file)
    raw.crop(tmin = START_TIME[k-1]).load_data()
    print(k)
    data = []
    for i in range(0, len(new_list_of_intervals)):
    
        t_idx = raw.time_as_index([0., new_list_of_intervals[i]])
        channels, times = raw[:, t_idx[0]:t_idx[1]]
        data.append(channels)
        print(len(data))
        raw.crop(tmin = new_list_of_intervals[i]+1)
    
    database.append(data)
    
df = pd.DataFrame(database)
df.to_csv('eeg_data_posner', index=False, header=False)
#raw.plot_psd(fmax=100)
#raw.plot(duration=5, n_channels=30)


#   3. Sampling data

#in_time = X + new_list_of_intervals
#for i in new_list_of_intervals:
#    for j in 





        


