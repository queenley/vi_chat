import argparse
import json
from sgd_translation import DialogTranslate
    

def make_parser():
    parser = argparse.ArgumentParser("Vietnamese Dialog Translation", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("--key", 
                        type=str, 
                        required=True, 
                        help="the private key of ChatGPT API")
    parser.add_argument("--repo_url", 
                        type=str, 
                        default="https://raw.githubusercontent.com/google-research-datasets/dstc8-schema-guided-dialogue/master/test/",
                        help="the url contains all dataset")
    parser.add_argument("--num", 
                        type=int, 
                        default=34,
                        help="the number of urls")
    parser.add_argument("--save_path", 
                        type=str, 
                        default="./dataset/",
                        help="the path to save")

    return parser


if __name__=="__main__":
    args = make_parser().parse_args()            
    for idx in range(args.num):
        # get url
        url = f"{args.repo_url}/dialogues_{str(idx+1).zfill(3)}.json"
        # translate
        translator = DialogTranslate(args.key, url)        
        result = translator.translate_dialog()
        # write result
        with open(f"{args.save_path}/{url.split('/')[-1]}", "w") as f:
            json.dump(result, f)
        print(f"\nThe dialog is saved to {args.save_path}")
        