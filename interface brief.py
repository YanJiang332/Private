

from textfsm import TextFSM
from pprint import pprint
import re

raw_result = """
display interface brief
PHY: Physical
*down: administratively down
^down: standby
(l): loopback
(s): spoofing
(E): E-Trunk down
(b): BFD down
(B): Bit-error-detection down
(e): ETHOAM down
(d): Dampening Suppressed
(p): port alarm down
(ld): loop-detect trigger down
(mf): mac-flapping blocked
(c): CFM down
(sd): STP instance discarding
InUti/OutUti: input utility/output utility
Interface                   PHY   Protocol  InUti OutUti   inErrors  outErrors
50GE4/0/5(100M)             down  down         0%     0%          0          0
50GE4/1/3(100M)             down  down         0%     0%          0          0
50|100GE4/0/4(100M)         down  down         0%     0%          0          0
50|100GE4/0/6(100G)         up    down      0.01%  0.01%          0          0
50|100GE4/1/2(50G)          down  down         0%     0%          0          0
Eth-Trunk4                  up    up       28.68%  5.39%          0          0
  50|100GE3/0/2(100G)       up    up       28.64%  5.38%          0          0
  50|100GE3/1/2(100G)       up    up       28.73%  5.40%          0          0
Eth-Trunk10                 up    up       33.99%  6.66%          0          0
  50|100GE3/1/4(100G)       up    up       34.49%  6.73%          0          0
  50|100GE4/0/2(100G)       up    up       33.48%  6.59%          0          0
Eth-Trunk12                 up    up        9.98% 51.79%          0          0
  GigabitEthernet1/1/0(10G) up    up        9.81% 52.48%          0          0
  GigabitEthernet5/0/15(10G) up    up        9.71% 52.84%          0          0
  GigabitEthernet5/1/12(10G) up    up        9.96% 50.68%          0          0
  GigabitEthernet6/1/4(10G) up    up       10.33% 50.92%          0          0
  GigabitEthernet7/1/19(10G) up    up       10.07% 52.04%          0          0
Eth-Trunk15                 up    down     44.62%  3.76%  649974380          0
  GigabitEthernet1/1/12(10G) up    up       43.41%  3.68%          2          0
  GigabitEthernet1/1/17(10G) up    up       43.28%  3.67%        856          0
  GigabitEthernet5/0/1(10G) up    up       45.68%  3.90%      17550          0
  GigabitEthernet5/0/2(10G) up    up       48.48%  3.65%        189          0
  GigabitEthernet5/0/7(10G) up    up       45.77%  3.64%        129          0
  GigabitEthernet5/0/18(10G) up    up       45.05%  3.69%         15          0
  GigabitEthernet6/0/0(10G) up    up       43.24%  3.99%         27          0
  GigabitEthernet6/0/1(10G) up    up       45.49%  3.90%  649955553          0
  GigabitEthernet6/0/2(10G) up    up       43.36%  3.69%         59          0
  GigabitEthernet7/1/20(10G) up    up       42.45%  3.80%          0          0
Eth-Trunk15.101             up    up        0.01%  0.01%          0          0
Eth-Trunk15.111             up    down         0%     0%          0          0
Eth-Trunk15.201             up    up       11.62%  2.12%          0          0
Eth-Trunk15.208             up    up        0.01%     0%          0          0
Eth-Trunk15.211             up    up       32.75%  1.31%          0          0
Eth-Trunk15.225             up    up        0.01%  0.01%          0          0
Eth-Trunk15.231             *down down         0%     0%          0          0
Eth-Trunk15.241             up    up        0.01%  0.01%          0          0
Eth-Trunk15.245             up    up        0.29%     0%          0          0
Eth-Trunk15.251             up    up        0.01%  0.01%          0          0
Eth-Trunk15.261             up    up        0.01%     0%          0          0
Eth-Trunk15.300             up    up        0.01%     0%          0          0
Eth-Trunk15.412             up    up        0.01%  0.33%          0          0
Eth-Trunk25                 down  down         0%     0%          0          0
  GigabitEthernet7/1/9(10G) *down down         0%     0%          0          0
Eth-Trunk25.3               down  down         0%     0%          0          0
Eth-Trunk26                 up    up        0.01% 19.02%          0          0
  GigabitEthernet1/1/8(10G) up    up        0.01% 13.36%          0          0
  GigabitEthernet5/1/17(10G) up    up        0.01% 13.13%          0          0
  GigabitEthernet6/0/11(10G) up    up        0.01% 25.40%          0          0
  GigabitEthernet7/1/14(10G) up    up        0.01% 24.20%          0          0
Eth-Trunk29                 down  down         0%     0%          0          0
Eth-Trunk30                 down  down         0%     0%          0          0
Eth-Trunk32                 up    down      0.01%  0.01%          0          0
  GigabitEthernet6/0/10(10G) up    up        0.01%  0.01%          0          0
Eth-Trunk32.10              up    up           0%     0%          0          0
Eth-Trunk32.200             up    up        0.01%  0.01%          0          0
Eth-Trunk32.300             up    up           0%     0%          0          0
Eth-Trunk32.333             up    up        0.01%  0.01%          0          0
Eth-Trunk33                 down  down         0%     0%          0          0
Eth-Trunk33.3               down  down         0%     0%          0          0
Eth-Trunk34                 up    down      6.43%  0.01%          0          0
  GigabitEthernet5/1/1(10G) up    up        6.43%  0.01%          0          0
Eth-Trunk34.10              up    up        0.01%  0.01%          0          0
Eth-Trunk34.20              up    up        6.43%     0%          0          0
Eth-Trunk34.30              up    up        0.01%     0%          0          0
Eth-Trunk34.400             up    up        0.01%  0.01%          0          0
Eth-Trunk36                 up    down      0.01%  0.64%          0          0
  50|100GE4/0/0(100G)       up    up        0.01%  0.64%          0          0
Eth-Trunk36.600             up    up        0.01%  0.64%          0          0
Eth-Trunk40                 down  down         0%     0%          0          0
Eth-Trunk40.3               down  down         0%     0%          0          0
Eth-Trunk41                 up    down      4.34%  9.06%         42          0
  GigabitEthernet7/1/10(10G) up    up        4.34%  9.06%         42          0
Eth-Trunk41.3               up    up        4.15%  9.06%          0          0
Eth-Trunk45                 down  down         0%     0%          0          0
Eth-Trunk45.4               down  down         0%     0%          0          0
Eth-Trunk47                 up    down      2.93% 34.32%          0          0
  GigabitEthernet1/1/18(10G) up    up        3.00% 33.93%          0          0
  GigabitEthernet1/1/22(10G) up    up        2.58% 34.24%          0          0
  GigabitEthernet5/0/19(10G) up    up        3.13% 34.38%          0          0
  GigabitEthernet7/1/2(10G) up    up        2.80% 34.40%          0          0
  GigabitEthernet7/1/4(10G) up    up        3.24% 35.26%          0          0
  GigabitEthernet7/1/22(10G) up    up        2.84% 33.74%          0          0
Eth-Trunk47.3               up    up        2.95% 34.36%          0          0
Eth-Trunk51                 up    up        0.71%  0.37%          0          0
  GigabitEthernet5/0/6(10G) up    up        0.71%  0.37%          0          0
  GigabitEthernet6/0/3(10G) up    up        0.01%  0.01%          0          0
Eth-Trunk59                 up    down      0.01%  0.01%          0          0
  GigabitEthernet5/0/10(10G) up    up        0.01%  0.01%          0          0
  GigabitEthernet6/0/6(10G) up    up        0.01%  0.01%          0          0
Eth-Trunk59.111             up    up        0.01%  0.01%          0          0
Eth-Trunk59.231             up    up        0.01%     0%          0          0
Eth-Trunk60                 up    down      4.25% 41.63%     104770          0
  GigabitEthernet1/1/13(10G) up    up        4.48% 42.31%         68          0
  GigabitEthernet1/1/15(10G) up    up        4.25% 41.62%     103361          0
  GigabitEthernet1/1/16(10G) up    up        4.32% 41.24%        555          0
  GigabitEthernet5/0/4(10G) up    up        4.08% 41.45%          2          0
  GigabitEthernet5/0/5(10G) up    up        4.24% 41.58%          8          0
  GigabitEthernet5/0/9(10G) up    up        4.38% 40.91%         48          0
  GigabitEthernet5/0/14(10G) up    up        4.24% 41.34%         26          0
  GigabitEthernet5/0/16(10G) up    up        4.36% 42.97%         21          0
  GigabitEthernet7/1/15(10G) up    up        4.08% 41.99%          0          0
  GigabitEthernet7/1/16(10G) up    up        4.20% 41.61%        681          0
  GigabitEthernet7/1/18(10G) up    up        4.12% 40.95%          0          0
Eth-Trunk60.10              up    up        2.07% 11.19%          0          0
Eth-Trunk60.20              up    up        0.01%     0%          0          0
Eth-Trunk60.30              up    up        0.01%     0%          0          0
Eth-Trunk60.40              up    up        0.01%     0%          0          0
Eth-Trunk60.50              up    up        0.01%     0%          0          0
Eth-Trunk60.60              up    up        0.01%     0%          0          0
Eth-Trunk60.70              up    up        0.01%     0%          0          0
Eth-Trunk60.80              up    up        0.01%     0%          0          0
Eth-Trunk60.90              up    up        0.01%     0%          0          0
Eth-Trunk60.100             up    up        2.16% 30.19%          0          0
Eth-Trunk60.110             up    up        0.01%  0.26%          0          0
Eth-Trunk60.203             up    up        0.01%     0%          0          0
Eth-Trunk60.212             up    up        0.01%     0%          0          0
Eth-Trunk60.220             up    up        0.01%     0%          0          0
Eth-Trunk61                 up    down     69.76%  0.01%          0          0
  GigabitEthernet1/1/10(10G) up    up       69.71%  0.01%          0          0
  GigabitEthernet5/0/11(10G) up    up       69.82%  0.01%          0          0
Eth-Trunk61.210             up    up        0.01%     0%          0          0
Eth-Trunk61.220             up    up       12.87%  0.01%          0          0
Eth-Trunk61.230             up    up        0.58%  0.01%          0          0
Eth-Trunk61.240             up    up        0.01%     0%          0          0
Eth-Trunk61.250             up    up        0.55%     0%          0          0
Eth-Trunk61.260             up    up       55.64%     0%          0          0
Eth-Trunk66                 down  down         0%     0%          0          0
Eth-Trunk71                 up    up        8.84% 38.08%        305          0
  50|100GE3/1/6(100G)       up    up        8.84% 38.08%        305          0
Eth-Trunk73                 up    down      0.01%  0.01%          0          0
  GigabitEthernet5/0/23(10G) up    up        0.01%  0.01%          0          0
  GigabitEthernet5/1/4(10G) up    up        0.01%  0.01%          0          0
  GigabitEthernet6/0/4(10G) up    up        0.01%  0.01%          0          0
Eth-Trunk73.3               *down down         0%     0%          0          0
Eth-Trunk73.1000            up    down         0%     0%          0          0
Eth-Trunk73.1121            up    up           0%     0%          0          0
Eth-Trunk73.3000            up    up        0.01%  0.01%          0          0
Eth-Trunk73.4045            up    up           0%     0%          0          0
Eth-Trunk73.4046            up    up           0%     0%          0          0
Eth-Trunk73.4047            up    up           0%     0%          0          0
Eth-Trunk74                 up    down      0.01%  0.01%          0          0
  GigabitEthernet5/1/6(10G) up    up        0.01%  0.01%          0          0
  GigabitEthernet5/1/14(10G) up    up        0.01%  0.01%          0          0
  GigabitEthernet6/0/8(10G) up    up        0.01%  0.01%          0          0
Eth-Trunk74.3               *down down         0%     0%          0          0
Eth-Trunk74.1000            *down down         0%     0%          0          0
Eth-Trunk74.1004            *down down         0%     0%          0          0
Eth-Trunk74.1006            up    up           0%     0%          0          0
Eth-Trunk74.1007            up    up           0%     0%          0          0
Eth-Trunk74.4046            up    up           0%     0%          0          0
Eth-Trunk74.4047            up    up           0%     0%          0          0
Eth-Trunk75                 down  down         0%     0%          0          0
  GigabitEthernet5/0/3(10G) down  down         0%  0.01%          0          0
  GigabitEthernet5/0/8(10G) down  down         0%  0.01%          0          0
  GigabitEthernet6/0/5      down  down         0%  0.01%          0          0
Eth-Trunk75.3               down  down         0%     0%          0          0
Eth-Trunk76                 up    down      0.01%  0.01%          0          0
  GigabitEthernet5/1/18(10G) up    up        0.01%  0.01%          0          0
  GigabitEthernet5/1/19(10G) up    up        0.01%  0.01%          0          0
  GigabitEthernet6/0/9(10G) up    up        0.01%  0.01%          0          0
Eth-Trunk76.3               *down down         0%     0%          0          0
Eth-Trunk76.1000            up    up           0%     0%          0          0
Eth-Trunk76.1014            up    up           0%     0%          0          0
Eth-Trunk78                 up    down     73.00%  7.37%          0          0
  GigabitEthernet5/1/21(10G) up    up       73.60%  7.37%          0          0
  GigabitEthernet5/1/23(10G) up    up       72.21%  7.37%          0          0
  GigabitEthernet6/1/3(10G) up    up       73.19%  7.37%          0          0
Eth-Trunk78.3               *down down         0%     0%          0          0
Eth-Trunk78.4045            up    up       72.75%  7.42%          0          0
Eth-Trunk97                 down  down         0%     0%          0          0
  GigabitEthernet1/1/2(10G) down  down         0%     0%          0          0
  GigabitEthernet7/1/6(10G) down  down         0%     0%          0          0
Eth-Trunk97.3               down  down         0%     0%          0          0
Eth-Trunk101                up    down     38.93%  3.59%          0          0
  GigabitEthernet1/1/7(10G) up    up       36.91%  3.42%          0          0
  GigabitEthernet5/0/20(10G) up    up       41.05%  3.62%          0          0
  GigabitEthernet6/1/1(10G) up    up       38.46%  3.47%          0          0
  GigabitEthernet6/1/5(10G) up    up       39.31%  3.87%          0          0
Eth-Trunk101.15             up    up           0%     0%          0          0
Eth-Trunk101.1003           up    up       39.03%  3.59%          0          0
Eth-Trunk101.3000           up    up           0%     0%          0          0
Eth-Trunk104                up    down     20.52%  2.05%          0          0
  GigabitEthernet7/1/1(10G) up    up       21.46%  1.99%          0          0
  GigabitEthernet7/1/3(10G) up    up       19.60%  2.05%          0          0
  GigabitEthernet7/1/23(10G) up    up       20.49%  2.12%          0          0
Eth-Trunk104.1000           up    up       20.46%  2.05%          0          0
Eth-Trunk104.1400           up    up           0%     0%          0          0
Eth-Trunk104.2000           up    up           0%     0%          0          0
Eth-Trunk105                up    down     21.59%  1.98%          0          0
  GigabitEthernet1/1/19(10G) up    up       24.04%  2.07%          0          0
  GigabitEthernet1/1/20(10G) up    up       20.43%  1.91%          0          0
  GigabitEthernet1/1/21(10G) up    up       21.26%  2.02%          0          0
  GigabitEthernet1/1/23(10G) up    up       20.65%  1.92%          0          0
Eth-Trunk105.1000           up    up           0%     0%          0          0
Eth-Trunk105.3000           up    up           0%     0%          0          0
Eth-Trunk105.4045           up    up       21.45%  1.91%          0          0
Eth-Trunk105.4046           up    up           0%     0%          0          0
Eth-Trunk111                down  down         0%     0%          0          0
Eth-Trunk112                up    up       18.93%  2.58%          0          0
  100GE7/0/1                up    up       18.77%  2.64%          0          0
  50|100GE3/0/0(100G)       up    up       19.09%  2.52%          0          0
Eth-Trunk115                up    up       28.35% 26.50%       1477          0
  100GE1/0/0                up    up       30.29% 26.51%       1468          0
  50|100GE4/1/0(100G)       up    up       26.52% 26.53%          9          0
  50|100GE4/1/6(100G)       up    up       28.23% 26.44%          0          0
Eth-Trunk120                up    up       25.97% 26.72%          0          0
  100GE7/0/0                up    up       26.30% 26.71%          0          0
  50|100GE3/0/4(100G)       up    up       25.88% 26.68%          0          0
  50|100GE4/1/4(100G)       up    up       25.73% 26.77%          0          0
Eth-Trunk125                up    up        4.20% 27.29%         31          0
  GigabitEthernet1/1/6(10G) up    up        3.92% 27.47%         31          0
  GigabitEthernet6/1/6(10G) up    up        4.47% 27.12%          0          0
Eth-Trunk150                up    up       25.30% 43.31%          0          0
  100GE1/0/1                up    up       25.04% 41.52%          0          0
  50|100GE3/1/0(100G)       up    up       25.56% 45.11%          0          0
Eth-Trunk201                down  down         0%     0%          0          0
Eth-Trunk201.1000           down  down         0%     0%          0          0
Eth-Trunk203                up    up        6.03% 51.63%          0          0
  50|100GE3/0/6(100G)       up    up        6.03% 51.63%          0          0
Eth-Trunk203.4045           up    down         0%     0%          0          0
Eth-Trunk204                down  down         0%     0%          0          0
Eth-Trunk204.1000           down  down         0%     0%          0          0
Eth-Trunk205                up    up       23.23% 66.66%      64877          0
  GigabitEthernet5/0/12(10G) up    up       23.73% 66.24%        385          0
  GigabitEthernet5/0/13(10G) up    up       23.36% 66.18%      59612          0
  GigabitEthernet5/1/9(10G) up    up       23.02% 66.73%         50          0
  GigabitEthernet5/1/10(10G) up    up       24.21% 66.58%       1362          0
  GigabitEthernet5/1/11(10G) up    up       23.05% 66.58%       1550          0
  GigabitEthernet6/1/8(10G) up    up       23.58% 66.88%        672          0
  GigabitEthernet6/1/9(10G) up    up       22.52% 66.63%        673          0
  GigabitEthernet6/1/10(10G) up    up       22.51% 67.13%        198          0
  GigabitEthernet6/1/11(10G) up    up       23.09% 67.00%        375          0
Eth-Trunk220                up    up        4.85% 33.27%        641          0
  GigabitEthernet1/1/9(10G) up    up        5.23% 32.88%          0          0
  GigabitEthernet5/0/17(10G) up    up        4.85% 33.59%          0          0
  GigabitEthernet5/1/0(10G) up    up        4.67% 33.48%          0          0
  GigabitEthernet7/1/7(10G) up    up        4.67% 33.11%        641          0
GigabitEthernet0/0/0        *down down         0%     0%          0          0
GigabitEthernet1/1/1(10G)   down  down         0%     0%          0          0
GigabitEthernet1/1/3(10G)   down  down         0%     0%          0          0
GigabitEthernet1/1/4(10G)   down  down         0%     0%          0          0
GigabitEthernet1/1/5(10G)   up    down      0.01%  0.01%          0          0
GigabitEthernet1/1/11(10G)  down  down         0%     0%          0          0
GigabitEthernet1/1/14(10G)  up    up        0.01%  0.01%          0          0
GigabitEthernet5/0/0(10G)   up    up       23.81%  2.49%         77          0
GigabitEthernet5/0/21(10G)  down  down         0%     0%          0          0
GigabitEthernet5/0/22(10G)  down  down         0%     0%          0          0
GigabitEthernet5/1/2(10G)   down  down         0%     0%          0          0
GigabitEthernet5/1/3(10G)   *down down         0%     0%          0          0
GigabitEthernet5/1/5(10G)   *down down         0%     0%          0          0
GigabitEthernet5/1/7(10G)   *down down         0%     0%          0          0
GigabitEthernet5/1/8(10G)   *down down         0%     0%          0          0
GigabitEthernet5/1/13(10G)  down  down         0%     0%          0          0
GigabitEthernet5/1/15(10G)  up    up       53.75%  5.72%          0          0
GigabitEthernet5/1/16(10G)  *down down         0%     0%          0          0
GigabitEthernet5/1/20(10G)  *down down         0%     0%          0          0
GigabitEthernet5/1/22(10G)  *down down         0%     0%          0          0
GigabitEthernet6/0/7(10G)   down  down         0%     0%          0          0
GigabitEthernet6/1/0(10G)   down  down         0%     0%          0          0
GigabitEthernet6/1/2(10G)   down  down         0%     0%          0          0
GigabitEthernet6/1/7(10G)   up    up       54.97% 20.96%          0          0
GigabitEthernet7/1/0(10G)   down  down         0%     0%          0          0
GigabitEthernet7/1/5(10G)   up    down      0.01%  0.01%          0          0
GigabitEthernet7/1/8(10G)   down  down         0%     0%          0          0
GigabitEthernet7/1/11(10G)  down  down         0%     0%          0          0
GigabitEthernet7/1/12(10G)  down  down         0%     0%          0          0
GigabitEthernet7/1/13(10G)  down  down         0%     0%          0          0
GigabitEthernet7/1/17(10G)  down  down         0%     0%          0          0
GigabitEthernet7/1/21(10G)  down  down         0%     0%          0          0
LoopBack0                   up    up(s)        0%     0%          0          0
LoopBack1                   up    up(s)        0%     0%          0          0
NULL0                       up    up(s)        0%     0%          0          0
Tunnel0/0/101               *down down         --     --          0          0
Tunnel0/0/103               *down down         --     --          0          0
Tunnel0/0/105               *down down         --     --          0          0
Tunnel0/0/111               down  down         --     --          0          0
Tunnel0/0/113               down  down         --     --          0          0
Tunnel0/0/115               down  down         --     --          0          0
Tunnel0/0/116               up    up           --     --          0          0
Tunnel0/0/117               up    up           --     --          0          0
Tunnel0/0/118               *down down         --     --          0          0
Tunnel0/0/119               *down down         --     --          0          0
Tunnel0/0/120               *down down         --     --          0          0
Tunnel0/0/121               *down down         --     --          0          0
Tunnel0/0/122               up    up           --     --          0          0
Tunnel0/0/123               up    up           --     --          0          0
Tunnel0/0/125               up    up           --     --          0          0
Virtual-Template0           up    up(s)        0%     0%          0          0
"""

