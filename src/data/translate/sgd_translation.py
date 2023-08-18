import openai 
import pandas as pd
import time
from typing import List, Any
from tqdm import tqdm
tqdm.pandas()


class DialogTranslate:
    """
    A class to represent a Dialog Generation.
    Methods
    -------
    _dialog_generate(message):
        Call ChatGPT API
    generate_dialog():
        Generate annotated dialog
    """
    def __init__(self, 
                 openai_key:str, 
                 url:str,
                ):

        """
        Constructs all the necessary attributes for the DialogGenerate object.

        Parameters
        ----------
            openai_key : str
                a private key of ChatGPT
            url : str
                url to download dataset (.json)                     
        """       
        
        openai.api_key = openai_key
        self.url = url     
        self._load_data()


    def _load_data(self):       
        """
        Load data from url (.json)
        """
        self.data = pd.read_json(self.url)


    def _get_utterance(self, temp_df: Any) -> List:    
        """
        Get utterance from the dataframe of data
            Parameters:
                temp_df (str): a data dataframe 
            Returns:
                list_utterance (list): a list of utterances

        """        
        sub_df = pd.DataFrame(temp_df)
        return sub_df["utterance"].tolist()
        
    
    def _call_api(self, dialog: List, service: str) -> str:
        """
        Translate utterances to Vietnamese
        Args:
            dialog (list): a list of utterances
            service (str): domain of the dialog

        Returns:
            reply (str): translate result of ChatGPT API
        """
        message = f"""Translate this dialog to Vietnamese: {dialog} in service "{service[0].upper()}" with tone Natural"""
        messages = [{"role": "system", "content": "You are a intelligent assistant."}, 
                    {"role": "user", "content": message}]
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        reply = chat.choices[0].message.content
        
        return reply
    

    def _translate_utterances(self, dialog: List, service: str) -> str:
        """
        Translate utterances to Vietnamese
        Args:
            dialog (list): a list of utterances
            service (str): domain of the dialog

        Returns:
            reply (str): translate result of ChatGPT API
        """
        try:
            reply = self._call_api(dialog, service)
        except:
            # in time limit 
            print("Sleeping...")
            time.sleep(25)
            print("Translate...")
            reply = self._call_api(dialog, service)

        return reply
    

    def translate_dialog(self):
        """
        translate sgd dstc8 dataset
        Returns:
            result (.json): a dialog after translating 
        """        

        # get utterances
        self.data["utterances"] = self.data["turns"].apply(self._get_utterance)
        # translate utterances
        self.data["vi_utterances"] = self.data.progress_apply(lambda col: self._translate_utterances(col["utterances"], col["services"]), axis=1)
        # replace en to vi
        for _, row in self.data.iterrows():
            s = row["vi_utterances"]
            vi_list = s.strip("][").replace("""\"""", """'""").split("', '")
            for i in range(len(vi_list)):
                row["turns"][i]["utterance"] = vi_list[i]    
        # dataframe to json 
        result = self.data.to_json(orient="records", force_ascii=False)
        return result
        