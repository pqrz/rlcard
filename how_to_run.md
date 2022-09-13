Following are the steps to run the tarneeb game:

To Run WebApp
1. Login to Machine:                       (ssh to machine)
2. Activate Environment:                        conda activate /home/ubuntu/environments/pytorch_cpu
3. Location:                                              cd /home/ubuntu/work/tarneeb/codes/codes_v02_tarneeb_webapp/rlcard_tarneeb_webapp/rlcard/
4. Command to Run Training Script:     python demo_v3_gameplay_train.py (run if the .pth files are not created already at the location)
5. Command to run webapp:                  python app.py
6. Link to website:                                   http://<your IP>:5000/play


Note: to kill server running on port use command: fuser -k 5000/tcp

-------------------------------------------------------------------

(developer commands)
>>  rsync -av --exclude=".*" /home/ubuntu/work/tarneeb/codes/codes_v02_tarneeb_webapp/rlcard_tarneeb_webapp/rlcard/* ./



