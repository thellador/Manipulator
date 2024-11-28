import multiprocessing
import signal
import sys

def run_main():
    import kinematics

def run_kinematics_and_arduino():
    import kinematics_and_arduino

def signal_handler(sig, frame):
    print("\nПрограмма завершена пользователем.")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    process1 = multiprocessing.Process(target=run_main)
    process2 = multiprocessing.Process(target=run_kinematics_and_arduino)

    process1.start()
    process2.start()

    process1.join()
    process2.join()
