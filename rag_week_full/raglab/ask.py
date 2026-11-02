import argparse, json
from .core import answer_question

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('question')
    parser.add_argument('--top-k',type=int,default=5)
    parser.add_argument('--rerank',choices=['none','keyword','cross'],default='none')
    args=parser.parse_args()
    print(json.dumps(answer_question(args.question,args.top_k,args.rerank),indent=2,ensure_ascii=False))

if __name__=='__main__':main()
