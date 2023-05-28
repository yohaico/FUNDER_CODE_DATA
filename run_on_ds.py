import os
from setfit import SetFitModel
import pandas as pd
from definitions import ROOT_DIR

dir_ds = os.path.join(ROOT_DIR)
csv = r"enter_csv_name_here"
df = pd.read_csv(dir_ds + "\\" + csv + ".csv", index_col=0)

dir_model = os.path.join(ROOT_DIR, "model")
model = SetFitModel.from_pretrained(dir_model, local_files_only=True)
res_list = list()
vector_raw = list()
for i in range(1, 101, 1):
    vector_raw.append("FUNDER_" + str(i).zfill(3))

length = str(df.__len__())
for index, row in df.iterrows():
    tmp_dict = dict()
    tmp_dict["index"] = index
    tmp_dict["labels"] = row["labels"]
    text = row["text"]
    preds_proba = model.predict_proba([text]).tolist()
    return_dict = {labels: scores for labels, scores in zip(vector_raw, preds_proba[0])}
    preds = model([text]).tolist()[0]
    tmp_dict.update({"prediction": preds})
    tmp_dict.update(return_dict)
    res_list.append(tmp_dict)

out_df = pd.DataFrame(res_list)
out_df = out_df.round(decimals=2)
out_df.to_csv(dir_ds + "\\" + csv + "_out_vector.csv", index=False, encoding="utf_8_sig")
