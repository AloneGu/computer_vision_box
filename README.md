## computer_vision_box

## opencv version : 2.4.11

## example to match orb feature

        cd ORB

        python test_orb.py

## auto generate training data for human detection

        set these parameter in auto_generate_training_data/detect_motion.py
        VIDEO_DIR = '../video_data' # where is the videos
        OUTPUT_DIR = '/home/jac/Documents/work_tmp/' # where to save result
        PLACEMENT = '8100224' # device name
        PROCESS_DATE = '2016-03-05' # time

        cd auto_generate_training_data

        python detect_motion.py

        you will see result in OUTPUT_DIR

## recombine part of different videos in same place

        check concat_video