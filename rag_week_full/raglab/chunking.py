import argparse
from .core import load_chunks

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--size',type=int,default=75)
    parser.add_argument('--overlap',type=int,default=15)
    args=parser.parse_args()
    chunks=load_chunks(args.size,args.overlap)
    print(f'Chunks: {len(chunks)} (size={args.size}, overlap={args.overlap})')
    for item in chunks:
        print(f'\n[{item.source} #{item.chunk_index} id={item.id}]\n{item.text[:220]}')

if __name__=='__main__':main()
