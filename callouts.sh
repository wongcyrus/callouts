git clone https://github.com/wongcyrus/ExcelLexBot
cd ExcelLexBot
./setup.sh
sudo ./get_layer_packages.sh
source deployment.sh
cd ..
git clone https://github.com/wongcyrus/callouts
cd callouts
./deploy_chatbot.sh
./setup.sh
sudo ./get_layer_packages.sh