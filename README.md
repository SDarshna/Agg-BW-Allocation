# Agg-BW-Allocation
Allocating BW to a paticular agg BW region on PA using SASE APIs

CLI:
./RN-BW-allocation.py -t1 T1-secret.yml -Regname us-east -bw 200

Output:
--------------------------------
Script Execution Progress: 
--------------------------------
Login to TSG ID 1491283841 successful
BW Allocation Successful
+---------------+--------------+--------------+
| Agg BW Region | BW Allocated | SPN Node     |
+===============+==============+==============+
| us-east       | 200          | us-east-palm |
+---------------+--------------+--------------+

Returns the SPN Node after allocation of the BW
