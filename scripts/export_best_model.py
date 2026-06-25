import os
import glob
import shutil

def export_latest_model():
    # 1. Find all feature_columns.txt files in mlruns
    mlruns_dir = os.path.join(os.path.dirname(__file__), "..", "mlruns")
    search_pattern = os.path.join(mlruns_dir, "**", "feature_columns.txt")
    
    # Use glob with recursive=True
    all_feature_files = glob.glob(search_pattern, recursive=True)
    
    if not all_feature_files:
        print("❌ No models found in mlruns. Run the pipeline first!")
        return

    # 2. Get the latest one by modification time
    latest_feature_file = max(all_feature_files, key=os.path.getmtime)
    artifacts_dir = os.path.dirname(latest_feature_file)
    
    print(f"🔍 Found latest model artifacts at: {artifacts_dir}")
    
    # 3. Create export directory
    export_dir = os.path.join(os.path.dirname(__file__), "..", "model_export")
    if os.path.exists(export_dir):
        shutil.rmtree(export_dir)
    os.makedirs(export_dir, exist_ok=True)
    
    # 4. Copy the MLflow model folder contents into export_dir
    model_src_dir = os.path.join(artifacts_dir, "model")
    for item in os.listdir(model_src_dir):
        s = os.path.join(model_src_dir, item)
        d = os.path.join(export_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)
            
    # 5. Copy the extra artifacts
    shutil.copy2(os.path.join(artifacts_dir, "feature_columns.txt"), export_dir)
    shutil.copy2(os.path.join(artifacts_dir, "preprocessing.pkl"), export_dir)
    
    print(f"✅ Successfully exported model and artifacts to {export_dir}")
    print("   Ready to build Docker image!")

if __name__ == "__main__":
    export_latest_model()
