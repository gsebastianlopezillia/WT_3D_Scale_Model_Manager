import util.misc as misc

def main():
    kernel = misc.loadDLL("daKernel-dev.dll")
    print("Kernel:", type(kernel))
    try:
        oodle = kernel[574]
        print("Success! oodle:", type(oodle))
    except Exception as e:
        print("Error getting by ordinal:", e)

if __name__ == "__main__":
    main()
