# update and upgrade apt
sudo apt update
sudo apt upgrade -y

# --- OLD STEPS ---
# # add Google package repo containing TFLite
# echo "deb [signed-by=/usr/share/keyrings/coral-edgetpu-archive-keyring.gpg] https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list

# # add GPG to keychain
# curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo tee /usr/share/keyrings/coral-edgetpu-archive-keyring.gpg >/dev/null

# # update package list to scan for new repo
# sudo apt update

# # install TFLite
# sudo apt install python3-tflite-runtime

# --- NEW STEPS ---
# install dependency to fix libcblas.so error (TFLite)
sudo apt install libatlas-base-dev

# install dependency to fix libopenjp2.so error (Pillow)
sudo apt-get install libopenjp2-7-dev

# install pip dependencies
source venv/bin/activate
pip install -r requirements.txt

# download model and labels
rm -rf data/
wget https://storage.googleapis.com/download.tensorflow.org/models/tflite/mobilenet_v1_1.0_224_quant_and_labels.zip -P data/
unzip data/mobilenet_v1_1.0_224_quant_and_labels.zip -d data/
rm data/mobilenet_v1_1.0_224_quant_and_labels.zip