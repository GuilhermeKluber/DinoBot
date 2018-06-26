from generation import Generation
from scanner import get_location


def main():
    generation = Generation()
    lx,ly,rx,ry=get_location()
    epoch= 0
    while True:
        epoch=epoch+1
        print("Geracao {}".format(epoch))
        generation.execute(lx,ly,rx,ry,epoch)
        generation.keep_best_genomes()
        generation.mutations()

if __name__ == '__main__':
    main()
