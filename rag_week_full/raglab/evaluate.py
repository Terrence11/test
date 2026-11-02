import json, argparse
from pathlib import Path
from .core import retrieve, keyword_rerank

DATA=Path(__file__).resolve().parents[1]/'data'/'eval_questions.jsonl'

def main():
    p=argparse.ArgumentParser();p.add_argument('--rerank',choices=['none','keyword'],default='none');args=p.parse_args()
    rows=[json.loads(x) for x in DATA.read_text().splitlines() if x.strip()]
    hit1=hit3=0
    for item in rows:
        hits=retrieve(item['question'],8 if args.rerank=='keyword' else 3)
        if args.rerank=='keyword':hits=keyword_rerank(item['question'],hits)
        names=[h['source'] for h in hits[:3]]
        h1=item['expected_source'] in names[:1]
        h3=item['expected_source'] in names
        hit1+=h1;hit3+=h3
        print(f'{item["question"]} | top3={names} | top1={h1} top3={h3}')
    print(f'Hit@1={hit1}/{len(rows)} ({hit1/len(rows):.0%}) | Hit@3={hit3}/{len(rows)} ({hit3/len(rows):.0%})')

if __name__=='__main__':main()
