import cv2
import time
from airmouse.core.opencv_camera import OpenCVCamera
from airmouse.core.mediapipe_tracker import MediaPipeTracker
from airmouse.gestures.trainer import GestureTrainer
from airmouse.utils.logger import setup_logger

logger = setup_logger("train_cli")

def run_trainer(args=None):
    logger.info("Starting ML Calibration...")
    
    camera = OpenCVCamera()
    tracker = MediaPipeTracker()
    trainer = GestureTrainer(model_path="custom_gestures.pkl")
    
    if not camera.start():
        logger.error("Could not start camera for training.")
        return
        
    gestures_to_train = ["point", "pinch", "shaka", "double_pinch", "thumb_up", "thumb_down"]
    frames_per_gesture = 60 # 60 frames = approx 2 seconds of data
    
    cv2.namedWindow("AirMouse++ Trainer", cv2.WINDOW_NORMAL)
    
    print("========================================")
    print("Welcome to AirMouse++ ML Calibration!")
    print("We will learn your hand shapes for perfect accuracy.")
    print("Press 'q' at any time to quit.")
    print("========================================")
    
    try:
        for gesture in gestures_to_train:
            print(f"\n>>> PREPARE TO PERFORM: '{gesture}'")
            print("Get your hand ready in the camera view...")
            
            # Countdown
            for i in range(3, 0, -1):
                print(f"{i}...")
                
                # Show camera feed during countdown
                start_time = time.time()
                while time.time() - start_time < 1.0:
                    frame = camera.read_frame()
                    if frame is not None:
                        display_frame = frame.copy()
                        cv2.putText(display_frame, f"Get ready for '{gesture}': {i}", (50, 50), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
                        cv2.imshow("AirMouse++ Trainer", display_frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            return
                    else:
                        time.sleep(0.01)
                
            print(f"--- RECORDING '{gesture}' NOW ---")
            
            frames_collected = 0
            while frames_collected < frames_per_gesture:
                frame = camera.read_frame()
                if frame is None:
                    time.sleep(0.01)
                    continue
                    
                display_frame = frame.copy()
                tracking_data = tracker.process(frame)
                
                if tracking_data and "landmarks" in tracking_data:
                    trainer.add_sample(tracking_data["landmarks"], gesture)
                    frames_collected += 1
                    
                    # Draw visual feedback
                    cv2.putText(display_frame, f"Recording '{gesture}': {frames_collected}/{frames_per_gesture}", 
                                (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    cv2.putText(display_frame, "No hand detected! Show your hand.", 
                                (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                                
                cv2.imshow("AirMouse++ Trainer", display_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    return
                    
        print("\nAll gestures recorded! Training model...")
        
        # Display a "Training..." screen so it doesn't just freeze
        frame = camera.read_frame()
        if frame is not None:
            cv2.putText(frame, "Training Machine Learning Model...", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            cv2.imshow("AirMouse++ Trainer", frame)
            cv2.waitKey(1)
            
        success = trainer.train_and_save()
        if success:
            print("========================================")
            print("Calibration complete! You can now run 'airmouse start'.")
            print("========================================")
            
    finally:
        camera.stop()
        cv2.destroyAllWindows()
