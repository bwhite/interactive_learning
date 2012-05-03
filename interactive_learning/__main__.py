import argparse
import vidfeat
import tempfile
import shutil
import picarus
import time
import hadoopy
import hashlib
import random
import subprocess


def run_video_frame_classification(train_dir):
    try:
        neg_dir = train_dir + '/0'
        pos_dir = train_dir + '/1'
        while 1:
            # Train using initial pos/neg
            c = vidfeat.SyntheticFrameFeature().train(vidfeat.load_label_frames(train_dir))
            # Predict on dataset
            hdfs_input = random.sample(hadoopy.ls('/user/brandyn/aladdin/mp4_devt/'), 96)
            start_time = '%f' % time.time()
            hdfs_output = '/user/brandyn/aladdin_results/video_grep/%s' % start_time
            picarus.vision.run_video_grep_frames(hdfs_input, hdfs_output, c)
            unsorted_dir = tempfile.mkdtemp()
            try:
                for _, y in hadoopy.readtb(hdfs_output):
                    open('%s/%s.jpg' % (unsorted_dir, hashlib.sha1(y).hexdigest()), 'w').write(y)
                # Present results to user and add to list
                try:
                    cmd = 'python -m interactive_learning.image_selector %s %s %s --port 8083' % (unsorted_dir, pos_dir, neg_dir)
                    print(cmd)
                    subprocess.call(cmd.split())
                except OSError:
                    pass
            finally:
                shutil.rmtree(unsorted_dir)
    finally:
        #shutil.rmtree(temp_root)
        pass


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('method', choices=('classification', 'detection'))
    return vars(parser.parse_args())


def main():
    config = parse()
    if config['method'] == 'classification':
        run_video_frame_classification('/home/brandyn/playground/synthetic_data')
    else:
        raise ValueError


if __name__ == '__main__':
    main()
