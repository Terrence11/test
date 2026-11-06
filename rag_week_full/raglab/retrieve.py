import argparse
from .core import retrieve

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('question')
    parser.add_argument('--top-k',type=int,default=5)
    args=parser.parse_args()
    for h in retrieve(args.question,args.top_k):
        print(f'\nsource={h["source"]} id={h["id"]} cosine_distance={h["distance"]:.3f}\n{h["text"]}')

if __name__=='__main__':main()
