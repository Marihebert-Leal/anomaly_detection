# anomaly_detection
Script to analyze purchases within a social network of user's, detecting any behavior that is far from the average within that social network
# Getting Started
Two set data: " batch_log.json" and "stream_log.json". Both files are in the log_input folder.
The first file, batch_log.json, contains past data that should be used to build the initial state of the entire user network, as well as 
the purchase history of the users.
Data in the second file, stream_log.json, should be used to determine whether a purchase is anomalous.
Two parameters: 
D:the number of degrees that defines a user's social network.
T: the number of consecutive purchases made by a user's social network (not including the user's own purchases)
The first line of batch_log.json contains a JSON object with the parameters: degree (D) and number of tracked purchases (T) to consider 
for calculation.
To run the script use run.sh 
the script results are saved in "flagged_purchases.json" in log_output folder.
the path and names of the input and output files can be modified in the run.sh
# Prerequisites
Python 2.7 or newer
# Sample Data
You can find a medium sized sample data set in the sample_dataset folder.
