import chat_gpt_run
import re
import pandas as pd
from pathlib import Path
import os
from definitions import ROOT_DIR
import logger as logger

txt_file_path = os.path.join(ROOT_DIR, "data", r"Riverside Situational Q-sort Version 4.0.txt")
dir_path = os.path.join(ROOT_DIR)
with open(txt_file_path) as f:
    lines = f.readlines()
text = ""
subject = ""
for idx in range(len(lines)):
    line = str(lines[idx]).strip()
    if idx % 2 == 0:
        subject = line
        continue
    else:
        if Path(dir_path + subject + ".csv").exists():
            logger.print_msg("found  " + subject)
            continue
        text = str(lines[idx]).strip()
        res = chat_gpt_run.get_response(text)
        # dd = res["choices"][0]["message"]["content"]
        list_res = res.split("\n")
        res_list = list()
        for item in list_res:
            if len(item.strip()) == 0:
                continue
            sub = re.sub(r"\d+\.", "", string=item)
            res_list.append(sub.strip())
            continue
        df = pd.DataFrame(res_list)
        df.columns = ["response"]
        df.index += 1
        df.to_csv(path_or_buf=dir_path + subject + ".csv", index_label="index",
                  index=True)
        logger.print_msg("finished " + subject)
        text = ""
        subject = ""
        continue
exit(0)
