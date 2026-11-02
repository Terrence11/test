import argparse
from .core import load_chunks, embed_texts, get_collection

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--size',type=int,default=75)
    parser.add_argument('--overlap',type=int,default=15)
    args=parser.parse_args()
    chunks=load_chunks(args.size,args.overlap)
    if not chunks: raise RuntimeError('No Markdown files found in data/docs')
    print(f'Embedding {len(chunks)} chunks (uses paid API)...')
    vectors=embed_texts([c.text for c in chunks])
    col=get_collection()
    # Recreate content deterministically on each indexing run, avoiding stale chunks.
    existing=col.get()['ids']
    if existing: col.delete(ids=existing)
    col.upsert(ids=[c.id for c in chunks],documents=[c.text for c in chunks],embeddings=vectors,metadatas=[{'source':c.source,'chunk_index':c.chunk_index} for c in chunks])
    print(f'Indexed {col.count()} chunks in local Chroma.')

if __name__=='__main__':main()
