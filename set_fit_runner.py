from sentence_transformers.losses import CosineSimilarityLoss
from sklearn.metrics import precision_recall_fscore_support, accuracy_score, confusion_matrix
from setfit import SetFitModel, SetFitTrainer
import pprint as pprint


def compute_metrics(labels, preds):
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='macro')
    acc = accuracy_score(labels, preds)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall,
    }


# Load SetFit model from Hub
model = SetFitModel.from_pretrained("sentence-transformers/paraphrase-mpnet-base-v2")


def run_setfit(train_ds, test_ds, model_path):
    # Create trainer
    trainer = SetFitTrainer(
        model=model,
        metric=compute_metrics,
        # metric="accuracy",
        train_dataset=train_ds,
        eval_dataset=test_ds,
        loss_class=CosineSimilarityLoss,
        batch_size=16,
        num_iterations=20,  # Number of text pairs to generate for contrastive learning
        num_epochs=1,  # Number of epochs to use for contrastive learning
    )
    # Train and evaluate!
    trainer.train()
    metrics_eval = trainer.evaluate()
    res = pprint.pformat(metrics_eval)
    trainer.model.save_pretrained(save_directory=model_path)
    return res, model
