import argparse
from .core import retrieve, keyword_rerank, cross_encoder_rerank

def main():
    p=argparse.ArgumentParser()
    p.add_argument('question')
    p.add_argument('--method', choices=['keyword','cross'],default='keyword')
    args=p.parse_args()
    hits=retrieve(args.question,8)
    ranked=keyword_rerank(args.question,hits) if args.method=='keyword' else cross_encoder_rerank(args.question,hits)
    for name,items in [('ORIGINAL',hits[:3]),('RERANKED',ranked[:3])]:
        print(f'\n{name}:')
        for h in items: print(f'  {h["source"]}: {h["text"][:95]}')

if __name__=='__main__':main()
