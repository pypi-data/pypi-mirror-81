import os
import keras
from nextoff.models.raw import TestModel

# =======================================================================================
# BEG: abstraction for train, test and eval of model
# =======================================================================================
def train_test_model_with(data, args, savename="bestmodel"):
    """
    + `args` must follow convention
    + data is of type `InMemoryImgHandler`
    """
    # initialize and build
    # --------------------
    baseline_model = TestModel(args)
    # compile
    baseline_model.compile(args)
    
    # Train eval, save and plot
    # -------------------------
    if 'v' in args.__dict__: v = args.v
    else: v = 0
    baseline_model.fit(
        (data.x_train, data.y_train),
        (data.x_val, data.y_val), 
        v, # verbose
        savename, 
        args
    )
    
    # Evaluate the performance (unseen data)
    baseline_model.evaluate(data.x_test, data.y_test, v=1)
    # plot
    baseline_model.plot()
# =======================================================================================
# END: abstraction for train, test and eval of model
# =======================================================================================