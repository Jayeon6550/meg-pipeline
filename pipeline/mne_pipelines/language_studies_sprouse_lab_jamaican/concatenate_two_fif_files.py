

import mne



PATH_TO_FIF1 = r"C:\Users\hz3752\Box\MEG\Data\jamaican-language-study\sub-001\meg\sub-001_task-jamaican_meg-raw.fif"
PATH_TO_FIF2 = r"C:\Users\hz3752\Box\MEG\Data\jamaican-language-study\sub-001\meg\sub-001_task-jamaican_meg-raw.fif"

raw1 = mne.io.read_raw_fif(PATH_TO_FIF1)
raw2 = mne.io.read_raw_fif(PATH_TO_FIF2)

raws = [raw1, raw2]

concat_raw = mne.concatenate_raws(raws, preload=None, events_list=None, on_mismatch='raise', verbose=None)


concat_raw.save("concate_attempt.fif")