raw_result = raw_result.split('GigabitEthernet0/0/0')

def parse_data_with_template(template_path, raw_result):
    with open(template_path) as f:
        template = TextFSM(f)
        data = template.ParseText(raw_result)
        print(data)
    return data

def process_data(data):
    eth_trunks = {}
    for item in data:

        if '.' not in item[0]:
            # print(item)
            # print(data)
            if item[0].startswith('Eth-Trunk'):
                eth_trunks[item[0]] = []
            elif len(eth_trunks) > 0 and list(eth_trunks.keys())[-1].startswith('Eth-Trunk'):
                list(eth_trunks.values())[-1].append(item[0])
            else:
                eth_trunks[item[0]] = []
    # print(eth_trunks)
    return eth_trunks

def format_result(eth_trunks):
    result = []
    for key, values in eth_trunks.items():
        if values:
            for value in values:
                result.append([key, value])
        else:
            result.append(['N/A', key])
    return result

def remove_brackets_from_interfaces(result):
    for item in result:
        item[1] = re.sub(r'\(.*?\)', '', item[1])
    return result

def format_result1(eth_trunks):
    Y = {}
    for key, values in eth_trunks.items():
        if values:
            for value in values:
                if value not in Y:
                    Y[value] = []
                Y[value].append(key)
        else:
            if key not in Y:
                Y[key] = []
            Y[key].append('N/A')
    return Y

# 使用函数
def interface_brief():
    template_path = './template/display_interface_brief.template'
    data = parse_data_with_template(template_path, raw_result[0])
    data1 = parse_data_with_template(template_path, raw_result[1])
    eth_trunks = process_data(data)
    eth_trunks1 = process_data(data1)
    eth_trunk_port = format_result1(eth_trunks)
    eth_trunk_port1 = format_result1(eth_trunks1)
    # trunk_port = remove_brackets_from_interfaces(eth_trunk_port + eth_trunk_port1)
    trunk_port = {}
    trunk_port.update(eth_trunk_port)
    trunk_port.update(eth_trunk_port1)
    
    return trunk_port


if __name__ == '__main__':
    pprint(interface_brief())