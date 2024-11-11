with open('output/wuwa/wuwa.txt', 'w') as file:
    file.write('wuwa success')

from modules.utility import *

@log('WUWA START', 'WUWA FINISH')
def main():
    print('WUWA DONE')

main()