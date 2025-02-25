# Got it! Let’s visualize the experimental results carefully, plotting the algorithms to match the matrix sizes they were tested on:
# - DFS up to size 20
# - Greedy up to size 25
# - DFS_wrap up to size 15
# - Greedy_wrap up to size 20

import matplotlib.pyplot as plt

# Data points for each algorithm
dfs_sizes = list(range(4, 21))
dfs_times = [0.0001609182357788086, 0.0006995868682861329, 0.001269073486328125, 0.0017580556869506835, 
             0.0016928982734680175, 0.003731110095977783, 0.005226616859436035, 0.004227118492126465, 
             0.009637789726257324, 0.02632197618484497, 0.12815439701080322, 0.2343933129310608, 
             0.4378528642654419, 0.49462744474411013, 0.5825985336303711, 0.9891670775413514, 
             0.9394499683380126]

greedy_sizes = list(range(4, 26))
greedy_times = [0.0013460516929626465, 0.0027971863746643066, 0.004264702796936035, 0.005679285526275635, 
                0.00946399211883545, 0.014941916465759278, 0.01901954412460327, 0.028078815937042235, 
                0.03975771188735962, 0.053376626968383786, 0.07470666885375976, 0.12568434000015258, 
                0.13423579931259155, 0.1669769334793091, 0.20896735906600952, 0.17567315101623535, 
                0.10139958381652832, 1.2055198001861571, 0.5462160730361938, 0.7693249964714051, 
                1.553399097919464, 0.8273705673217774]

dfs_wrap_sizes = list(range(4, 16))
dfs_wrap_times = [0.0009376621246337891, 0.004224455356597901, 0.008377377986907958, 0.01737138032913208, 
                  0.03576856851577759, 0.05263018846511841, 0.1860103178024292, 0.3498684358596802, 
                  0.6070546126365661, 1.2178926634788514, 2.6753934526443484, 4.7618291330337525]

greedy_wrap_sizes = list(range(4, 21))
greedy_wrap_times = [0.002159888744354248, 0.0033843278884887694, 0.004069955348968506, 0.007625997066497803, 
                     0.010198197364807128, 0.014300603866577149, 0.023418362140655517, 0.021603496074676515, 
                     0.04239072561264038, 0.08654677391052246, 0.06107040643692017, 0.07024036169052124, 
                     0.10248760938644409, 0.2011355757713318, 0.1634056830406189, 0.18260119199752808, 
                     0.33006205797195437]

# Plotting the results
fig, axs = plt.subplots(2, 1, figsize=(12, 10))

# DFS vs Greedy
axs[0].plot(dfs_sizes, dfs_times, label='DFS', marker='o')
axs[0].plot(greedy_sizes, greedy_times, label='Greedy', marker='s')
axs[0].set_title('DFS vs Greedy Algorithm')
axs[0].set_xlabel('Matrix Size')
axs[0].set_ylabel('Time (seconds)')
axs[0].legend()
axs[0].grid()

# DFS_wrap vs Greedy_wrap
axs[1].plot(dfs_wrap_sizes, dfs_wrap_times, label='DFS_wrap', marker='o')
axs[1].plot(greedy_wrap_sizes, greedy_wrap_times, label='Greedy_wrap', marker='s')
axs[1].set_title('DFS_wrap vs Greedy_wrap Algorithm')
axs[1].set_xlabel('Matrix Size')
axs[1].set_ylabel('Time (seconds)')
axs[1].legend()
axs[1].grid()

plt.tight_layout()
plt.show()