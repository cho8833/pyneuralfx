import os
from utils import traverse_dir
import soundfile as sf

if __name__ == "__main__":
    print('> ================= Start Preprocessing =================  <')

    train_ratio = 0.6
    valid_ratio = 0.1
    test_ratio = 0.3

    assert (train_ratio + valid_ratio + test_ratio) == 1

    base_dir = "../data/amp/MarshallJVM410H"

    os.makedirs(base_dir, exist_ok=True)

    train_path_dir_x = os.path.join(base_dir, 'train', 'x')
    train_path_dir_y = os.path.join(base_dir, 'train', 'y')
    os.makedirs(train_path_dir_x, exist_ok=True)
    os.makedirs(train_path_dir_y, exist_ok=True)

    valid_path_dir_x = os.path.join(base_dir, 'valid', 'x')
    valid_path_dir_y = os.path.join(base_dir, 'valid', 'y')
    os.makedirs(valid_path_dir_x, exist_ok=True)
    os.makedirs(valid_path_dir_y, exist_ok=True)

    test_path_dir_x = os.path.join(base_dir, 'test', 'x')
    test_path_dir_y = os.path.join(base_dir, 'test', 'y')
    os.makedirs(test_path_dir_x, exist_ok=True)
    os.makedirs(test_path_dir_y, exist_ok=True)

    dirs = os.listdir(base_dir)

    # B0_M0_T0_G5\\B0_M0_T0_G5-input.wav          --- x
    # B0_M0_T0_G5\\B0_M0_T0_G5-preamp.wav         --- we don't use this
    # 'B0_M0_T0_G5\\B0_M0_T0_G5-speakerout.wav    --- y
    for _, directory in enumerate(dirs):
            if directory == 'test' or directory == 'train' or directory == 'valid':
                continue
            entries = os.listdir(os.path.join(base_dir, directory))

            print('fn_x: ', entries[0])
            print('fn_y: ', entries[2])

            wav_x, sr_x = sf.read(os.path.join(base_dir, directory, entries[0]))
            wav_y, sr_y = sf.read(os.path.join(base_dir, directory, entries[2]))

            min_len = min(len(wav_x), len(wav_y))
            wav_x = wav_x[:min_len]
            wav_y = wav_y[:min_len]

            print('> len(wav): ', len(wav_x))
            assert sr_x == sr_y
            assert len(wav_x) == len(wav_y)

            x_naming = "x_" + directory + ".wav"

            y_naming = "y_" + directory + ".wav"

            # train
            train_end = int(len(wav_x) * train_ratio)
            train_wav_x = wav_x[:train_end]
            train_wav_y = wav_y[:train_end]
            sf.write(os.path.join(train_path_dir_x, x_naming), train_wav_x, sr_x, subtype='PCM_24')
            sf.write(os.path.join(train_path_dir_y, y_naming), train_wav_y, sr_y, subtype='PCM_24')

            # valid
            valid_end = int(len(wav_x) * valid_ratio)
            valid_wav_x = wav_x[train_end:valid_end + train_end]
            valid_wav_y = wav_y[train_end:valid_end + train_end]
            sf.write(os.path.join(valid_path_dir_x, x_naming), valid_wav_x, sr_x, subtype='PCM_24')
            sf.write(os.path.join(valid_path_dir_y, y_naming), valid_wav_y, sr_y, subtype='PCM_24')

            # test
            test_end = int(len(wav_x) * test_ratio)
            test_wav_x = wav_x[valid_end + train_end:]
            test_wav_y = wav_y[valid_end + train_end:]
            sf.write(os.path.join(test_path_dir_x, x_naming), test_wav_x, sr_x, subtype='PCM_24')
            sf.write(os.path.join(test_path_dir_y, y_naming), test_wav_y, sr_y, subtype='PCM_24')

