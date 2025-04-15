import sys
import argparse

#-g for store and encrypt the key
#-k for decrypt the key












def main():

    if len(sys.argv) < 2:
        print("Error")
        sys.exit(1)

    parser = argparse.ArgumentParser(description = "OTP KEY")
    parser.add_argument('-k', type=syr , help = "Decrypt the Key ")
    parser.adda_rgument('-g', type=str , help="Encryt the Key ")
    args = parser.parse_args()

    if args.g:
        Encryt(int key)

    elif args.k:
        Decrypt(int key)
        
    else   
        print("please include only g or k")
        sys.exit(1)
  

if __name__ == "__main__":
    main()
