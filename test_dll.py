import sys
import os

def main():
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    print("Base path:", base_path)
    
    lib_path = os.path.join(base_path, "lib")
    print("Lib path:", lib_path)
    
    if os.path.exists(lib_path):
        print("Files in lib:")
        for f in os.listdir(lib_path):
            print("  ", f)
    else:
        print("Lib path does NOT exist!")
        print("Root contents:")
        for f in os.listdir(base_path):
            print("  ", f)

if __name__ == "__main__":
    main()
