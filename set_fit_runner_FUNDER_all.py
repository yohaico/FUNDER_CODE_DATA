import pprint
from datasets import Dataset
import pandas as pd
import set_fit_runner as set_fit_runner
import os
from definitions import ROOT_DIR
import re
import dir_files_scan_util as dir_files_scan_util
from pathlib import Path

tmp_train_dict_list = list()
tmp_test_dict_list = list()
q_path = os.path.join(ROOT_DIR, 'data', 'Q-Sort')
run_list = dir_files_scan_util.get_files_path_by_ext_top_dir(q_path, "csv")
cat_ctr = 0
for var in run_list:
    stem = Path(var).stem
    stem = re.sub(r"^\d+.", "", stem).strip()
    tmp_train_dict_list.append({'text': str(stem), 'label': cat_ctr})
    df_tmp_var = pd.read_csv(var, index_col=0)
    tmp_list = df_tmp_var["response"].tolist()
    for idx in range(0, 20, 1):
        tmp_train_dict_list.append({'text': tmp_list[idx], 'label': cat_ctr})
    for idx in range(20, len(tmp_list), 1):
        tmp_test_dict_list.append({'text': tmp_list[idx], 'label': cat_ctr})
    cat_ctr += 1

dir_model = os.path.join(ROOT_DIR, "model")
dir_files_scan_util.make_dirs_if_needed(dir_model)
dir_all = os.path.join(ROOT_DIR)

train_df = pd.DataFrame(tmp_train_dict_list)
train_df = train_df.sample(frac=1).reset_index(drop=True)
test_df = pd.DataFrame(tmp_test_dict_list)
test_df = test_df.sample(frac=1).reset_index(drop=True)
train_df.to_csv(dir_all + r"\train_balanced.csv", index=False, encoding="utf_8_sig")
test_df.to_csv(dir_all + r"\test_balanced.csv", index=False, encoding="utf_8_sig")

train_df_dict = Dataset.from_pandas(train_df)
test_df_dict = Dataset.from_pandas(test_df)
tmp_train_dict_list.clear()
tmp_test_dict_list.clear()
res, res_model = set_fit_runner.run_setfit(train_df_dict, test_df_dict, dir_model)
pprint.pprint(res)
res_text = pprint.pformat(res)
with open(dir_model + "\\" + "result_evaluate.txt", 'w', encoding="utf8", errors='ignore') as output_file:
    output_file.write(res_text.strip())
predictions_list = res_model(test_df["text"].tolist())
results_df_df = test_df
results_df_df["result"] = predictions_list.tolist()

results_df_df.to_csv(dir_all + r"\results_df.csv", index=False, encoding="utf_8_sig")
exit(0)
